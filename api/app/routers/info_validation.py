from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app import models
from app.crud.utils import get_all
from app.schemas.info_validation import InfoValidation, InfoValidationCreate
import app.crud.info_validation as crud_validation
import app.crud.user as crud_user

router: APIRouter = APIRouter(
    prefix="/validation",
    tags=["InfoValidation"],
)


@router.get("/{user_id}", response_model=list[InfoValidation], tags=["InfoValidation"])
async def get_info_validation(user_id: int, db: Session = Depends(get_db)):
    """
    Find validations by user_id
    """
    res = crud_validation.get_validations_by_user_id(db, user_id)
    if res is None:
        raise HTTPException(status_code=404, detail="No validations data found")
    return res


@router.put("/", response_model=InfoValidation, tags=["InfoValidation"])
async def new_info_validation(
    info_validation: InfoValidationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new validation info
    """
    try:
        res = crud_validation.create_validation(db, info_validation)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating this conso data")
        return res
    except Exception as e:
        raise error_to_status_code(e)



#Made to validate user infos (mail or phone)
@router.post("/validate_infos", response_model=bool, tags=["Auth"])
async def validate_infos(
    infos: InfoValidationCreate,
    db: Session = Depends(get_db),
    
):
    """
        Request to validate user's infos (mail or phone)
    """
    try:
        #Checking if this validation infos exists
        info_validation = crud_validation.get_validations_by_user_id_and_field(db, infos.user_id, infos.validation_field)
        if info_validation is None:
            raise HTTPException(status_code=404, detail="There is no such code in db")

        #Now we check if the code givent by user is the same that has been sent by mail/sms 
        if infos.validation_code == info_validation.validation_code :
            user = crud_user.get_user_by_id(db, infos.user_id)
            #We validate user mail or phone
            crud_user.validate_field(db, infos.validation_field, user)
            #We delete the validation info
            crud_validation.delete_info_validation(db, info_validation.id)
            return True
        return False 

    except Exception as e:
        raise error_to_status_code(e)
