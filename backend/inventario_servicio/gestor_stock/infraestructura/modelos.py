from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import Table, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False, unique=True)
    inventario = Column(Integer, nullable=False, default=0)

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    tiempo_entrega = Column(String)
    precio = Column(Float)
    condiciones_almacenamiento = Column(Text)
    fecha_vencimiento = Column(String)
    estado = Column(String)
    inventario_inicial = Column(Integer)
    imagenes_productos = Column(Text)
    proveedor = Column(String)