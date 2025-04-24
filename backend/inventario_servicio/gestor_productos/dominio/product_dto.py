from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

from .product_image_dto import ProductImageDTO

@dataclass
class ProductDTO:
    """Representa los datos de un producto que se reciben en la API."""
    nombre: str
    descripcion: str
    tiempo_entrega: str
    precio: float
    condiciones_almacenamiento: str
    fecha_vencimiento: date
    estado: str
    inventario_inicial: int
    proveedor: str
    imagenes_productos: List[ProductImageDTO] = field(default_factory=list)
    id: Optional[int] = None
