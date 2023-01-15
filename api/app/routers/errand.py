from sqlalchemy.orm import Session
from app import models
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.models as models
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.errand import Errand, ErrandCreate, ErrandOrderBy
import app.crud.errand as crud_errand


router: APIRouter = APIRouter(
    prefix="/errand",
    tags=["Errands"],
)

@router.get("/", response_model=list[Errand], tags=["Errands"])
async def get_errands(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: ErrandOrderBy = ErrandOrderBy.id,
    reverse_order: bool = False,
):
    """
    Find all errands
    """
    res = crud_errand.get_all_errands(db, limit, offset, order_by, reverse_order)
    if res is None:
        raise HTTPException(status_code=404, detail="No errand found")
    return res

@router.put("/{", response_model=Errand, tags=["Errands"])
async def new_errand(
    errand: ErrandCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new errand
    """
    try:
        res = crud_errand.create_errand(db, errand)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating an errand ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.delete("/{errand_id}", response_model=bool, tags=["Errands"])
async def delete_errand(
    errand_id: int, db: Session = Depends(get_db)
):
    """
    Delete an errand from the database
    """
    crud_errand.delete_errand(db, errand_id)
    return True