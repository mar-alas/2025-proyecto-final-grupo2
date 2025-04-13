from abc import ABC, abstractmethod

class EventPublisher(ABC):
    @abstractmethod
    def publicar_mensaje(self, topico: str, mensaje: dict) -> None:
        raise NotImplementedError("Este método debe ser implementado por una subclase")