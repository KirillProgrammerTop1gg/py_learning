from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from src.token_utils import create_token
from src.database.db import get_db
from src.repository import users as repository_users
from src.routes import users, skills, exchanges, reviews, stats, categories

# Створюємо застосунок
app = FastAPI(
    title="SkillSwap API",
    description="REST API для платформи обміну навичками",
    version="2.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["<http://localhost:3000>"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо маршрути
app.include_router(users.router, prefix="/api")
app.include_router(skills.router, prefix="/api")
app.include_router(exchanges.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(categories.router, prefix="/api")


@app.get("/")
def read_root():
    return {
        "message": "Ласкаво просимо до SkillSwap API v2.1",
        "documentation": "/docs",
        "endpoints": {
            "categories": "/api/categories",
            "users": "/api/users",
            "skills": "/api/skills",
            "exchanges": "/api/exchanges",
            "reviews": "/api/reviews",
            "stats": "/api/stats",
        },
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Перевірка стану застосунку та БД."""
    try:
        # Простий запит для перевірки з'єднання з БД
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {"status": "healthy", "database": db_status, "version": "2.2.0"}
class TokenRequest(BaseModel):
    user_id: int
    role: str = "user"

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await repository_users.get_user_by_username(form_data.username, db)
    if not user:
        raise HTTPException(status_code=400, detail="Невірний username або пароль")
    
    token = create_token(user.id, role="user")
    return {"access_token": token, "token_type": "bearer"}

@app.on_event("startup")
async def startup_event():
    """Дії при запуску застосунку."""
    print("🚀 SkillSwap API запущено!")
    print("📚 Документація доступна на: <http://localhost:8000/docs>")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
