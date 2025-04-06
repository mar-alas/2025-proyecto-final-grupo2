from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .modelos import Pedido, Base
import os

DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5435")
DB_NAME = os.getenv('DB_NAME', default="ventas_servicio_db")

def get_engine():
    """Dynamically determine the engine based on the environment."""
    if os.environ.get('UTEST') == "True":
        return create_engine("sqlite:///ventas_servicio.db")
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

class RepositorioPedidos:
    def __init__(self, db_session):
        self.db_session = db_session or Session()

    def guardar(self, pedido: Pedido):
        """Guarda un nuevo pedido en la base de datos."""
        self.db_session.add(pedido)
        self.db_session.commit()

    def obtener_por_id(self, pedido_id):
        """Obtiene un pedido por su ID."""
        return self.db_session.query(Pedido).filter_by(id=pedido_id).first()

    def obtener_todos(self):
        """Obtiene todos los pedidos."""
        return self.db_session.query(Pedido).all()

    def obtener_por_cliente(self, cliente_id):
        """Obtiene todos los pedidos de un cliente por su ID."""
        return self.db_session.query(Pedido).filter_by(cliente_id=cliente_id).all()