from sqlalchemy.orm import Session
from app import models
from app.crud.utils import get_all, get_coordinates, compute_distance
from app.schemas.recommandation import Recommandation, RecommandationCreate, RecommandationOrderBy
from sqlalchemy.sql.expression import func


def get_all_recommandation(
    db: Session,
    limit: int,
    offset: int,
    orderby: RecommandationOrderBy,
    reverse: bool,
):
    return get_all(db, models.Recommandation, limit, offset, orderby, reverse, None)

def is_not_in(a, b) :
    return a not in b
    

def get_recommandations_filtered(db:Session, type,price, origin_city, maximum_distance, indispo):
    
    if type == "":
        all_reco = db.query(models.Recommandation).filter(models.Recommandation.price <= price).all()

    else:
        all_reco = db.query(models.Recommandation).filter(models.Recommandation.recommandation_type == type).filter(models.Recommandation.price <= price).filter(is_not_in(indispo, models.Recommandation.indispo) == True).all()
    
    origin = get_coordinates(origin_city, 'FR')
    print(origin)
    
    final_reco_list = []
        
    for reco in all_reco:
        if (compute_distance(origin[0], origin[1], reco.lat, reco.lon) <= maximum_distance) :
            final_reco_list.append(reco)
    
    return final_reco_list
        
def get_recommandations_by_type(db:Session, reco_type:str):
    return db.query(models.Recommandation).filter(models.Recommandation.recommandation_type == reco_type).all()

def get_recommandations_by_subtype(db:Session, subtype:str):
    return db.query(models.Recommandation).filter(models.Recommandation.subtype == subtype).order_by(models.Recommandation.price, func.random()).all()
        
    
    
def create_recommandation(db: Session, reco: RecommandationCreate):
    print("start crud")
    db_reco = models.Recommandation(**reco.dict())
    
    print("location start")
    coordinates = get_coordinates(db_reco.place, 'FR')
    db_reco.lat = coordinates[0]
    db_reco.lon = coordinates[1]
    print("location end")
    
    db.add(db_reco)
    db.commit()
    db.refresh(db_reco)
    print("end crud")
    return db_reco


def delete_recommandation(db: Session, reco_id: int):
    db_reco = db.query(models.Recommandation).filter(models.Recommandation.id == reco_id).first()
    if db_reco is None:
        return None
    db.delete(db_reco)
    db.commit()
    return db_reco


