from enum import Enum

class Rol(str, Enum):
    student = "Estudiante"
    exEntity = "Entidad_Externa"
    teacher = "Tutor_UNRN"
    teacher2 = "Tutor_Externo"