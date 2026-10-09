from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.config import settings
from app.auth.jwt_handler import create_access_token

router=APIRouter(prefix="/auth", tags=["auth"])

oauth=OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri=request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback", name="auth_callback")
async def auth_callback(request: Request, db: Session=Depends(get_db)):
    token=await oauth.google.authorize_access_token(request)
    user_info=token["userinfo"]

    user=db.query(User).filter(User.google_id==user_info["sub"]).first()
    if not user:
        user=User(google_id=user_info["sub"],email=user_info["email"], name=user_info["name"])
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token=create_access_token({"sub": str(user.id)})
    return {"access_token": jwt_token, "token_type": "bearer"}

