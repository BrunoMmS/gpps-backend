from pydantic import BaseModel
class tasks(BaseModel):
    id : int
    description: str
    done: bool
