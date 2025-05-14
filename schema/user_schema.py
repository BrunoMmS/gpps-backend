from pydantic import BaseModel

#from services.rol import Rol


class User(BaseModel):
    id : int
    username: str
    lastname: str
    email: str
    role: str

class UserCreate(User):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str