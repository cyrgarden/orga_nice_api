from sqlalchemy.orm import Session
from app import models
from app.schemas.room import Room, RoomCreate


def create_room(db: Session, room: RoomCreate):
    db_room = models.Room(**prise.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room



def get_all_rooms(db: Session):
    return db.query(models.Room).all()


def get_room_by_id(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def delete_user(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if db_room is None:
        return None
    db.delete(db_room)
    db.commit()
    return db_room
