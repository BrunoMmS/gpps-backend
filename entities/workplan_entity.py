from entities.activity_entity import ActivityEntity
from entities.project_entity import ProjectEntity

class WorkplanEntity:
    def __init__(self, id: int, project: ProjectEntity, description: str = "", activities: list[ActivityEntity] = []):
        self.__id: int = id
        self.__project: ProjectEntity = project
        self.__description: str = description
        self.__activities: list[ActivityEntity] = activities

    
    def addActivity(self, activity: ActivityEntity) -> None:
        if not isinstance(activity, ActivityEntity):
            raise TypeError("Debe ser una Actividad")
        self.__activities.append(activity)
    
    def assignProject(self, project : ProjectEntity) -> None:
        if not isinstance(project, ProjectEntity):
            raise TypeError("Debe ser un Proyecto")
        self.__project = project

    def getId(self) -> int:
        return self.__id

    def getDescription(self) -> str:
        return self.__description
    
    def get_completed_percent(self) -> float:
        if not self.__activities:
            raise ValueError("No hay actividades en el plan de trabajo")
        completed_activities = sum(1 for activity in self.__activities if activity.isDone())
        return (completed_activities / len(self.__activities)) * 100
    
    def get_incopmlete_percent(self) -> float:
        return 100 - self.get_completed_percent()