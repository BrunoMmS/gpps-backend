from typing import Optional
from sqlalchemy.orm import Session
from cruds.UserInProjectDAO import UserInProjectDAO
from cruds.projectDAO import ProjectDAO
from entities.project_entity import ProjectEntity
from entities.user_in_project_entity import UserInProjectEntity
from schemas.project_schema import ProjectCreate, ProyectComplete, ProjectWithUser
from schemas.workplan_schema import WorkPlanCreate
from models.project_model import ProjectModel
from services.notification_service import NotificationService
from services.rol import Rol
from services.user_service import UserService
from services.workplan_service import WorkPlanService
from services.activity_service import ActivityService
from entities.project_entity import ProjectEntity
class ProjectService:
    def __init__(self):
        self.project_dao = ProjectDAO()
        self.workplan_service = WorkPlanService()
        self.user_service = UserService()
        self.activity_service= ActivityService()

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
        return self.workplan_service.create_workplan(db,  workplan_data)
    
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
    def get_report_project(self, db: Session, proyect_id: int) -> Optional[str]:
       project_model = self.project_dao.get_proyect_complete(db, proyect_id)
       if not project_model:
        raise ValueError("Proyecto no encontrado")

       report_lines = []

       report_lines.append(f"Proyecto: {project_model.title}")
       report_lines.append(f"Descripción: {project_model.description}")
       report_lines.append(f"Activo: {'Sí' if project_model.active else 'No'}")
       report_lines.append(f"Fecha de inicio: {project_model.start_date}")
       report_lines.append(f"Fecha de fin: {project_model.end_date if project_model.end_date else 'No definida'}")
       report_lines.append("")
       workplan= self.workplan_service.workplan_to_entity(project_model.workplan,self.proyect_to_entity(project_model))
       
       if workplan:
           report_lines.append(f"Workplan:")
           report_lines.append(f"Descripción: {workplan.getDescription()}")
           report_lines.append(f"Duracion estimada: {workplan.getDuration()}")
           report_lines.append(f"Porcentaje de actividades hechas: {workplan.get_completed_percent()}")
           report_lines.append(f"Porcentaje de no actividades hechas: {workplan.get_incopmlete_percent()}")
           for activity_model in project_model.workplan.activities:
               activity_entity = self.activity_service.activity_to_entity(activity_model)
               report_lines.append(f"    - Actividad: {activity_entity.getName()}")
               report_lines.append(f"      Duración: {activity_entity.getDuration()}")
               report_lines.append(f"      Completada: {'Sí' if activity_entity.isFinished() else 'No'}")
               report_lines.append(f"      Porcentaje de tareas hechas:{activity_entity.get_complete_percent()}")
               report_lines.append(f"      Porcentaje de tareas hechas:{activity_entity.get_incomplete_percent()}")
               if activity_entity.getJobs():
                   report_lines.append("      Tareas:")
                   for task in activity_entity.getJobs():
                       report_lines.append(f"        * {task.getDescription()} - {'Completada' if task.isDone() else 'Pendiente'}")
               else:
                  report_lines.append("No tiene tareas.")
                
               report_lines.append("") 
       else:
           report_lines.append(f"No hay proyecto definido")
       return "\n".join(report_lines)       

    def proyect_to_entity(self, proyect_model: ProyectComplete) -> ProjectEntity:
        user_entity = None
        if proyect_model.creator is not None:
          user_entity = self.user_service.to_entity(proyect_model.creator)
        return ProjectEntity(
        id=proyect_model.id,
        title=proyect_model.title,
        description=proyect_model.description,
        active=proyect_model.active,
        start_date=proyect_model.start_date,
        end_date=proyect_model.end_date,
        user=user_entity
        )

        
        
