import re

from services.rol import Rol

class UserEntity:
    def __init__(self, id: int, username: str, password: str, lastname: str, 
                 email: str, role: str):
        if not isinstance(id, int) or id < 0:
            raise ValueError("ID debe ser un entero positivo.")

        if not username or not username.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        
        if not lastname or not lastname.strip():
            raise ValueError("El apellido no puede estar vacío.")

        if not self.__is_valid_email(email):
            raise ValueError("El email no tiene un formato válido.")

        if role not in [Rol.admin, Rol.student, Rol.teacher, Rol.teacher2, Rol.exEntity]:
            raise ValueError(f"Rol inválido: {role}")
        
        self.__password : str = password
        self.__id: int = id
        self.__username: str = username
        self.__lastname: str = lastname
        self.__email: str = email
        self.__role: str = role

    def __is_valid_email(self, email: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def getUsername(self) -> str:
        return self.__username
    
    def getLastname(self) -> str:
        return self.__lastname
    
    def getEmail(self) -> str:
        return self.__email

    def getRole(self) -> str:
        return self.__role

    def getId(self) -> int:
        return self.__id
    
    def getPassword(self) -> str:
        return self.__password


