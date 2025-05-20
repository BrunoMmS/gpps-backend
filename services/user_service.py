# services/user_service.py
from sqlalchemy.orm import Session
from cruds.UserDAO import UserDAO
from schema.user_schema import UserCreate, UserLogin, User
from entities.user_entity import UserEntity
from models.user_model import UserModel

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def registrar_usuario(self, db: Session, user_data: UserCreate) -> User:
        if self.dao.get_by_email(db, user_data.email):
            raise ValueError("Email ya registrado")

        user_model = self.dao.create(db, user_data)
        return self.__to_schema(user_model)

    def autenticar_usuario(self, db: Session, credentials: UserLogin) -> User:
        user_model = self.dao.authenticate(db, credentials)
        if not user_model:
            raise ValueError("Credenciales inválidas")

        return self.__to_schema(user_model)

    def listar_usuarios(self, db: Session) -> list[User]:
        user_models = self.dao.list(db)
        return [self.__to_schema(user) for user in user_models]

    def __to_schema(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            lastname=user_model.lastname,
            email=user_model.email,
            role=user_model.role
        )
