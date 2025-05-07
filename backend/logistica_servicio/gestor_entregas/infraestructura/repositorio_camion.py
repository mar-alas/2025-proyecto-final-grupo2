from sqlalchemy.orm import sessionmaker
from .modelos import Camion, Base
import os
from sqlalchemy import create_engine
import logging

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

class RepositorioCamion:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.crear_camiones_por_defecto()

    def registrar_camion(self, camion_data):
        """Register a new truck."""
        try:
            self.logger.info(f"Registrando nuevo camión: {camion_data}")
            with Session() as session:
                camion = Camion(**camion_data)
                session.add(camion)
                session.commit()
                self.logger.info(f"Camión registrado con ID: {camion.id}")
                return camion.id
        except Exception as e:
            self.logger.error(f"Error al registrar camión: {e}")
            raise

    def obtener_camiones(self):
        """Retrieve all trucks."""
        try:
            self.logger.info("Obteniendo todos los camiones")
            with Session() as session:
                camiones = session.query(Camion).all()
                self.logger.debug(f"Camiones obtenidos: {camiones}")
                return [camion.__dict__ for camion in camiones]
        except Exception as e:
            self.logger.error(f"Error al obtener camiones: {e}")
            raise
    
    def obtener_camion_por_id(self, camion_id):
        """Retrieve a truck by its ID."""
        try:
            self.logger.info(f"Obteniendo camión con ID: {camion_id}")
            with Session() as session:
                camion = session.query(Camion).filter_by(id=camion_id).first()
                if not camion:
                    self.logger.error(f"Camión con ID {camion_id} no encontrado")
                    raise ValueError(f"Camión con ID {camion_id} no encontrado")
                return camion.__dict__
        except Exception as e:
            self.logger.error(f"Error al obtener camión por ID: {e}")
            raise

    def obtener_camion_por_placa(self, placa):
        """Retrieve a truck by its license plate."""
        try:
            self.logger.info(f"Obteniendo camión con placa: {placa}")
            with Session() as session:
                camion = session.query(Camion).filter_by(placa=placa).first()
                if not camion:
                    return None
                return camion.__dict__
        except Exception as e:
            self.logger.error(f"Error al obtener camión por placa: {e}")
            raise
    
    def crear_camiones_por_defecto(self):
        """Create two default trucks."""
        try:
            self.logger.info("Creando camiones por defecto")
            default_camiones = [
                {"placa": "ABC123", "marca": "Volvo", "modelo": "FH", "capacidad_carga_toneladas": 20000, "volumen_carga_metros_cubicos": 50},
                {"placa": "XYZ789", "marca": "Scania", "modelo": "R500", "capacidad_carga_toneladas": 25000, "volumen_carga_metros_cubicos": 60},
            ]
            for camion_data in default_camiones:
                existing_camion = self.obtener_camion_por_placa(camion_data["placa"])
                self.logger.info(f"Verificando existencia del camión con placa {camion_data['placa']}")
                if not existing_camion:
                    self.registrar_camion(camion_data)
                else:
                    self.logger.info(f"Camión con placa {camion_data['placa']} ya existe. No se creará uno nuevo.")
            self.logger.info("Camiones por defecto creados exitosamente")
        except Exception as e:
            self.logger.error(f"Error al crear camiones por defecto: {e}")
            raise
