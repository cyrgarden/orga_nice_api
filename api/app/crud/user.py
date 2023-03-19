from sqlalchemy.orm import Session
from app import models
from app.schemas.room import RoomCreate
from app.crud.utils import send_mail
import os



def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def new_user(db: Session, user: str, password: str, mail_adress: str, is_admin: bool):
    print("CRUD : ")
    db_user = models.User(username=user, password=password, admin=is_admin, mail = mail_adress)
    db.add(db_user)
    db.commit()
    return db_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_mail(db: Session, user_mail: str):
    return db.query(models.User).filter(models.User.mail == user_mail).first()

def reset_password_one(db: Session, user_mail:str):
    user = get_user_by_mail(db, user_mail)
    if user is None :
        return None
    send_mail(db, user_mail, "NEW PASSWORD REQUEST", "new_password")
    
def reset_password_two(db: Session, user_id :int, new_password : str):
    user = get_user_by_id(db, user_id)
    

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


def get_user_rooms(db:Session, user_id:int): 
    user = get_user_by_id(db, user_id)
    if user is None : 
        return None
    print(user.all_rooms)
    return user.all_rooms

def validate_field(db:Session, field: str, user): 
    print("IN CRUD")
    if field == 'mail' :
        user.mail_confirmed = True
    
    else : 
        print("not good")
        return None

    print(user.mail_confirmed)
    db.commit()
    db.refresh(user)
    return user



def add_img(db:Session, user_id:int, img_url):
    print(img_url)
    user = get_user_by_id(db, user_id)
    print(user.username)
    user.img = img_url
    db.commit()
    db.refresh(user)
    return user

def get_img(db:Session, user_id:int):
    print(os.getcwd())
    print(os.listdir(os.curdir)) 
    print(os.listdir('./static'))
    print(os.listdir('./static/'))   
    print(os.path.exists('./static'))
    print(os.path.exists('../static'))
    user = get_user_by_id(db, user_id)
    return './static/test_img.jpg'


