from sqlalchemy.orm import Session
from app import models
from app.schemas.recommandation import Recommandation, RecommandationCreate, RecommandationOrderBy
import app.crud.recommandation as crud_reco
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.crud.room as crud_room
import app.models as models
from app.schemas.room import Room, RoomCreate
from app.schemas.user import User, UserCreate
from app.router_utils import get_db, get_current_user, logger, error_to_status_code


router: APIRouter = APIRouter(
    prefix="/recommandation",
    tags=["Recommandations"],
)

@router.get("/", response_model=list[Recommandation], tags=["Recommandations"])
async def get_recommandations(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: RecommandationOrderBy = RecommandationOrderBy.id,
    reverse_order: bool = False,
):
    """
    Find all recommandations
    """
    res = crud_reco.get_all_recommandation(db, limit, offset, order_by, reverse_order)
    if res is None:
        raise HTTPException(status_code=404, detail="No recommandation found")
    return res


@router.get("/filtered/", response_model=list[Recommandation], tags=["Recommandations"])
async def get_filtered_recommandations(
    db: Session = Depends(get_db),
    type: str = '',
    price: float = 100000.0,
    origin_city: str = '',
    maximum_distance: float = 100.0,
    indispo: str = '',
):
    """
    Find filtered recommandations
    """
    res = crud_reco.get_recommandations_filtered(db, type,price,origin_city, maximum_distance, indispo)
    if res is None:
        raise HTTPException(status_code=404, detail="No recommandation found")
    return res

@router.get("/filtered_subtype/", response_model=list[Recommandation], tags=["Recommandations"])
async def get_filtered_recommandations_by_subtype(
    db: Session = Depends(get_db),
    subtype: str = '',
):
    """
    Find filtered recommandations
    """
    res = crud_reco.get_recommandations_by_subtype(db, subtype)
    if res is None:
        raise HTTPException(status_code=404, detail="No recommandation found")
    return res


@router.put("/", response_model=Recommandation, tags=["Recommandations"])
async def new_recommandation(
    reco: RecommandationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new recommandation
    """
    try:
        res = crud_reco.create_recommandation(db, reco)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating a room ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.delete("/{recommandation_id}", response_model=bool, tags=["Recommandations"])
async def delete_recommandation(
    recommandation_id: int, db: Session = Depends(get_db)
):
    """
    Delete a recommandation from the database
    """
    crud_reco.delete_recommandation(db, recommandation_id)
    return True
