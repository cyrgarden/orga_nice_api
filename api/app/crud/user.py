from sqlalchemy.orm import Session
from app import models
from app.schemas.room import RoomCreate



def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def new_user(db: Session, user: str, password: str, is_admin: bool):
    print("CRUD : ")
    db_user = models.User(username=user, password=password, admin=is_admin)
    db.add(db_user)
    db.commit()
    return db_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


def get_user_rooms(db:Session, user_id): 
    user = get_user_by_id(db, user_id)
    print(user.all_rooms)
    return user.all_rooms