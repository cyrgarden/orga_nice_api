from sqlalchemy.orm import Session
from app import models
from app.crud.utils import send_mail
from app.schemas.pending_password import PendingPassword, PendingPasswordCreate
import app.crud.user as crud_user
from app import auth
import string
import random



def get_pending_password_by_user_id(db, user_id:int ):
    return db.query(models.PendingPassword).filter(models.PendingPassword.user_id == user_id).first()

    
def create_pending_password(db: Session, user_mail:str, pending_password : PendingPasswordCreate):
    #db_event = models.Event(**event.dict())
    user = crud_user.get_user_by_mail(db, user_mail)
    if user is None :
        return None
    
    new_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(9))
    db_new_pending_password = models.PendingPassword(**pending_password.dict())
    db_new_pending_password.user_id = user.id
    db_new_pending_password.new_password = auth.get_password_hash(new_password)
    print(db_new_pending_password.new_password)
    db.add(db_new_pending_password)
    db.commit()
    db.refresh(db_new_pending_password)
    
    send_mail(db,user_mail, "NEW PASSWORD REQUEST", "HERE IS YOUR NEW PASSWORD: {}".format(new_password) )
    return db_new_pending_password


def delete_pending_password(db: Session, pending_password_id: int):
    db_pending_password = db.query(models.PendingPassword).filter(models.PendingPassword.id == pending_password_id).first()
    if db_pending_password is None:
        return None
    db.delete(db_pending_password)
    db.commit()
    return db_pending_password

