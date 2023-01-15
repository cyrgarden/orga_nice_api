from sqlalchemy.orm import Session
from app.crud.utils import get_all
from app import models
from app.schemas.errand import Errand, ErrandCreate, ErrandOrderBy
from app.schemas.user import User
import app.crud.event as crud_event


def create_errand(db: Session, errand: ErrandCreate):
    db_errand = models.Errand(**errand.dict())
    db.add(db_errand)
    db.commit()
    db.refresh(db_errand)
    return db_errand


def get_all_errands(
    db: Session,
    limit: int,
    offset: int,
    orderby: ErrandOrderBy,
    reverse: bool,
):
    return get_all(db, models.Errand, limit, offset, orderby, reverse, None)


def delete_errand(db: Session, errand_id: int):
    db_errand = db.query(models.Errand).filter(models.Errand.id == errand_id).first()
    if db_errand is None:
        return None
    db.delete(db_errand)
    db.commit()
    return db_errand


