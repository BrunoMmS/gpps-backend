from enum import Enum


class Rol(str, Enum):
    user = "estudiante"
    admin = "administrador"
    teacher = "tutorUNRN"
    teacher2 = "tutorExterno"