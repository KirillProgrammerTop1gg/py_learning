from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from datetime import datetime, timedelta, timezone
import jwt, os
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ALGORITHM = "HS256"


def get_current_user(token: str = Depends(oauth2_scheme)) -> tuple[str, str]:
    return _validate_token(token)


def get_current_user_from_token(token: str) -> tuple[str, str]:
    return _validate_token(token)


def _validate_token(token: str) -> tuple[str, str]:
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
        return str(user_id), user_role
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не вдалося розшифрувати токен",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_token(user_id: str, role: str = "user") -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
