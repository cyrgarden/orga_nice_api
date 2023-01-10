from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.crud.room as crud_room
import app.models as models
import app.schemas.room as schemas
from app.router_utils import get_db


router: APIRouter = APIRouter(
    prefix="/room",
    tags=["Rooms"],
)

@router.put("/", response_model=Room, tags=["Room"])
async def new_prise(
    room: RoomCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Create a new room
    """
    try:
        res = crud_room.create_room(db, room)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating a room ")
        logger(db, user, f"Created gpu {prise.label}")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.get("/room/", response_model=List[schemas.Room])
def get_all_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud.get_all_rooms(db, skip=skip, limit=limit)
    return rooms


@router.get("/rooms/{room_id}", response_model=schemas.Room)
def read_user(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room_by_id(db, room_id=room_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
