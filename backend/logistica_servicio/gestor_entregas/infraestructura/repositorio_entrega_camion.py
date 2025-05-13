from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from infraestructura.modelos import Base, EntregasProgramadas, EntregaProgramadaDetalle
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


class RepositorioEntregasProgramadas:
    def __init__(self):
        self.db_session = Session()

    def agregar_entrega_programada(self, entrega: EntregasProgramadas):
        try:
            self.db_session.add(entrega)
            self.db_session.commit()
            self.db_session.refresh(entrega)  # Refresh to get the generated ID
            return entrega.id
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def obtener_entrega_programada_por_id(self, entrega_id: int):
            return self.db_session.query(EntregasProgramadas).filter_by(id=entrega_id).first()
    
    def obtener_entregas_programadas_por_fecha_camion(self, fecha: str, camion_id: int):
        return self.db_session.query(EntregasProgramadas).filter_by(fecha_programada=fecha, camion_id=camion_id).all()

    def actualizar_entrega_programada(self, entrega_id: int, nuevos_datos: dict):
        try:
            entrega = self.db_session.query(EntregasProgramadas).filter_by(id=entrega_id).first()
            if entrega:
                for key, value in nuevos_datos.items():
                    setattr(entrega, key, value)
                self.db_session.commit()
                return entrega
            else:
                raise ValueError("Entrega no encontrada")
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def listar_entregas_programadas(self):
        return self.db_session.query(EntregasProgramadas).all()


class RepositorioEntregaProgramadasDetalle:
    def __init__(self):
        self.db_session = Session()

    def agregar_detalle(self, detalle: EntregaProgramadaDetalle):
        try:
            self.db_session.add(detalle)
            self.db_session.commit()
            return detalle.id
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def obtener_detalle_por_id(self, detalle_id: int):
        return self.db_session.query(EntregaProgramadaDetalle).filter_by(id=detalle_id).first()

    def listar_detalles_por_entrega(self, entrega_id: int):
        return self.db_session.query(EntregaProgramadaDetalle).filter_by(entrega_programada_id=entrega_id).all()


    def eliminar_detalle(self, detalle_id: int):
        try:
            detalle = self.obtener_detalle_por_id(detalle_id)
            if detalle:
                self.db_session.delete(detalle)
                self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e