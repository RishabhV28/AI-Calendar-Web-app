from app.database import SessionLocal
from app.models.user import User
from app.database import SessionLocal
from app.models.user import User
from app.models.event import Event 

db= SessionLocal()
if not db.query(User).filter(User.id==1).first():
    db.add(User(id=1, google_id="dev", email="dev@example.com", name="Dev"))
    db.commit()

db.close()