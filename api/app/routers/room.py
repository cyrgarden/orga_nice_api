from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
import app.crud.room as crud_room
from app.schemas.room import Room, RoomCreate
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router: APIRouter = APIRouter(
    prefix="/room",
    tags=["Rooms"],
)


@router.put("/{user_id}", response_model=Room, tags=["Rooms"])
async def new_room(
    user_id: int,
    room: RoomCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Create a new room
    """
    try:
        res = crud_room.create_room(db, room, user_id)
        if res is None:
            raise HTTPException(
                status_code=404, detail="Error while creating a room ")
        logger(db, user, f"Created room {room.label}")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.post("/{user_id}/join_room/{invite_link}", response_model=Room, tags=["Rooms"])
async def add_user_to_room(
    user_id: int,
    invite_link: str,
    db: Session = Depends(get_db),
):
    """
    Create a new room
    """
    try:
        res = crud_room.add_user(db, user_id, invite_link)
        if res is None:
            raise HTTPException(
                status_code=404, detail="Error while creating a room ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.get("/{room_id}/users", tags=["Rooms"])
async def get_room_users(room_id: int, db: Session = Depends(get_db)):
    users = crud_room.get_room_users(db, room_id)
    users_infos = []
    for user in users:
        users_infos.append({'user_id': user.id, 'username': user.username,
                           'mail': user.mail, 'all_events': user.all_events, 'img_url': user.img})

    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    to_return = jsonable_encoder(users_infos)
    return JSONResponse(content=to_return)


@router.get("/", response_model=List[Room])
def get_all_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rooms = crud_room.get_all_rooms(db)
    return rooms


@router.get("/{room_id}", response_model=Room)
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
    db_room = crud_room.get_room_by_id(db, room_id=room_id)

    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@router.delete("/{room_id}", response_model=bool, tags=["Events"])
async def delete_event(
    room_id: int, db: Session = Depends(get_db)
):
    """
    Delete a room from the database
    """
    crud_room.delete_event(db, room_id)
    return True
