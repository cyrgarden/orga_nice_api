from sqlalchemy.orm import Session
from app import models
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.models as models
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.pending_password import PendingPassword, PendingPasswordCreate
import app.crud.pending_password as crud_new_password


router: APIRouter = APIRouter(
    prefix="/pending_password",
    tags=["PendingPassword"],
)


@router.put("/{user_mail}", response_model=PendingPassword, tags=["PendingPassword"])
async def new_pending_password(
    user_mail :str,
    new_pending_password : PendingPasswordCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new event
    """
    try:
        res = crud_new_password.create_event(db, user_mail, new_pending_password)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating an event ")
        return res
    except Exception as e:
        raise error_to_status_code(e)

