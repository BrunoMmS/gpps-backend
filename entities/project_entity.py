from datetime import date

from entities.workplan_entity import WorkplanEntity


class ProjectEntity:
    def __init__(self, id: int, title: str, description: str,
                 active : bool, start_date: date, end_date: date = None, workplan: WorkplanEntity = None):
        self.__id : int = id
        self.__title: int = title
        self.__description : str = description
        self.__active : bool = active
        self.__start_date: date = start_date
        self.__end_date: date = end_date
        self.__workplan: WorkplanEntity = workplan
        #self.__user : User = None
        """
        def assignUser(self, user: User) -> None:
            if no isInstanced(user, User):
                raise TypeError("Debe ser un usuario")
            self.__user = user
        """


        
