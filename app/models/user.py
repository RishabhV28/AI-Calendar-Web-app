from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    google_id=Column(String,unique=True,index=True,nullable=False)
    email=Column(String, unique=True, index=True, nullable=False)
    name=Column(String)

    events=relationship("Event", back_populates="owner")