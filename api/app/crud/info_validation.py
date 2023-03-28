from sqlalchemy.orm import Session
from app import models
from app.crud.utils import send_mail
from app.schemas.info_validation import InfoValidationCreate
import app.crud.user as crud_user
import string
import random
import time
import datetime


def get_validations_by_user_id(db: Session, user_id: int):
    return db.query(models.InfoValidation).filter(models.InfoValidation.user_id == user_id).all()


# Create a validation_info
def create_validation(db: Session, info_validation: InfoValidationCreate):
    # We check if one already exist. If it does, we delete it so it will be replaced by a new one
    existing_validation = get_validations_by_user_id_and_field(
        db, info_validation.user_id, info_validation.validation_field)
    if existing_validation:
        delete_info_validation(db, existing_validation.id)

    db_info_validation = models.InfoValidation(**info_validation.dict())

    # Random validation code generation
    db_info_validation.validation_code = ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(6))

    # Generate the current timsestamp
    now = time.time()
    current_GMT = time.gmtime(now)
    timestamp = datetime.datetime(current_GMT.tm_year, current_GMT.tm_mon, current_GMT.tm_mday,
                                  current_GMT.tm_hour, current_GMT.tm_min, tzinfo=datetime.timezone.utc).timestamp()
    db_info_validation.timestamp = timestamp

    db.add(db_info_validation)
    db.commit()
    db.refresh(db_info_validation)

    user = crud_user.get_user_by_id(db, info_validation.user_id)

    # If it's 'mail' we send a mail
    if info_validation.validation_field == 'mail':
        send_mail(db, user.mail, "VALIDATION CODE",
                  "Your code is {}".format(db_info_validation.validation_code))
        return db_info_validation

    return db_info_validation


def get_validations_by_user_id_and_field(db: Session, user_id: int, validation_field: str):
    return db.query(models.InfoValidation).filter(models.InfoValidation.user_id == user_id).filter(models.InfoValidation.validation_field == validation_field).first()


def delete_info_validation(db: Session, validation_id: int):
    db_info_validation = db.query(models.InfoValidation).filter(
        models.InfoValidation.id == validation_id).first()
    if db_info_validation is None:
        return None
    db.delete(db_info_validation)
    db.commit()
    return db_info_validation


def clean_info_validation(db: Session, limit_timestamp):
    db.query(models.InfoValidation).filter(
        int(models.InfoValidation.timestamp) <= limit_timestamp).delete()
