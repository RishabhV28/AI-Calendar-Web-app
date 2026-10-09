from fastapi import APIRouter, Depends,HTTPException,Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services import event_service
from datetime import datetime
from app.auth.dependencies import get_current_user
from app.models.user import User



router= APIRouter(prefix="/events", tags=['events'])

@router.post("/",response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db),current_user:User= Depends(get_current_user)):
    return event_service.create_event(db, event,user_id=current_user.id)

@router.get("/",response_model=list[EventResponse])
def list_events(db: Session=Depends(get_db),
                current_user: User=Depends(get_current_user),
                start: datetime |None=Query(None),
                end: datetime | None=Query(None),):
    if start and end:
        return event_service.get_events_in_range(db, current_user.id, start, end)
    return event_service.get_events(db,user_id=current_user.id)

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    event=event_service.delete_event(db,event_id,current_user.id)
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    return{"status": "deleted"}



@router.patch("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, data: EventUpdate, db: Session=Depends(get_db),current_user: User=Depends(get_current_user)):
    event=event_service.update_event(db, event_id, current_user.id, data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event