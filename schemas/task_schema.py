from pydantic import BaseModel

class Task(BaseModel):
    id : int
    description: str
    done: bool

class TaskCreate(BaseModel):
    description:str
    done: bool
