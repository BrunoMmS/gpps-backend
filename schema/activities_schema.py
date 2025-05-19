from pydantic import BaseModel
class activities(BaseModel):
    name: str
    duration: int
    id: int
    done: bool
