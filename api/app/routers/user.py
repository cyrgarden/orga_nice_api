from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.auth as auth
from app.router_utils import get_db, get_current_user, logger, error_to_status_code
from app.crud.utils import is_mail_valid, is_password_valid
from app.schemas.user import User, UserCreate, UserSubscribe
from app.schemas.room import Room, RoomCreate
from app.schemas.new_password import NewPasswordBase
import app.crud.user as crud_user
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

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

@router.get("/{user_id}/rooms", response_model=list[Room], tags=["Auth"])
async def get_user_rooms(user_id:int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    rooms = crud_user.get_user_rooms(db, user_id)
    if rooms is None:
        raise HTTPException(status_code=404, detail="Rooms not found")
    return rooms



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
    new_user: UserSubscribe,
    db: Session = Depends(get_db),
):

    if not is_password_valid(new_user.password) :
        raise HTTPException(
            status_code=400, detail="Mot de passe n'est pas valide. Il doit faire au minimum 9 caracteres."
        )

    if not is_mail_valid(new_user.mail) :
        raise HTTPException(
            status_code=400, detail="Votre adresse mail est invalide"
        )
    
    if crud_user.get_user_by_mail(db, new_user.username) is not None :
        raise HTTPException(
            status_code=400, detail="Ce mail est déjà pris."
        )

    if crud_user.get_user(db, new_user.username) is not None :
        raise HTTPException(
            status_code=400, detail="Ce pseudo existe déjà."
        )
    
    
    db_user = crud_user.new_user(
            db,
            new_user.username,
            auth.get_password_hash(new_user.password),
            new_user.mail,
            new_user.admin,
    )
    return db_user
   

@router.get("/me", response_model=User, tags=["Auth"])
async def read_users_me(user=Depends(get_current_user)):
    user.password = None
    return user


@router.post("/add_img/{user_id}")
async def add_img(user_id: int, img: UploadFile = File(...),db: Session = Depends(get_db)):
    FILEPATH = './static/'
    pimage_name = FILEPATH + img.filename
    print(pimage_name)
    content = await img.read()
    with open(pimage_name, 'wb') as f:
        f.write(content)
        await img.close()
    
    print(os.listdir(os.curdir)) 
    print(os.listdir('./static')) 
    file_url = 'http://45.155.169.59/' + pimage_name[1:]
    print(file_url)

    res = crud_user.add_img(db, user_id, file_url)

    return True


@router.get("/get_img/{user_id}")
async def get_img(user_id: int,db: Session = Depends(get_db)):
    print("ROUTER PART: ")
    print(os.path.exists('./static/test_img.jpg'))
    print(os.listdir(os.curdir)) 
    res = crud_user.get_img(db, user_id)
    print(os.listdir(os.curdir))    
    
    return FileResponse(res)
    

