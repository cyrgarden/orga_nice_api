from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all
from app.schemas.reco_indispo import RecoIndispo, RecoIndispoCreate


def create_indispo(db: Session, new_indispo: RecoIndispoCreate):
    db_indispo = models.RecoIndispo(**new_indispo.dict())
    db.add(db_indispo)
    db.commit()
    db.refresh(db_indispo)
    return db_indispo


def delete_indispo(db: Session, indispo_id: int):
    db_indispo = db.query(models.RecoIndispo).filter(models.RecoIndispo.id == indispo_id).first()
    if db_indispo is None:
        return None
    db.delete(db_indispo)
    db.commit()
    return db_indispo

