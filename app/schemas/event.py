from pydantic import BaseModel
from datetime import datetime
from typing import Optional 

class EventCreate(BaseModel):
    title: str
    start_time: datetime
    end_time: Optional[datetime]=None

class EventUpdate(BaseModel):
    title: Optional[str]=None
    start_time: Optional[datetime]=None
    end_time: Optional[datetime]=None

class EventResponse(EventCreate):
    id: int
    created_via: str
    user_id: int

    class Config:
        from_attributes=True