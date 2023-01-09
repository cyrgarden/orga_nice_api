from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.auth as auth
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.schemas.user import User, UserCreate
import app.crud.user as crud_user

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Auth"],
)


@router.get("/", response_model=list[User], tags=["Auth"])
async def get_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user.admin:
        users = crud_user.get_all_users(db)
        for user in users:
            user.password = None
        return users
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )


@router.delete("/{user_id}", response_model=bool, tags=["Auth"])
async def delete_user(
    user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if user.admin:
        crud_user.delete_user(db, user_id=user_id)
        logger(db, user, f"Deleted user {user_id}")
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )


@router.put("/", response_model=User, tags=["Auth"])
async def add_user(
    new_user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        db_user = crud_user.new_user(
            db,
            new_user.username,
            auth.get_password_hash(new_user.password),
            new_user.admin,
            )
        logger(db, user, f"Added user {db_user.id}")
        return db_user
    except Exception as e:
        raise error_to_status_code(e)
   

@router.get("/me", response_model=User, tags=["Auth"])
async def read_users_me(user=Depends(get_current_user)):
    user.password = None
    return user
