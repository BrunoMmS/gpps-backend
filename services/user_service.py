from sqlalchemy.orm import Session
from cruds.UserDAO import UserDAO
from schema.user_schema import UserCreate, UserLogin, User
from entities.user_entity import UserEntity
from models.user_model import UserModel

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def registrar_usuario(self, db: Session, user_data: UserCreate) -> User:
        user_entity = UserEntity(
            id=user_data.id,
            username=user_data.username,
            lastname=user_data.lastname,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role
        )

        if self.dao.get_by_email(db, user_entity.getEmail()):
            raise ValueError("Email ya registrado")

        user_model = self.dao.create(db, user_entity)

        return self.__to_schema(self.__to_entity(user_model))

    def autenticar_usuario(self, db: Session, credentials: UserLogin) -> User:
        user_entity = UserEntity(
            email=credentials.email,
            password=credentials.password
        )

        user_model = self.dao.authenticate(db, user_entity)
        if not user_model:
            raise ValueError("Credenciales inválidas")
        
        return self.__to_schema(self.__to_entity(user_model))

    def listar_usuarios(self, db: Session) -> list[User]:
        user_models = self.dao.list(db)
        return [self.__to_schema(self.__to_entity(user)) for user in user_models]

    def __to_entity(self, user_model: UserModel) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            password=user_model.password,
            username=user_model.username,
            lastname=user_model.lastname,
            email=user_model.email,
            role=user_model.role
        )

    def __to_schema(self, user_entity: UserEntity) -> User:
        return User(
            id=user_entity.getId(),
            username=user_entity.getUsername(),
            lastname=user_entity.getLastname(),
            email=user_entity.getEmail(),
            role=user_entity.getRole()
        )
