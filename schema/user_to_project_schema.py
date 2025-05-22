from pydantic import BaseModel


class UserToProjectCreate(BaseModel):
    user_id: int
    project_id: int
