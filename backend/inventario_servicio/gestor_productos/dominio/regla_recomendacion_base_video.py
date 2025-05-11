from abc import ABC, abstractmethod
from dominio.producto_detectado_video import ProductoDetectadoVideo

class ReglaRecomendacion(ABC):
    @abstractmethod
    def aplicar(self, producto: ProductoDetectadoVideo) -> list[dict]:
        pass

    @abstractmethod
    def sugerencias_pedido(self, producto: ProductoDetectadoVideo) -> list[dict]:
        pass