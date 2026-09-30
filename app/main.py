from fastapi import FastAPI
from app.database import Base, engine
from app. routes import events
from app.models import user, event 

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Scheduler API")
app.include_router(events.router)

@app.get("/")
def root():
    return{"status":"ok","message":"Running"}