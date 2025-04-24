from sqlalchemy import Column, Integer, String, DateTime, JSON
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