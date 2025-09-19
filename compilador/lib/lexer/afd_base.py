from abc import ABC, abstractmethod
from .token import Token

class AfdBase(ABC):
    @abstractmethod
    def process(self, source: str, start_index: int) -> Token | None:
        """
        Processa a string de entrada a partir de um índice inicial
        e retorna um Token se encontrar um padrão válido, ou None caso contrário.
        """
        pass