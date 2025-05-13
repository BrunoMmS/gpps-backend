from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict

from schema.user_schema import UserCreate

# Mock database and utility functions
users_db: Dict[str, Dict] = {}

def get_password_hash(password: str) -> str:
    return f"hashed_{password}"

def get_user(token: str):
    return users_db.get(token)

user_router = APIRouter()

@user_router.post("/register", response_model=UserCreate)
def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = {"username": user.username, "hashed_password": hashed_password, "role": user.role}
    return UserCreate(username=user.username, role=user.role)

@user_router.get("/users")
def list_users():
    return [{"username": user["username"], "role": user["role"]} for user in users_db.values()]