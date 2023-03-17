from sqlalchemy.orm import Session
from app import models
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.models as models
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.reco_indispo import RecoIndispo, RecoIndispoCreate
import app.crud.reco_indispo as crud_indispo


router: APIRouter = APIRouter(
    prefix="/reco_indispo",
    tags=["RecoIndispos"],
)

@router.put("/", response_model=RecoIndispo, tags=["RecoIndispos"])
async def create_indispo(
    new_indispo: RecoIndispoCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new event
    """
    try:
        res = crud_indispo.create_indispo(db,new_indispo )
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating an indispo ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.delete("/{indispo_id}", response_model=bool, tags=["RecoIndispos"])
async def delete_indispo(
    indispo_id: int, db: Session = Depends(get_db)
):
    """
    Delete an indispo from the database
    """
    crud_indispo.delete_indispo(db, indispo_id)
    return True