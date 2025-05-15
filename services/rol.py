from enum import Enum


class Rol(str, Enum):
    student = "estudiante"
    exEntity = "EntidadExterna"
    teacher = "tutorUNRN"
    teacher2 = "tutorExterno"