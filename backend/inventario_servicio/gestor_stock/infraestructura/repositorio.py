from sqlalchemy.orm import Session, sessionmaker
from .modelos import Stock
import os
from sqlalchemy import create_engine
from .modelos import Base
from .modelos import Producto

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

class RepositorioStock:
    def __init__(self, db_session: Session):
        self.db_session = db_session or Session()

    def actualizar_inventario_inicial(self, producto_id, cantidad):
        stock = self.db_session.query(Stock).filter_by(producto_id=producto_id).first()
        if stock:
            stock.inventario = cantidad
        else:
            stock = Stock(producto_id=producto_id, inventario=cantidad)
            self.db_session.add(stock)
        self.db_session.commit()

    def actualizar_inventario(self, producto_id, cantidad):
        stock = self.db_session.query(Stock).filter_by(producto_id=producto_id).first()
        if stock:
            stock.inventario += cantidad
        else:
            stock = Stock(producto_id=producto_id, inventario=cantidad)
            self.db_session.add(stock)
        self.db_session.commit()

    def obtener_inventario(self):
        query = self.db_session.query(
            Stock.producto_id,
            Stock.inventario,
            Producto.nombre.label("producto_nombre")
        ).join(Producto, Stock.producto_id == Producto.id)
        return query.all()