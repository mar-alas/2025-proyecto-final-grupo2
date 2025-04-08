from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
import json
import sqlite3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float, Text

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
# Define the Base for SQLAlchemy models
Base = declarative_base()

# Define the Productos table as a SQLAlchemy model
class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    tiempo_entrega = Column(String)
    precio = Column(Float)
    condiciones_almacenamiento = Column(Text)
    fecha_vencimiento = Column(String)
    estado = Column(String)
    inventario_inicial = Column(Integer)
    imagenes_productos = Column(Text)
    proveedor = Column(String)

# Use the dynamically determined engine
engine = get_engine()
Session = sessionmaker(bind=engine)

# Ensure all tables are created in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()

# Delete all records from the Stock table (if it exists)
try:
    stock_table = Table('stock', Base.metadata, autoload_with=engine)
    session.execute(stock_table.delete())
    session.commit()
except Exception as e:
    print(f"Error while clearing stock table: {e}")

# Delete all records from the Productos table
session.query(Producto).delete()
session.commit()

# Insert the mock data into the Productos table
productos = [
    Producto(id=1, nombre="Sal", descripcion="Sal refinada para consumo diario", tiempo_entrega="2 días", precio=50.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco", fecha_vencimiento="2025-12-31",
                estado="en_stock", inventario_inicial=500, imagenes_productos="sal1.jpg,sal2.jpg",
                proveedor="Proveedor Salinas S.A."),
    Producto(id=2, nombre="Arroz", descripcion="Arroz blanco de grano largo", tiempo_entrega="3 días", precio=120.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco", fecha_vencimiento="2025-12-31",
                estado="en_stock", inventario_inicial=300, imagenes_productos="arroz1.jpg,arroz2.jpg",
                proveedor="Proveedor Arrocero S.A."),
    Producto(id=3, nombre="Azúcar", descripcion="Azúcar blanca refinada", tiempo_entrega="2 días", precio=80.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco", fecha_vencimiento="2025-12-31",
                estado="en_stock", inventario_inicial=400, imagenes_productos="azucar1.jpg,azucar2.jpg",
                proveedor="Proveedor Dulce S.A."),
    Producto(id=4, nombre="Aceite", descripcion="Aceite vegetal para cocinar", tiempo_entrega="4 días", precio=150.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco", fecha_vencimiento="2025-12-31",
                estado="en_stock", inventario_inicial=250, imagenes_productos="aceite1.jpg,aceite2.jpg",
                proveedor="Proveedor Oleico S.A."),
    Producto(id=5, nombre="Frijoles", descripcion="Frijoles negros empaquetados", tiempo_entrega="3 días", precio=90.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco", fecha_vencimiento="2025-12-31",
                estado="en_stock", inventario_inicial=350, imagenes_productos="frijoles1.jpg,frijoles2.jpg",
                proveedor="Proveedor Legumbres S.A.")
]


# Add the products to the session with a check to avoid duplicates
for producto in productos:
    existing_producto = session.query(Producto).filter_by(id=producto.id).first()
    if not existing_producto:
        session.add(producto)

# Commit the session to save the data
session.commit()

# Close the session
session.close()

def mock_registro_producto():
    conexion = ConexionPulsar()
    productor = conexion.cliente.create_producer("ProductoRegistrado")
    productos = [
        {
            "id": 1,
            "nombre": "Sal",
            "descripcion": "Sal refinada para consumo diario",
            "tiempo_entrega": "2 días",
            "precio": 50.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 500,
            "imagenes_productos": ["sal1.jpg", "sal2.jpg"],
            "proveedor": "Proveedor Salinas S.A."
        },
        {
            "id": 2,
            "nombre": "Arroz",
            "descripcion": "Arroz blanco de grano largo",
            "tiempo_entrega": "3 días",
            "precio": 120.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 300,
            "imagenes_productos": ["arroz1.jpg", "arroz2.jpg"],
            "proveedor": "Proveedor Arrocero S.A."
        },
        {
            "id": 3,
            "nombre": "Azúcar",
            "descripcion": "Azúcar blanca refinada",
            "tiempo_entrega": "2 días",
            "precio": 80.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 400,
            "imagenes_productos": ["azucar1.jpg", "azucar2.jpg"],
            "proveedor": "Proveedor Dulce S.A."
        },
        {
            "id": 4,
            "nombre": "Aceite",
            "descripcion": "Aceite vegetal para cocinar",
            "tiempo_entrega": "4 días",
            "precio": 150.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 250,
            "imagenes_productos": ["aceite1.jpg", "aceite2.jpg"],
            "proveedor": "Proveedor Oleico S.A."
        },
        {
            "id": 5,
            "nombre": "Frijoles",
            "descripcion": "Frijoles negros empaquetados",
            "tiempo_entrega": "3 días",
            "precio": 90.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 350,
            "imagenes_productos": ["frijoles1.jpg", "frijoles2.jpg"],
            "proveedor": "Proveedor Legumbres S.A."
        }
    ]

    for producto in productos:
        mensaje = {
            "producto_id": producto["id"],
            "nombre": producto["nombre"],
            "descripcion": producto["descripcion"],
            "tiempo_entrega": producto["tiempo_entrega"],
            "precio": producto["precio"],
            "condiciones_almacenamiento": producto["condiciones_almacenamiento"],
            "fecha_vencimiento": producto["fecha_vencimiento"],
            "estado": producto["estado"],
            "inventario_inicial": producto["inventario_inicial"],
            "imagenes_productos": producto["imagenes_productos"],
            "proveedor": producto["proveedor"]
        }
        productor.send(json.dumps(mensaje).encode("utf-8"))
    conexion.cliente.close()
