from sqlalchemy.orm import Session

from app import models
from app.crud.utils import get_all
from app.schemas.log import LogCreate, LogsOrderBy


def get_logs(db: Session, offset: int, limit: int, orderby: LogsOrderBy, reverse: bool):
    return get_all(db, models.Logs, limit, offset, orderby, reverse, None)


def clear_logs(db: Session):
    db.query(models.Logs).delete()
    db.commit()
    return True


def add_log(db: Session, log: LogCreate):
    db_log = models.Logs(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

