from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all
from app.schemas.event import Event, EventCreate, EventOrderBy




def get_all_event(
    db: Session,
    limit: int,
    offset: int,
    orderby: EventOrderBy,
    reverse: bool,
):
    return get_all(db, models.Event, limit, offset, orderby, reverse, None)

def create_event(db: Session, event: EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        return None
    db.delete(db_event)
    db.commit()
    return db_event

