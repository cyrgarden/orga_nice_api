from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all
from app.schemas.recommandation import Recommandation, RecommandationCreate, RecommandationOrderBy




def get_all_recommandation(
    db: Session,
    limit: int,
    offset: int,
    orderby: RecommandationOrderBy,
    reverse: bool,
):
    return get_all(db, models.Recommandation, limit, offset, orderby, reverse, None)


def create_recommandation(db: Session, reco: RecommandationCreate):
    db_reco = models.Recommandation(**reco.dict())
    db.add(db_reco)
    db.commit()
    db.refresh(db_reco)
    return db_reco


def delete_recommandation(db: Session, reco_id: int):
    db_reco = db.query(models.Recommandation).filter(models.Recommandation.id == reco_id).first()
    if db_reco is None:
        return None
    db.delete(db_reco)
    db.commit()
    return db_reco
