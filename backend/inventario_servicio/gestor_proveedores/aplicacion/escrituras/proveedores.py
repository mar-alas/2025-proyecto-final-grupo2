from flask import Blueprint, jsonify, request
from infraestructura.schema import ProveedorInputSchema
from infraestructura.despachador import DespachadorProveedores
from infraestructura.consumidor import ConsumidorProveedores
from infraestructura.repositorio import RepositorioProveedores
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid  # Import the UUID module
import os
import logging
from dominio.reglas_negocio import validar_datos_no_vacios

proveedores_escritura = Blueprint('home_escritura', __name__)

# Despachador para publicar comandos en la cola de comandos
despachador_comandos = DespachadorProveedores(topico_eventos="comandos_proveedores")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5433")
DB_NAME = os.getenv('DB_NAME', default="inventario_servicio_db")

engine = None
if os.environ.get('UTEST') == "True":
    engine = create_engine("sqlite:///proveedores.db")
else:
    # Configurar base de datos
    DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
db_session = Session()

consumidor = ConsumidorProveedores(
    topico_comandos="comandos_proveedores",
    topico_eventos="eventos_proveedores",
    db_session=db_session
)

@proveedores_escritura.route('/proveedores', methods=['POST'])
def registrar_proveedor():
    data = request.json

    # Validate that data is not empty
    errores = validar_datos_no_vacios(data)
    if not errores:
        # Validate schema only if data is not empty
        errores = ProveedorInputSchema().validate(data)
    if errores:
        return jsonify({"error": errores}), 400

    # Check for duplicate 'nombre' using the repository
    repositorio = RepositorioProveedores(db_session=db_session)
    if repositorio.existe_por_nombre(data.get("nombre")):
        return jsonify({"error": f"Ya existe un proveedor con el nombre '{data.get('nombre')}'."}), 207

    logger.info(f"Recibido comando para registrar proveedor: {data}")
    # Generate a unique correlation ID
    correlation_id = str(uuid.uuid4())
    data["correlation_id"] = correlation_id
    try:
        logger.info(f"Publicando el comando en la cola de comandos con ID: {correlation_id}")
        # Publicar el comando en la cola de comandos
        comando = {"comando": "RegistrarProveedor", "data": data}
        despachador_comandos.publicar_evento(comando)
    except Exception as e:
        logger.error(f"Error al publicar el comando: {str(e)}")
        return jsonify({"error": "Error al procesar el comando"}), 500
    else:
        return jsonify({"message": "Proveedor enviado a registrar exitosamente"}), 201