from entities.project_entity import ProjectEntity
from entities.user_entity import UserEntity
from roles.rol import Rol

class UserInProjectEntity:
    def __init__(self, user_entity: UserEntity, project_entity: ProjectEntity, id: int = None):
        if not isinstance(user_entity, UserEntity):
            raise TypeError("user_entity debe ser una instancia de UserEntity")
        
        if not isinstance(project_entity, ProjectEntity):
            raise TypeError("project_entity debe ser una instancia de ProjectEntity")
        
        if user_entity.getRole() not in [Rol.student, Rol.teacher, Rol.teacher2]:
            raise ValueError("No se puede asignar un usuario que no sea estudiante o profesor a un proyecto")
        self.__id = id
        self.__user_entity = user_entity
        self.__project_entity = project_entity

    def getUser(self) -> UserEntity:
        return self.__user_entity

    def getProject(self) -> ProjectEntity:
        return self.__project_entity

    def getId(self) -> int:
        return self.__id