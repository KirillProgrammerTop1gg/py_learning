from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme)) -> tuple[int, str]:
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        user_role = payload.get("role")
        if user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недійсний токен: відсутні поля user_id або role",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id, user_role
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не вдалося розшифрувати токен",
            headers={"WWW-Authenticate": "Bearer"},
        )