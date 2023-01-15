from sqlalchemy.orm import Session
from app import models
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import app.models as models
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.task import Task, TaskCreate, TaskOrderBy
import app.crud.task as crud_task


router: APIRouter = APIRouter(
    prefix="/task",
    tags=["Tasks"],
)

@router.get("/", response_model=list[Task], tags=["Tasks"])
async def get_Tasks(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    order_by: TaskOrderBy = TaskOrderBy.id,
    reverse_order: bool = False,
):
    """
    Find all Tasks
    """
    res = crud_task.get_all_tasks(db, limit, offset, order_by, reverse_order)
    if res is None:
        raise HTTPException(status_code=404, detail="No Task found")
    return res

@router.put("/", response_model=Task, tags=["Tasks"])
async def new_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new Task
    """
    try:
        res = crud_task.create_task(db, task)
        if res is None:
            raise HTTPException(status_code=404, detail="Error while creating an Task ")
        return res
    except Exception as e:
        raise error_to_status_code(e)


@router.delete("/{task_id}", response_model=bool, tags=["Tasks"])
async def delete_task(
    task_id: int, db: Session = Depends(get_db)
):
    """
    Delete an Task from the database
    """
    crud_task.delete_Task(db, task_id)
    return True