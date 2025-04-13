from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    def publicar_mensaje(self, topico: str, mensaje: dict) -> None:
        pass