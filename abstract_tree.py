from abc import ABC, abstractmethod

class AbstractTree(ABC):
    @abstractmethod
    def insert(self, value: int) -> None:
        pass

    @abstractmethod
    def delete(self, value:int) -> None:
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def contains(self, value: int) -> bool:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass