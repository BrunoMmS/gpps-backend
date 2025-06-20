from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserLogin, User
from services.user_service import UserService
from db.db import SessionLocal

user_router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = user_service.registrar_usuario(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_user

@user_router.post("/login", response_model=User)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = user_service.autenticar_usuario(db, credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    return user

@user_router.get("/", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return user_service.listar_usuarios(db)

@user_router.get("/{idUser}", response_model=User)
def get_user_by_id(idUser: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_id(db, idUser)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))