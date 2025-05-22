class TaskEntity:
    def __init__(self, id: int, description : str, done : bool):
        self.__id : int= id
        self.__description : str = description
        self.__done : bool = done
    
    def isDone(self) -> bool:
        return self.__done

    def markDone(self) -> None:
        self.__done = True
    
    def markUndone(self) -> None:
        self.__done = False
    
    def addNewDescription(self, newDescription : str) -> None:
        self.__description = newDescription

    def getDescription(self) -> str:
        return self.__description
    
    def getId(self) -> int:
        return self.__id