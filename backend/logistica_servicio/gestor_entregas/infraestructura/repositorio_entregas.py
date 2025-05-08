from sqlalchemy.orm import sessionmaker
from .modelos import Entrega, DetalleEntrega, Base
import os
from sqlalchemy import create_engine, text
import logging
from sqlalchemy.engine import Result

# Load database configuration from environment variables
DB_USERNAME = os.getenv('DB_USERNAME', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5434")  # Port for logistica_servicio_db
DB_NAME = os.getenv('DB_NAME', default="logistica_servicio_db")

def get_engine():
    """Dynamically determine the engine based on the environment."""
    if os.environ.get('UTEST') == "True":
        return create_engine("sqlite:///test_logistica.db")
    else:
        return create_engine(
            f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}',
            pool_size=5,
            max_overflow=2,
            pool_recycle=120,
            pool_timeout=30,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10}
        )

# Use the dynamically determined engine
engine = get_engine()
Session = sessionmaker(bind=engine)

# Ensure all tables are created in the database
Base.metadata.create_all(engine)

class RepositorioEntrega:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def registrar_entrega(self, entrega_data):
        """Register a new delivery."""
        with Session() as session:
            self.logger.info("Iniciando sesión para registrar entrega")
            try:
                self.logger.info(f"Registrando nueva entrega: {entrega_data}")
                entrega = Entrega(**entrega_data)
                session.add(entrega)
                session.commit()
                self.logger.info(f"Entrega registrada con ID: {entrega.id}")
                return entrega.id
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error al registrar entrega: {e}")
                raise

    def actualizar_estado_entrega(self, entrega_id, nuevo_estado):
        """Update the status of a delivery."""
        with Session() as session:
            try:
                self.logger.info(f"Actualizando estado de entrega ID={entrega_id} a '{nuevo_estado}'")
                entrega = session.query(Entrega).filter_by(id=entrega_id).first()
                if not entrega:
                    self.logger.error(f"Entrega con ID={entrega_id} no encontrada")
                    raise ValueError(f"Entrega con ID={entrega_id} no encontrada")
                entrega.estado = nuevo_estado
                session.commit()
                self.logger.info(f"Estado de entrega actualizado para ID={entrega_id}")
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error al actualizar estado de entrega ID={entrega_id}: {e}")
                raise

    def obtener_entregas(self):
        """Retrieve all deliveries."""
        with Session() as session:
            try:
                self.logger.info("Obteniendo todas las entregas")
                entregas = session.query(Entrega).all()
                self.logger.debug(f"Entregas obtenidas: {entregas}")
                return [entrega.__dict__ for entrega in entregas]
            except Exception as e:
                self.logger.error(f"Error al obtener entregas: {e}")
                raise
        
    def obtener_entrega_por_id(self, entrega_id):
        """Retrieve a delivery by its ID."""
        with Session() as session:
            try:
                self.logger.info(f"Obteniendo entrega por ID={entrega_id}")
                entrega = session.query(Entrega).filter_by(id=entrega_id).first()
                if not entrega:
                    self.logger.error(f"Entrega con ID={entrega_id} no encontrada")
                    raise ValueError(f"Entrega con ID={entrega_id} no encontrada")
                return entrega.__dict__
            except Exception as e:
                self.logger.error(f"Error al obtener entrega por ID={entrega_id}: {e}")
                raise

class RepositorioDetalleEntrega:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def registrar_detalle_entrega(self, detalle_data):
        """Register a new delivery detail."""
        with Session() as session:
            try:
                self.logger.info(f"Registrando nuevo detalle de entrega: {detalle_data}")
                detalle = DetalleEntrega(**detalle_data)
                session.add(detalle)
                session.commit()
                self.logger.info(f"Detalle de entrega registrado con ID: {detalle.id}")
                return detalle.id
            except Exception as e:
                session.rollback()
                self.logger.error(f"Error al registrar detalle de entrega: {e}")
                raise

    def obtener_detalles_por_entrega(self, entrega_id):
        """Retrieve all details for a specific delivery."""
        with Session() as session:
            try:
                self.logger.info(f"Obteniendo detalles para entrega ID={entrega_id}")
                detalles = session.query(DetalleEntrega).filter_by(entrega_id=entrega_id).all()
                self.logger.debug(f"Detalles obtenidos: {detalles}")
                return [detalle.__dict__ for detalle in detalles]
            except Exception as e:
                self.logger.error(f"Error al obtener detalles para entrega ID={entrega_id}: {e}")
                raise

"""
curl -X GET http://localhost:3005/api/v1/logistica/generador_rutas_entrega/generar_ruta \
-H "Content-Type: application/json" \
-d '{
    "punto_inicio": {"origen": [4.594121, -74.0817500]},
    "destinos": {
        "B": {"destino": [4.594132167917568, -74.13704414499277]},
        "C": {"destino": [4.564711253902941, -74.176446888055]},
        "D": {"destino": [4.574122371307626, -74.15785927548833]},
        "E": {"destino": [4.536418454418684, -73.98529749322314]},
        "F": {"destino": [4.7027182581716325, -73.99337167373093]},
        "G": {"destino": [4.640993401080931, -74.12516695821564]},
        "H": {"destino": [4.565212545615564, -74.17241358017695]},
        "I": {"destino": [4.700496635976153, -73.98662311060907]},
        "J": {"destino": [4.571271053226157, -74.02800748220766]}
    }
}'
"""