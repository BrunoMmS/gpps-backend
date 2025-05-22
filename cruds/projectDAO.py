from sqlalchemy.orm import Session
from entities.project_entity import ProjectEntity
from models.project_model import ProjectModel
from schema.project_schema import ProjectCreate
from typing import List, Optional

class ProjectDAO:
    def get_by_id(self, db: Session, project_id: int) -> ProjectModel | None:
        return db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    def list(self, db: Session) -> list[ProjectModel]:
        return db.query(ProjectModel).all()
    
    def list_by_user(self, db: Session, idUser: int) -> Optional[List[ProjectModel]]:
        return db.query(ProjectModel).filter(ProjectModel.user_id == idUser).all()
    
    def create(self, db: Session, project_data: ProjectEntity) -> ProjectModel:
        db_project = ProjectModel(
            id=project_data.getId(),
            title=project_data.getTitle(),
            description=project_data.getDescription(),
            active=project_data.isActive(),  
            start_date=project_data.getStartDate(),
            end_date=project_data.getEndDate(),
            user_id=project_data.getUser().getId()
        )

        db.add(db_project)
        db.commit()
        db.refresh(db_project)

        return db_project