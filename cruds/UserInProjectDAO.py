from models.user_in_project_model import UserInProjectModel
from sqlalchemy.orm import Session
from entities.user_in_project_entity import UserInProjectEntity

class UserInProjectDAO:
    def __init__(self ):
        pass
    def create(self, db: Session, user_in_project: UserInProjectEntity) -> UserInProjectModel:
        db_user_in_project = UserInProjectModel(
            user_id=user_in_project.getUser().getId(),
            project_id=user_in_project.getProject().getId()
        )
        db.add(db_user_in_project)
        db.commit()
        db.refresh(db_user_in_project)
        return db_user_in_project
    #obtener el usuario en algun proyecto sin importar el proyecto
    def get_by_user_id(self, db: Session, user_id: int) -> UserInProjectModel | None:
        return db.query(UserInProjectModel).filter(UserInProjectModel.user_id == user_id).first()