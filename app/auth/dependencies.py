from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.auth.jwt_handler import decode_access_token
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security=HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials=Depends(security), db: Session =  Depends(get_db)) -> User:
    token=credentials.credentials
    try:
        payload=decode_access_token(token)
        user_id=int(payload.get('sub'))
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid or expired token")

    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user