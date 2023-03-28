from sqlalchemy.orm import Session
from app import models
from app.crud.user import get_user_by_id
from app.schemas.indisponibility import IndisponibilityCreate


def create_indispo(db: Session, new_indispo: IndisponibilityCreate):
    db_indispo = models.Indisponibility(**new_indispo.dict())
    db.add(db_indispo)
    db.commit()
    db.refresh(db_indispo)
    return db_indispo


def get_user_infos_by_room_and_date(db: Session, room_id: int, date: str):
    indispos = db.query(models.Indisponibility).filter(
        models.Indisponibility.room_id == room_id).filter(models.Indisponibility.date == date).all()
    if indispos is None:
        return None


    id_list = []

    for indispo in indispos:
        user = get_user_by_id(db, indispo.user_id)
        if user == None:
            pass
        id_list.append(user.username)

    if len(id_list) == 0:
        return None

    return id_list


def delete_indispo(db: Session, indispo_id: int):
    db_indispo = db.query(models.Indisponibility).filter(
        models.Indisponibility.id == indispo_id).first()
    if db_indispo is None:
        return None
    db.delete(db_indispo)
    db.commit()
    return db_indispo
