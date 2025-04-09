from sqlalchemy.orm import sessionmaker
from .modelos import Stock
import os
from sqlalchemy import create_engine
from .modelos import Base
from .modelos import Producto
import logging

# Load database configuration from environment variables
DB_USERNAME = os.getenv('DB_USERNAME', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5433")  # Port for inventario_servicio_db
DB_NAME = os.getenv('DB_NAME', default="inventario_servicio_db")

def get_engine():
    """Dynamically determine the engine based on the environment."""
    if os.environ.get('UTEST') == "True":
        return create_engine("sqlite:///test_stock.db")
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
    def __init__(self):
        self.db_session = Session()
        self.logger = logging.getLogger(__name__)

    def actualizar_inventario_inicial(self, producto_id, cantidad):
        try:
            self.logger.info(f"Actualizando inventario inicial para producto_id={producto_id} con cantidad={cantidad}")
            stock = self.db_session.query(Stock).filter_by(producto_id=producto_id).first()
            if stock:
                self.logger.debug(f"Producto encontrado en inventario. Actualizando inventario a {cantidad}")
                stock.inventario = cantidad
            else:
                self.logger.debug(f"Producto no encontrado en inventario. Creando nuevo registro con cantidad={cantidad}")
                stock = Stock(producto_id=producto_id, inventario=cantidad)
                self.db_session.add(stock)
            self.db_session.commit()
            self.logger.info(f"Inventario inicial actualizado para producto_id={producto_id}")
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error al actualizar inventario inicial para producto_id={producto_id}: {e}")
            raise

    def actualizar_inventario(self, producto_id, cantidad):
        try:
            self.logger.info(f"Actualizando inventario para producto_id={producto_id} con cantidad={cantidad}")
            stock = self.db_session.query(Stock).filter_by(producto_id=producto_id).first()
            if stock:
                self.logger.debug(f"Producto encontrado en inventario. Incrementando inventario en {cantidad}")
                stock.inventario += cantidad
                if stock.inventario < 0:
                    self.logger.error(f"Inventario negativo para producto_id={producto_id}.")
                    raise ValueError(f"No hay suficiente inventario para el producto con el id {producto_id}.")
                self.db_session.commit()
                self.logger.info(f"Inventario actualizado para producto_id={producto_id}")
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error al actualizar inventario para producto_id={producto_id}: {e}")
            raise


    def obtener_inventario(self):
        try:
            self.logger.info("Obteniendo inventario completo")
            query = self.db_session.query(
                Stock.producto_id,
                Stock.inventario,
                Producto.nombre.label("producto_nombre")
            ).join(Producto, Stock.producto_id == Producto.id)
            result = query.all()
            self.logger.debug(f"Inventario obtenido: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Error al obtener inventario: {e}")
            raise