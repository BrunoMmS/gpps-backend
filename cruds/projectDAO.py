from operator import or_
from sqlalchemy.orm import Session, joinedload
from entities.project_entity import ProjectEntity
from models.project_model import ProjectModel
from models.user_in_project_model import UserInProjectModel
from schemas.project_schema import ProyectComplete
from typing import List, Optional
from models.workplan_model import WorkPlan
from models.activity_model import ActivityModel
from models.task_model import TaskModel
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
    def update(self, db: Session, project_data: ProjectEntity) -> ProjectModel:
        db_project = db.query(ProjectModel).filter(ProjectModel.id == project_data.getId()).first()

        if not db_project:
            raise Exception("Project not found")

        db_project.title = project_data.getTitle()
        db_project.description = project_data.getDescription()
        db_project.active = project_data.isActive()
        db_project.start_date = project_data.getStartDate()
        db_project.end_date = project_data.getEndDate()
        db_project.user_id = project_data.getUser().getId()

        db.commit()
        db.refresh(db_project)

        return db_project
    
    def get_proyect_complete(self,db: Session, proyect_id: int) -> Optional[ProyectComplete]:
        proyect = (
        db.query(ProjectModel)
        .options(
            joinedload(ProjectModel.workplan)
            .joinedload(WorkPlan.activities)
            .joinedload(ActivityModel.tasks),
            joinedload(ProjectModel.creator)
        )
        .filter(ProjectModel.id == proyect_id )
        .first()
    )
        if not proyect:
          return None
        proyect_complete = ProyectComplete.from_orm(proyect)
        proyect_complete.creator = proyect.creator
        return proyect_complete
    
    def get_projects_complete_by_user(self, db: Session, user_id: int) -> List[ProyectComplete]:
        proyectos = (
          db.query(ProjectModel)
           .options(
            joinedload(ProjectModel.workplan)
            .joinedload(WorkPlan.activities)
            .joinedload(ActivityModel.tasks),
            joinedload(ProjectModel.creator)
            )
            .filter(
                or_(
                ProjectModel.user_id == user_id,
                ProjectModel.users.any(UserInProjectModel.user_id == user_id)
                )
            )
        .all()
        )
        return [ProyectComplete.from_orm(proy) for proy in proyectos]