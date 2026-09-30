from sqlalchemy.orm import Session
from datetime import datetime,timedelta
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate

def create_event(db: Session, event:EventCreate, user_id:int, created_via: str="manual"):
    data=event.model_dump()
    if data["end_time"] is None:
        data["end_time"]=data["start_time"]+timedelta(hours=1)
    db_event=Event(**data,user_id=user_id,created_via=created_via,created_at=datetime.utcnow())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events(db: Session, user_id: int):
    return db.query(Event).filter(Event.user_id==user_id).order_by(Event.start_time).all()

def delete_event(db: Session, event_id: int,user_id:int):
    event=db.query(Event).filter(Event.id == event_id,Event.user_id==user_id).first()
    if event:
        db.delete(event)
        db.commit()
    return event

def update_event(db: Session, event_id: int, user_id: int, data: EventUpdate):
    event=db.query(Event).filter(Event.id==event_id, Event.user_id==user_id).first()
    if not event:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

def get_events_in_range(db: Session, user_id: int,start: datetime, end: datetime):
    return (
        db.query(Event)
        .filter(Event.user_id==user_id, Event.start_time<end, Event.end_time>start)
        .order_by(Event.start_time)
        .all()
    )
