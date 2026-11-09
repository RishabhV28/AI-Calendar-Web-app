from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import dateparser
from app.schemas.event import EventCreate
from app.services import event_service

def now_local() -> datetime:
    return datetime.now(ZoneInfo("Asia/Kolkata")).replace(tzinfo=None)

def resolve(date_text:str,time_text:str="00:00"):
    return dateparser.parse(
        f"{date_text} {time_text}",
        settings={"RELATIVE_BASE": now_local(),"PREFER_DATES_FROM":"future"},
    )

def run_tool(name:str,args:dict, db, user)-> dict:
    if name=="create_event":
        start=resolve(args["date"],args["time"])
        if start is None:
            return {"status":"error","message":f"Couldn't understand the date '{args['date']}'"}
        end=start+timedelta(minutes=args.get("duration_minutes") or 60)

        conflicts=event_service.get_events_in_range(db, user.id, start, end)
        if conflicts:
            return{"status":"conflict", "conflicts":[
                {"title": c.title, "start": c.start_time.isoformat(),"end": c.end_time.isoformat()}
                for c in conflicts
            ]}

        event=event_service.create_event(
            db, EventCreate(title=args["title"], start_time=start, end_time=end),
            user_id=user.id, created_via="chat",
        )
        return {"status": "created", "id": event.id, "title":event.title, "start": event.start_time.isoformat()}

    if name=="list_events":
        day=resolve(args["date"])
        if day is None:
            return {"status":"error", "message": f"Couldnt understand the date '{args['date']}'"}
        day_start=day.replace(hour=0, minute=0, second=0, microsecond=0)
        events=event_service.get_events_in_range(db,user.id, day_start, day_start+ timedelta(days=1))
        return {"status": "ok", "events": [
            {"title": e.title, "start": e.start_time.isoformat(), "end": e.end_time.isoformat()} for e in events
        ]}
    return {"status":"error","message": f"unknown tool{name}"}