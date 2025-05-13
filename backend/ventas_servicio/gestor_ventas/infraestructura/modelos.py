from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VisitaCliente(Base):
    __tablename__ = 'visitas_cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, nullable=False)
    vendedor_id = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    ubicacion_productos_ccp = Column(JSON, nullable=False)
    ubicacion_productos_competencia = Column(JSON, nullable=False)


class RutaVisita(Base):
    __tablename__ = 'rutas_visita'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendedor_id = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    nombre_cliente = Column(String, nullable=False)
    barrio = Column(String, nullable=False)
    orden = Column(Integer, nullable=False)
    tiempo_estimado = Column(String, nullable=True)
    distancia = Column(String, nullable=True)


class PlanVentaVendedor(Base):
    __tablename__ = 'planes_venta_x_vendedor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vendedor_id = Column(Integer, nullable=False)
    fecha = Column(String, nullable=False)
    valor = Column(Float, nullable=False)