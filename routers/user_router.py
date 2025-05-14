from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict

from schema.user_schema import UserCreate, UserLogin

# Mock database and utility functions
users_db: Dict[str, Dict] = {}

def get_password_hash(password: str) -> str:
    return f"hashed_{password}"

def get_user(token: str):
    return users_db.get(token)

user_router = APIRouter()

@user_router.post("/users/register", response_model=UserCreate)
def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {
        "id": len(users_db) + 1,
        "username": user.username,
        "lastname": user.lastname,
        "email": user.email,
        "role": user.role,
        "hashed_password": hashed_password
    }

    return UserCreate(
        id=len(users_db),
        username=user.username,
        lastname=user.lastname,
        email=user.email,
        role=user.role,
        password=user.password
    )

@user_router.get("/users")
def list_users():
    return [{"username": user["username"], "role": user["role"]} for user in users_db.values()]


@user_router.post("/users/login")
def login(credentials: UserLogin):
    user = None
    for u in users_db.values():
        if u["email"] == credentials.email:
            user = u
            break

    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    hashed_input_password = get_password_hash(credentials.password)
    if user["hashed_password"] != hashed_input_password:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }