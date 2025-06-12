from enum import Enum

class Rol(str, Enum):
    student = "Student"
    exEntity = "ExternalEntity"
    inteacher = "Teacher_UNRN"
    exteacher = "ExternalTeacher"
    admin = "Administrator"