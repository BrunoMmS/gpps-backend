from pydantic import BaseModel

class Task(BaseModel):
    id : int
    description: str
    done: bool
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    description:str
    done: bool
