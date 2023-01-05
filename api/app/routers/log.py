from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.router_utils import get_db, get_current_user
from app.schemas.log import Log, LogsOrderBy
import app.crud.log as crud_log


router: APIRouter = APIRouter(
    prefix="/logs",
    tags=["Logs"],
)


@router.get("/logs", response_model=list[Log], tags=["Logs"])
def get_logs(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: LogsOrderBy = LogsOrderBy.timestamp,
    reverse: bool = False,
    user=Depends(get_current_user),
):
    return crud_log.get_logs(
        db, offset=offset, limit=limit, orderby=order_by, reverse=reverse
    )


@router.delete("/logs", response_model=bool, tags=["Logs"])
def delete_logs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.is_admin:
        crud_log.clear_logs(db)
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
