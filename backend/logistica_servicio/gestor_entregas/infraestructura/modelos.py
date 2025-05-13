from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# repositorio_entregas.py
class Entrega(Base):
    __tablename__ = 'entregas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    fecha_entrega = Column(Date, nullable=False)
    hora_entrega = Column(Time, nullable=False)
    estado = Column(String(50), nullable=False)  # Ejemplo: "Pendiente", "Entregado", etc.
    direccion_entrega = Column(String(255), nullable=False)
    coordenadas_origen = Column(String(50), nullable=False)  # Ejemplo: "latitud,longitud"
    coordenadas_destino = Column(String(50), nullable=False)  # Ejemplo: "latitud,longitud"
    cantidad = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)  # cantidad * precio_unitario

class DetalleEntrega(Base):
    __tablename__ = 'detalle_entregas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entrega_id = Column(Integer, ForeignKey('entregas.id'), nullable=False)
    camion_id = Column(Integer, ForeignKey('camiones.id'), nullable=False)

# ________________end of repositorio_entregas.py______________________

# repositorio_entrega_camion.py

class EntregasProgramadas(Base):
    __tablename__ = 'entregas_programadas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_programada = Column(Date, nullable=False)
    camion_id = Column(Integer, ForeignKey('camiones.id'), nullable=False)
    ruta_calculada = Column(String(255), nullable=False)

class EntregaProgramadaDetalle(Base):
    __tablename__ = 'entrega_programada_detalles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    entrega_programada_id = Column(Integer, ForeignKey('entregas_programadas.id'), nullable=False)
    entrega_id = Column(Integer, ForeignKey('entregas.id'), nullable=False)

# ________________end of repositorio_entrega_camion.py______________________

# repositorio_camion.py
class Camion(Base):
    __tablename__ = 'camiones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String, nullable=False, unique=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    capacidad_carga_toneladas = Column(Float, nullable=False)
    volumen_carga_metros_cubicos = Column(Float, nullable=False)

# ________________end of repositorio_camion.py______________________