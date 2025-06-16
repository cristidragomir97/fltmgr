from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import select
from passlib.hash import bcrypt
import jwt
import datetime

from app.database_models import User, get_session

SECRET_KEY = "secret"

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register", response_model=User)
def register(user: UserCreate):
    with get_session() as session:
        exists = session.exec(select(User).where(User.username == user.username)).first()
        if exists:
            raise HTTPException(status_code=409, detail="User exists")
        new_user = User(
            id=str(datetime.datetime.utcnow().timestamp()),
            username=user.username,
            email=user.email,
            password_hash=bcrypt.hash(user.password),
            is_admin=False,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

@router.post("/login")
def login(data: LoginRequest):
    with get_session() as session:
        user = session.exec(select(User).where(User.username == data.username)).first()
        if not user or not bcrypt.verify(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        payload = {
            "sub": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
