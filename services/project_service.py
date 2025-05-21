from sqlalchemy.orm import Session
from cruds.UserInProjectDAO import UserInProjectDAO
from cruds.projectDAO import ProjectDAO
from cruds.workplanDAO import WorkPlanDAO
from cruds.activityDAO import ActivityDAO
from cruds.taskDAO import TaskDAO
from entities.project_entity import ProjectEntity
from entities.user_in_project_entity import UserInProjectEntity
from schema.project_schema import ProjectCreate
from schema.workplan_schema import WorkPlanCreate
from schema.activity_schema import ActivitieCreate
from schema.task_schema import Task
from models.project_model import ProjectModel
from services.rol import Rol
from services.user_service import UserService
from services.workplan_service import WorkPlanService


class ProjectService:
    def __init__(self):
        self.project_dao = ProjectDAO()
        self.workplan_dao = WorkPlanDAO()
        self.activity_dao = ActivityDAO()
        self.task_dao = TaskDAO()
        self.user_service = UserService()
        
    def crear_proyecto_completo(self, db: Session, data: ProjectCreate) -> ProjectModel:
        new_workplan = self.workplan_dao.create(db, WorkPlanCreate())
        for act in data.workplan.activities:
            activity_data = ActivitieCreate(
                name=act.name,
                duration=act.duration,
                workplan_id=new_workplan.id
            )
            self.activitie_dao.create(db, activity_data)

        for task in data.workplan.activities.tasks:
            task_data = Task(
                description=task.description,
                activity_id=task.activity_id
            )
            self.task_dao.create(db, task_data)

        project_data_dict = data.dict()
        project_data_dict["workplan_id"] = new_workplan.id
        return self.project_dao.create(db, ProjectCreate(**project_data_dict))

    def create_project(self, db: Session, project_data: ProjectCreate) -> ProjectModel:
        user = self.user_service.get_user_by_id(db, project_data.user_id)
        
        if not user:
            raise ValueError("Usuario no encontrado")
        
        userEntity = self.user_service.to_entity(user)
       
        project_data_dict = project_data.model_dump()
        project_entity = ProjectEntity(
            id=None,
            title=project_data_dict["title"],
            description=project_data_dict["description"],
            active=project_data_dict["active"],
            start_date=project_data_dict["start_date"],
            end_date=project_data_dict["end_date"]
        )
        project_entity.assignUserCreate(userEntity)
       
        return self.project_dao.create(db, project_entity)
    
    def add_workplan(self, db: Session,  workplan_data: WorkPlanCreate):
        workplan_service = WorkPlanService()
        return workplan_service.create_workplan(db,  workplan_data)
    
    def assign_user_to_project(self, db: Session, project_id: int, user_id: int, id_user_to_assign: int):
        project = self.project_dao.get_by_id(db, project_id)
        if not project:
            raise ValueError("Project not found")
        
        user = self.user_service.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        user_to_assign = self.user_service.get_user_by_id(db, id_user_to_assign)
        if not user_to_assign:
            raise ValueError("Usuario a asignar no encontrado")
        
        userEntity = self.user_service.to_entity(user)
        if userEntity.getRole() not in [Rol.exEntity, Rol.admin]:
            raise ValueError("No tienes permisos para asignar usuarios a este proyecto.")
        
        userToAssignEntity = self.user_service.to_entity(user_to_assign)
        projectEntity = ProjectEntity(
            id=project.id,
            title=project.title,
            description=project.description,
            active=project.active,
            start_date=project.start_date,
            end_date=project.end_date,
            user= self.user_service.to_entity(self.user_service.get_user_by_id(db, project.user_id))
        )
        
        user_to_project_entity = UserInProjectEntity(userToAssignEntity, projectEntity)
        user_to_project_dao = UserInProjectDAO()

        user_to_project_dao.create(db, user_to_project_entity)