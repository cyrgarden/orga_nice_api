from sqlalchemy.orm import Session
from api.app.crud.utils import get_all
from app import models
from app.schemas.task import Task, TaskCreate, TaskOrderBy
from app.schemas.user import User
import app.crud.event as crud_event


def create_task(db: Session, task: TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_all_tasks(
    db: Session,
    limit: int,
    offset: int,
    orderby: TaskOrderBy,
    reverse: bool,
):
    return get_all(db, models.Task, limit, offset, orderby, reverse, None)


def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return db_task


