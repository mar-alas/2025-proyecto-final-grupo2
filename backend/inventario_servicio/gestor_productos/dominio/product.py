# estándar
import uuid
from datetime import date

# terceros
from sqlalchemy.orm import relationship
from infraestructura.database import db


class Product(db.Model):
    __tablename__ = "productos"

    uuid = db.Column(db.String(36), primary_key=False, default=lambda: str(uuid.uuid4()))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    tiempo_entrega = db.Column(db.String(50), nullable=True)
    precio = db.Column(db.Float, nullable=False)
    condiciones_almacenamiento = db.Column(db.String(255), nullable=True)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    estado = db.Column(db.String(50), nullable=False, default="en_stock")
    inventario_inicial = db.Column(db.Integer, nullable=False)
    proveedor = db.Column(db.String(100), nullable=True)

    imagenes = relationship("ProductImage", back_populates="producto", cascade="all, delete-orphan")

    def __init__(
        self,
        nombre,
        descripcion,
        tiempo_entrega,
        precio,
        condiciones_almacenamiento,
        fecha_vencimiento,
        estado,
        inventario_inicial,
        proveedor,
        imagenes_productos=None,
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tiempo_entrega = tiempo_entrega
        self.precio = precio
        self.condiciones_almacenamiento = condiciones_almacenamiento
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.inventario_inicial = inventario_inicial
        self.proveedor = proveedor
        self.imagenes = imagenes_productos or []


    def to_dict(self):
        return {
            "id": self.id,
            # "uuid": self.uuid,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tiempo_entrega": self.tiempo_entrega,
            "precio": self.precio,
            "condiciones_almacenamiento": self.condiciones_almacenamiento,
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "estado": self.estado,
            "inventario_inicial": self.inventario_inicial,
            "proveedor": self.proveedor,
            "imagenes": [img.to_dict() for img in self.imagenes] if self.imagenes else []
        }
