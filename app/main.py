from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine
from app. routes import events, auth
from app.models import user, event 
from app.config import settings

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Scheduler API")
app.include_router(events.router)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(auth.router)

@app.get("/")
def root():
    return{"status":"ok","message":"Running"}