from sqlalchemy.orm import Session
from models.project_model import ProjectModel
from schema.project_schema import ProjectCreate

class ProjectDAO:
    def get_by_id(self, db: Session, project_id: int) -> ProjectModel | None:
        return db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    def list(self, db: Session) -> list[ProjectModel]:
        return db.query(ProjectModel).all()

    def create(self, db: Session, project_data: ProjectCreate) -> ProjectModel:
        db_project = ProjectModel(**project_data.model_dump())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project