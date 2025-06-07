from sqlalchemy.orm import Session
from cruds.UserDAO import UserDAO
from schemas.user_schema import UserCreate, UserLogin, User
from entities.user_entity import UserEntity
from models.user_model import UserModel
from entities.project_entity import ProjectEntity
from roles.rol import Rol

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

        return self.__to_schema(self.to_entity(user_model))

    def autenticar_usuario(self, db: Session, credentials: UserLogin) -> User:


        user_model = self.dao.authenticate(db, credentials.email, credentials.password)
        if not user_model:
            raise ValueError("Credenciales inválidas")
        
        return self.__to_schema(self.to_entity(user_model))

    def listar_usuarios(self, db: Session) -> list[User]:
        user_models = self.dao.list(db)
        return [self.__to_schema(self.to_entity(user)) for user in user_models]

    def get_user_by_id(self, db: Session, user_id: int) -> User: # Era UserCreate
        user_model = self.dao.get_by_id(db, user_id)
        if not user_model:
            raise ValueError("Usuario no encontrado")
        
        return self.__to_schema(self.to_entity(user_model))
    
    def to_entity(self, user_model: UserModel) -> UserEntity:
        return UserEntity(
            id=user_model.id,
            password=user_model.password,
            username=user_model.username,
            lastname=user_model.lastname,
            email=user_model.email,
            role=user_model.role
        )

    def __to_schema(self, user_entity: UserEntity) -> User: # Era UserCreate
        return UserCreate(
            id=user_entity.getId(),
            password=user_entity.getPassword(),
            username=user_entity.getUsername(),
            lastname=user_entity.getLastname(),
            email=user_entity.getEmail(),
            role=user_entity.getRole()
        ) #SUGERENCIA: En un futuro quitar password=user_entity.getPassword() ya que no se deberia mostrar la contraseña al usuario

     
    def add_tutor(self, user_entity: UserEntity, project: ProjectEntity, tutor: UserEntity) -> None:
        # CORREGIDO - Use 'and' en lugar de 'or'
        if user_entity.role != Rol.admin and user_entity.role != Rol.exEntity:
            raise ValueError("No tienes permisos para agregar un tutor")
        
        # CORREGIDO - Use 'and' en lugar de 'or'
        if tutor.role != Rol.inteacher and tutor.role != Rol.exteacher:
            raise ValueError("No estas agregando un tutor")
        
        if project.tutor_id is not None:
            raise ValueError("El proyecto ya tiene un tutor asignado")
        
        project.tutor_id = tutor.id

    def project_aprove(self, user_entity: UserEntity, project: ProjectEntity) -> ProjectEntity:
        # CORREGIDO - Use la constante de Rol en lugar de string
        if user_entity.role != Rol.admin:
            raise ValueError("No tienes permisos para aprobar un proyecto")
        
        if project.active:
            raise ValueError("El proyecto ya fue aprobado")
        
        if project.tutor_id is None:
            raise ValueError("El proyecto no tiene tutor asignado")
        
        project.active = True
        return project
          