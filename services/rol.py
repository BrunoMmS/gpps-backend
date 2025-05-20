from enum import Enum

class Rol(str, Enum):
    student = "Student"
    exEntity = "ExternalEntity"
    teacher = "Teacher_UNRN"
    teacher2 = "ExternalTeacher"
    admin = "Administrator"