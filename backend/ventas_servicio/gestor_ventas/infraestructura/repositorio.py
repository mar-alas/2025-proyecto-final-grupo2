from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .modelos import VisitaCliente as InfraVisitaCliente, Base
import os
import logging
from infraestructura.mappers import to_infraestructura_visita

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5435")
DB_NAME = os.getenv('DB_NAME', default="ventas_servicio_db")

DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'

# Initialize the database engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Ensure all tables are created in the database
def initialize_database():
    logger.info("Verificando si las tablas de la base de datos existen...")
    try:
        Base.metadata.create_all(engine)
        logger.info("Tablas creadas exitosamente o ya existentes.")
    except Exception as e:
        logger.error(f"Error al crear las tablas en la base de datos: {e}")
        raise e

# Call the database initialization function
initialize_database()

class RepositorioVisitas:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def guardar(self, visita):
        """Guarda una nueva visita en la base de datos."""
        try:
            # Map the domain model to the infrastructure model
            infra_visita = to_infraestructura_visita(visita)
            self.db_session.add(infra_visita)
            self.db_session.commit()
            logger.info("Visita guardada exitosamente.")
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error al guardar la visita: {e}")
            raise e