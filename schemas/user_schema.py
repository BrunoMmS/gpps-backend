from pydantic import BaseModel
#from services.rol import Rol

class User(BaseModel):
    id : int
    username: str
    lastname: str
    email: str
    role: str
    class Config:
        from_attributes = True

class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str