from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.router_utils import get_db, error_to_status_code
from app.schemas.indisponibility import Indisponibility, IndisponibilityCreate
import app.crud.indisponibility as crud_indispo


class UserQuery(BaseModel):
    room_id: int
    date: str


router: APIRouter = APIRouter(
    prefix="/indispo",
    tags=["Indisponibilities"],
)


@router.put("/", response_model=Indisponibility, tags=["Indisponibilities"])
async def create_indispo(
    new_indispo: IndisponibilityCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new event
    """
    try:
        res = crud_indispo.create_indispo(db, new_indispo)
        if res is None:
            raise HTTPException(
                status_code=404, detail="Error while creating an indispo ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.post("/indispo_users", response_model=List[str], tags=["Indisponibilities"])
async def get_user_infos_by_room_and_date(user_query: UserQuery, db: Session = Depends(get_db)):
    res = crud_indispo.get_user_infos_by_room_and_date(
        db, user_query.room_id, user_query.date)
    if res == None:
        raise HTTPException(status_code=404, detail=" Can't fint this user")

    return res


@router.delete("/{indispo_id}", response_model=bool, tags=["Indisponibilities"])
async def delete_indispo(
    indispo_id: int, db: Session = Depends(get_db)
):
    """
    Delete an indispo from the database
    """
    crud_indispo.delete_indispo(db, indispo_id)
    return True
