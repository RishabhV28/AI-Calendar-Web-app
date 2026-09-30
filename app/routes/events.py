from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services import event_service
from datetime import datetime

DEV_USER_ID=1

router= APIRouter(prefix="/events", tags=['events'])

@router.post("/",response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    return event_service.create_event(db, event,user_id=DEV_USER_ID)

@router.get("/",response_model=list[EventResponse])
def list_events(db: Session=Depends(get_db),
                start: datetime |None=Query(None),
                end: datetime | None=Query(None),):
    if start and end:
        return event_service.get_events_in_range(db, DEV_USER_ID, start, end)
    return event_service.get_events(db,user_id=DEV_USER_ID)

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session=Depends(get_db)):
    event=event_service.delete_event(db,event_id,DEV_USER_ID)
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    return{"status": "deleted"}


@router.post("/",response_model=EventResponse)
def create_event(event: EventCreate,db: Session= Depends(get_db)):
    return event_service.create_event(db, event, user_id=DEV_USER_ID)

@router.patch("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, data: EventUpdate, db: Session=Depends(get_db)):
    event=event_service.update_event(db, event_id, DEV_USER_ID, data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event