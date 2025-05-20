from entities.activity_entity import ActivityEntity
from entities.project_entity import ProjectEntity


class WorkplanEntity:
    def __init__(self, id: int, project: ProjectEntity = None, description: str = "", activities: list[ActivityEntity] = None):
        self.__id: int = id
        self.__project: ProjectEntity = project
        self.__description: str = description
        self.__activities: list[ActivityEntity] = activities if activities is not None else []

    
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