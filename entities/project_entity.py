from datetime import date

from entities.user_entity import UserEntity
from roles.rol import Rol

class ProjectEntity:
    def __init__(self, id: int, title: str, description: str,
                 active : bool, start_date: date, end_date: date = None, user: UserEntity = None):
        self.__id : int = id if id == None else id
        self.__title: int = title
        self.__description : str = description
        self.__active : bool = active #si se intancia activo es por mostrarlo en el catalogo pero debe pasar a validacion
        self.__start_date: date = start_date
        self.__end_date: date = end_date
        self.__user : UserEntity = user
        
    def assignUserCreate(self, user: UserEntity) -> None:
        if not isinstance(user, UserEntity):
            raise TypeError("Debe ser un usuario")
        if user.getRole() not in [Rol.student, Rol.exEntity, Rol.admin]:
            raise ValueError("No tienes permisos para crear un proyecto.")
        self.__user = user

    def getId(self) -> int:
        return self.__id

    def getTitle(self) -> str:
        return self.__title

    def getDescription(self) -> str:
        return self.__description

    def isActive(self) -> bool:
        return self.__active

    def getStartDate(self) -> date:
        return self.__start_date

    def getEndDate(self) -> date:
        return self.__end_date

    def getUser(self) -> UserEntity:
        return self.__user