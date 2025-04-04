from infraestructura.consumidor import ConsumidorProveedores
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5433")
DB_NAME = os.getenv('DB_NAME', default="inventario_servicio_db")

# Configurar base de datos
DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

# Crear consumidor
consumidor = ConsumidorProveedores(
    topico_comandos="comandos_proveedores",
    topico_eventos="eventos_proveedores",
    db_session=db_session
)

if __name__ == "__main__":
    print("Iniciando el servicio para procesar RegistrarProveedor...")
    consumidor.escuchar()