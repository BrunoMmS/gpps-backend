# services/user_service.py
from sqlalchemy.orm import Session
from cruds.UserDAO import UserDAO
from schema.user_schema import UserCreate, UserLogin
from models.user_model import UserModel

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def registrar_usuario(self, db: Session, user: UserCreate) -> UserModel:
        if self.dao.get_by_email(db, user.email):
            raise ValueError("Email ya registrado")
        return self.dao.create(db, user)

    def autenticar_usuario(self, db: Session, credentials: UserLogin) -> UserModel:
        user = self.dao.authenticate(db, credentials)
        if not user:
            raise ValueError("Credenciales inválidas")
        return user

    def listar_usuarios(self, db: Session) -> list[UserModel]:
        return self.dao.list(db)
