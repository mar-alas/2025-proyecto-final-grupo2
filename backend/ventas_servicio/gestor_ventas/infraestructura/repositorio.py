from sqlalchemy import create_engine, Date
from sqlalchemy.orm import sessionmaker
from .modelos import VisitaCliente as InfraVisitaCliente, Base
from .modelos import RutaVisita as InfraRutaVisita
from .modelos import PlanVentaVendedor

import os
import logging
from infraestructura.mappers import to_infraestructura_visita, to_plan_venta_entity
from datetime import datetime

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
engine = None
if os.environ.get('UTEST') == "True":
    engine = create_engine("sqlite:///ventas_servicio.db")
else:
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


class RepositorioPlanesVenta:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def guardar_o_actualizar(self, plan_venta):
        try:
            entity = to_plan_venta_entity(plan_venta)

            existente = self.db_session.query(PlanVentaVendedor).filter_by(
                vendedor_id=entity.vendedor_id,
                fecha=entity.fecha
            ).first()

            if existente:
                existente.valor = entity.valor
            else:
                self.db_session.add(entity)

            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Error al guardar el plan de venta: {e}")
            raise e


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


class RutasVisitas:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()
        self.agregar_datos_por_defecto()

    def obtener_rutas_por_vendedor_y_fecha(self, vendedor_id, fecha):
        """Retrieve routes for a specific vendor and date."""
        try:
            rutas = self.db_session.query(InfraRutaVisita).filter(
                InfraRutaVisita.vendedor_id == vendedor_id,
                InfraRutaVisita.fecha.cast(Date) == datetime.strptime(fecha, "%Y-%m-%d").date()
            ).all()
            return rutas
        except Exception as e:
            logger.error(f"Error al obtener las rutas: {e}")
            raise e

    # Add default data to the repository
    def agregar_datos_por_defecto(self):
        logger.info("Agregando datos por defecto a la base de datos...")
        session = Session()
        try:
            # Check if data already exists
            if not session.query(InfraRutaVisita).first():
                rutas_por_defecto = [
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 9, 0), cliente_id=1, nombre_cliente="Carlos Gomez", barrio="El Poblado", orden=1, tiempo_estimado="0.5", distancia="5 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 11, 0), cliente_id=2, nombre_cliente="Maria Lopez", barrio="La Floresta", orden=2, tiempo_estimado="1", distancia="10 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 14, 0), cliente_id=3, nombre_cliente="Luis Martinez", barrio="Belén", orden=3, tiempo_estimado="0.25", distancia="2 km"),
                    InfraRutaVisita(vendedor_id=1, fecha=datetime(2025, 4, 21, 16, 0), cliente_id=4, nombre_cliente="Ana Torres", barrio="Laureles", orden=4, tiempo_estimado="2", distancia="3 km")
                ]
                session.add_all(rutas_por_defecto)
                session.commit()
                logger.info("Datos por defecto agregados exitosamente.")
            else:
                logger.info("Los datos por defecto ya existen en la base de datos.")
        except Exception as e:
            session.rollback()
            logger.error(f"Error al agregar datos por defecto: {e}")
            raise e
        finally:
            session.close()