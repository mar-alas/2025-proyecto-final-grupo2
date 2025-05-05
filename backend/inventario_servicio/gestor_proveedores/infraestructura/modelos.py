from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Proveedor(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numero_contacto = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    caracteristicas = Column(String)
    condiciones_comerciales_tributarias = Column(String)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Proveedor(id={self.id}, nombre={self.nombre}, email={self.email}, pais={self.pais})>"