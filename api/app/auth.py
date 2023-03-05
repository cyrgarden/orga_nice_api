import os
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from jose import jwt  # type: ignore
from passlib.context import CryptContext  # type: ignore
from pydantic import BaseModel
import app.crud.user as crud_user
import app.crud.pending_password as crud_new_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        default=30,
    )
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud_user.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def authenticate_user_bis(db, username: str, password: str):
    user = crud_user.get_user(db, username)
    if not user:
        return False
    
    new_password = crud_new_password.get_pending_password_by_user_id(db, user.id)
    if not new_password :
        return False
    
    print("veryying bis password")
    if not verify_password(password, new_password.new_password):
        return False
    
    user.password = new_password.new_password
    db.commit()
    db.refresh(user)
    crud_new_password.delete_pending_password(db, new_password.id)
    return user



def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
