from jose import jwt,JWTError
from datetime import datetime, timedelta
from app.config import settings

ALGORITHM="HS256"

def create_access_token(data: dict, expires_delta: timedelta=timedelta(days=7)):
    to_encode=data.copy()
    to_encode.update({"exp": datetime.utcnow()+expires_delta})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])