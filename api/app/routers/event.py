from sqlalchemy.orm import Session
from app import models
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.models as models
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.event import Event, EventCreate, EventOrderBy
import app.crud.event as crud_event


router: APIRouter = APIRouter(
    prefix="/event",
    tags=["Events"],
)

@router.get("/", response_model=list[Event], tags=["Events"])
async def get_events(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: EventOrderBy = EventOrderBy.id,
    reverse_order: bool = False,
):
    """
    Find all events
    """
    res = crud_event.get_all_event(db, limit, offset, order_by, reverse_order)
    if res is None:
        raise HTTPException(status_code=404, detail="No event found")
    return res