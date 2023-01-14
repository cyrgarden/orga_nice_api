from sqlalchemy.orm import Session
from app import models
from app.schemas.room import Room, RoomCreate
from app.schemas.user import User
import app.crud.user as crud_user


def create_room(db: Session, room: RoomCreate, user_id: int):
    user = crud_user.get_user_by_id(db, user_id)
    db_room = models.Room(**room.dict())
    db_room.users.append(user)
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

def get_room_users(db:Session, room_id:int): 
    room = get_room_by_id(db, room_id)
    print(room.users)
    return room.users