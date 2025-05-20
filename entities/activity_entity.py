from entities.task_entity import TaskEntity


class ActivityEntity:
    def __init__(self, id: int, name: str, duration: int, 
                 done: bool, jobs: list[TaskEntity] = []):
        self.__id : int = id
        self.__name : str = name
        self.__duration : int = duration
        self.__done : bool = done
        self.__jobs : list[TaskEntity] = jobs

    def addTask(self, task: TaskEntity) -> None:
        if not isinstance(task, TaskEntity):
            raise TypeError("Debe ser una Tarea")
        self.__jobs.append(task)

    def searchTask(self, idTask: int) -> TaskEntity | None:
        return next((task for task in self.__jobs if task.getId() == idTask), None)

    def getId(self) -> int:
        return self.__id
    
    def changeName(self, name: str) -> None:
        self.__name = name

    def finished(self) -> None:
        self.__done = True
    
    def unfinished(self) -> None:
        self.__done = False
    
    def isFinished(self) -> bool:
        return self.__done