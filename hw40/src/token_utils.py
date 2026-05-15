from datetime import datetime, timedelta
import jwt

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"


def create_token(user_id: int, role: str = "user") -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.now(datetime.timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)