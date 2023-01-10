from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.crud.room as crud_room
import app.models as models
from app.schemas.room import Room, RoomCreate
from app.router_utils import get_db, get_current_user, logger, error_to_status_code

router: APIRouter = APIRouter(
    prefix="/room",
    tags=["Rooms"],
)

@router.put("/", response_model=Room, tags=["Rooms"])
async def new_room(
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
        logger(db, user, f"Created room {room.label}")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.get("/room/", response_model=List[Room])
def get_all_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud_room.get_all_rooms(db)
    return rooms


@router.get("/rooms/{room_id}", response_model=Room)
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    db_room = crud_room.get_room_by_id(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
