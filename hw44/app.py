from fastapi import (
    FastAPI,
    WebSocket,
    Request,
    WebSocketDisconnect,
    HTTPException,
    Depends,
    Query,
)
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_token, get_current_user_from_token
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from manager import manager, moderation, UserRole
from censor import censor_text
import uuid, logging
from datetime import datetime
from pwdlib import PasswordHash

logging.basicConfig(level=logging.INFO)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
pwd_context = PasswordHash.recommended()

users: dict[str, dict] = {}

moderation.set_users(users)


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    try:
        user_id, role = get_current_user_from_token(token)
    except HTTPException:
        await websocket.accept()
        await websocket.close(code=1008)
        logging.warning("WebSocket відхилено: невалідний токен")
        return

    user_data = users.get(user_id)
    if not user_data:
        await websocket.accept()
        await websocket.close(code=1008)
        logging.warning(f"WebSocket відхилено: користувач {user_id} не знайдений")
        return

    username = user_data["username"]

    if moderation.is_banned(username):
        await websocket.accept()
        await websocket.close(code=1008)
        logging.warning(f"WebSocket відхилено: {username} забанений")
        return

    await manager.connect(websocket, user_id=user_id, username=username)
    await manager.broadcast(f"🟢 {username} приєднався до чату")

    try:
        while True:
            data = await websocket.receive_text()

            if moderation.is_muted(username):
                remaining = moderation.muted_users.get(username)
                secs = (
                    int((remaining - datetime.now()).total_seconds())
                    if remaining
                    else 0
                )
                await manager.send_personal_message(
                    f"🔇 Ви замучені. Залишилось: {secs} сек.", websocket
                )
                continue

            if data.startswith("/"):
                result = await moderation.handle_command(
                    sender_username=username, message=data, manager=manager
                )
                if result:
                    await manager.send_personal_message(result, websocket)
                continue

            clean_data = censor_text(data)
            await manager.send_personal_message(f"Ви: {clean_data}", websocket)
            await manager.broadcast(f"{username}: {clean_data}", exclude=websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {username} покинув чат")
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
        try:
            await websocket.close()
        except Exception:
            pass


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_entry = next(
        ((uid, u) for uid, u in users.items() if u["username"] == form_data.username),
        None,
    )

    if not user_entry:
        raise HTTPException(status_code=400, detail="Невірний username або пароль")

    user_id, user = user_entry

    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Невірний username або пароль")

    token = create_token(
        user_id,
        role=user["role"].value if isinstance(user["role"], UserRole) else user["role"],
    )
    return {"access_token": token, "token_type": "bearer"}


@app.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    if any(u["username"] == form_data.username for u in users.values()):
        raise HTTPException(status_code=400, detail="Username вже зайнятий")

    user_id = str(uuid.uuid4())
    users[user_id] = {
        "username": form_data.username,
        "password": pwd_context.hash(form_data.password),
        "role": UserRole.USER if form_data.username != "admin" else UserRole.ADMIN,
    }
    logging.info(f"Новий користувач: {form_data.username} ({user_id})")
    return {"message": "Користувача створено", "user_id": user_id}
