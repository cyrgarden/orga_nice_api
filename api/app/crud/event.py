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


