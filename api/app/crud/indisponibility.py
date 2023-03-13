from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all
from app.schemas.indisponibility import Indisponibility, IndisponibilityCreate


def create_indispo(db: Session, new_indispo: IndisponibilityCreate):
    db_indispo = models.Indisponibility(**new_indispo.dict())
    db.add(db_indispo)
    db.commit()
    db.refresh(db_indispo)
    return db_indispo


def delete_indispo(db: Session, indispo_id: int):
    db_indispo = db.query(models.Indisponibility).filter(models.Indisponibility.id == indispo_id).first()
    if db_indispo is None:
        return None
    db.delete(db_indispo)
    db.commit()
    return db_indispo

