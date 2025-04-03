import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .modelos import Proveedor, Base

# Load database configuration from environment variables
DB_USERNAME = os.getenv('DB_USERNAME', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5433")  # Port for inventario_servicio_db
DB_NAME = os.getenv('DB_NAME', default="inventario_servicio_db")

def get_engine():
    """Dynamically determine the engine based on the environment."""
    if os.environ.get('UTEST') == "True":
        return create_engine("sqlite:///proveedores.db")
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

class RepositorioProveedores:
    def __init__(self, db_session=None):
        self.db_session = db_session or Session()

    def guardar(self, proveedor: Proveedor):
        """Save a new provider to the database."""
        self.db_session.add(proveedor)
        self.db_session.commit()

    def obtener_por_id(self, proveedor_id):
        """Retrieve a provider by its ID."""
        return self.db_session.query(Proveedor).filter_by(id=proveedor_id).first()

    def obtener_todos(self):
        """Retrieve all providers."""
        return self.db_session.query(Proveedor).all()

    def existe_por_nombre(self, nombre):
        """Check if a provider with the given name already exists."""
        return self.db_session.query(Proveedor).filter_by(nombre=nombre).first() is not None