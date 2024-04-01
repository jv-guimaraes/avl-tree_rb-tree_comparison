from abc import ABC, abstractmethod

class ArvoreAbstrata(ABC):
    @abstractmethod
    def inserir(self, valor: int) -> None:
        pass

    @abstractmethod
    def remover(self, valor:int) -> None:
        pass
    
    @abstractmethod
    def esta_vazia(self) -> bool:
        pass

    @abstractmethod
    def contem(self, valor: int) -> bool:
        pass

    @abstractmethod
    def resetar(self) -> None:
        pass