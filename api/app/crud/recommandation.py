from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all, get_coordinates, compute_distance
from app.schemas.recommandation import Recommandation, RecommandationCreate, RecommandationOrderBy




def get_all_recommandation(
    db: Session,
    limit: int,
    offset: int,
    orderby: RecommandationOrderBy,
    reverse: bool,
):
    return get_all(db, models.Recommandation, limit, offset, orderby, reverse, None)


def get_recommandations_filtered(db:Session, type, subtype, price, origin_city, maximum_distance):
    all_reco = db.query(models.Recommandation).filter(models.Recommandation.type == type).filter(models.Recommandation.subtype == subtype).filter(models.Recommandation.price <= price).all()
    
    origin = get_coordinates(origin_city, 'FR')
    
    final_reco_list = []
        
    for reco in all_reco:
        arrival = get_coordinates(reco.place)
        if (compute_distance(origin[0], origin[1], arrival[0], arrival[1]) <= maximum_distance) :
            final_reco_list.append(reco)
            
    return final_reco_list
        
        
    
    
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


