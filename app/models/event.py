from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__='events'

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    start_time=Column(DateTime,nullable=False)
    end_time=Column(DateTime,nullable=True)
    created_via=Column(String,default="manual")
    created_at=Column(DateTime)

    user_id=Column(Integer,ForeignKey("users.id"), nullable=False)
    owner=relationship("User",back_populates="events")