from sqlalchemy.orm import Session
from cruds.UserInProjectDAO import UserInProjectDAO
from cruds.projectDAO import ProjectDAO
from cruds.workplanDAO import WorkPlanDAO
from cruds.activityDAO import ActivityDAO
from cruds.taskDAO import TaskDAO
from entities.project_entity import ProjectEntity
from entities.user_in_project_entity import UserInProjectEntity
from schemas.project_schema import ProjectCreate, ProyectComplete, ProjectWithUser
from schemas.workplan_schema import WorkPlanCreate
from models.project_model import ProjectModel
from services.notification_service import NotificationService
from roles.rol import Rol
from services.user_service import UserService
from services.workplan_service import WorkPlanService

class ProjectService:
    def __init__(self):
        self.project_dao = ProjectDAO()
        self.workplan_service = WorkPlanService()
        self.user_service = UserService()
        
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
    
    
    def add_workplan(self, db: Session, user_id: int, workplan_data: WorkPlanCreate):
        return self.workplan_service.create_workplan(db, user_id, workplan_data)
    def list_projects(self, db: Session) -> list[ProjectModel]:
        projects = self.project_dao.list(db)
        return projects
    
    def list_projects_by_user(self, idUser: int, db: Session) -> list[ProjectModel]:
        projects = self.project_dao.list_by_user(db, idUser)
        return projects
    
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
        
        user_to_assign_entity = self.user_service.to_entity(user_to_assign)
        
        userEntity = self.user_service.to_entity(user)
        if userEntity.getRole() not in [Rol.exteacher, Rol.inteacher, Rol.student]:
            raise ValueError("No tienes permisos para asignar usuarios a este proyecto.")
        
        if user_to_assign_entity.getRole() not in [Rol.student]:
            raise ValueError("El usuario a asignar debe ser un estudiante.")
        
        user_in_project_dao = UserInProjectDAO()
        existing_user_in_project = user_in_project_dao.get_by_user_id(db, user_to_assign.id)
        if existing_user_in_project:
            raise ValueError("El usuario ya esta asignado a un proyecto.")
        
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
        notification_service = NotificationService(db)
        notification_service.notify(user_to_assign.id, f"Has sido asignado al proyecto {project.title} por {user.username}")

    def approve_project(self, db: Session, project_id: int) -> ProjectModel:
        project = self.project_dao.get_by_id(db, project_id)
        
        if not project:
            raise ValueError("Project not found")

        project_entity = ProjectEntity(
            id=project.id,
            title=project.title,
            description=project.description,
            active=True,  
            start_date=project.start_date,
            end_date=project.end_date,
            user=self.user_service.to_entity(self.user_service.get_user_by_id(db, project.user_id))
        )
        self.project_dao.update(db, project_entity)

        notification_service = NotificationService(db)
        notification_service.notify(project.user_id, f"Tu proyecto {project.title} ha sido aprobado.")
        return project
    
    def get_complete_project(self, db: Session, proyect_id: int) -> ProyectComplete:
        project_model = self.project_dao.get_proyect_complete(db, proyect_id)

        if not project_model:
            raise ValueError("Proyecto no encontrado")

        return ProyectComplete.model_validate(project_model)
    
    def get_complete_project_by_user(self, db: Session, user_id: int) -> list[ProyectComplete]:
        project_model = self.project_dao.get_projects_complete_by_user(db, user_id)

        if not project_model:
            raise ValueError("El usuario no esta adjunto a ningun proyecto")

        return [ProyectComplete.model_validate(proy) for proy in project_model]
    
    def get_project_with_user(self, db: Session, project_id: int) -> ProjectWithUser:
        project = self.project_dao.get_by_id(db, project_id)
        
        if not project:
            raise ValueError("Project not found")
        
        user = self.user_service.get_user_by_id(db, project.user_id)
        if not user:
            raise ValueError("User not found")
        
        return ProjectWithUser(
            id=project.id,
            title=project.title,
            description=project.description,
            active=project.active,
            start_date=project.start_date,
            end_date=project.end_date,
            user=self.user_service.get_user_by_id(db, user.id)
        )
    
    def get_projects_with_user(self, db: Session, user_id: int) -> list[ProjectWithUser]:
        user = self.user_service.get_user_by_id(db, user_id)
        projects = self.project_dao.list_by_user(db, user_id)
 
        projects_schemas: list[ProjectWithUser]  = []
 
        for project in projects:
            projects_schemas.append(ProjectWithUser(
            id=project.id,
            title=project.title,
            description=project.description,
            active=project.active,
            start_date=project.start_date,
            end_date=project.end_date,
            user=user
        ))
        
        return projects_schemas
    
    def get_all_projects_with_user(self, db: Session) -> list[ProjectWithUser]:
        projects = self.project_dao.list(db)
        projects_schemas: list[ProjectWithUser] = []

        for project in projects:
            user = self.user_service.get_user_by_id(db, project.user_id)
            if user:
                projects_schemas.append(ProjectWithUser(
                    id=project.id,
                    title=project.title,
                    description=project.description,
                    active=project.active,
                    start_date=project.start_date,
                    end_date=project.end_date,
                    user=user
                ))
        
        return projects_schemas
            


        
