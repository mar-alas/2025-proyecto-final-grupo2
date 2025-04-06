from flask import Blueprint, jsonify, request
from infraestructura.schema import PedidoInputSchema
from infraestructura.repositorio import RepositorioPedidos
from infraestructura.mappers import to_infraestructura_pedido
from dominio.reglas_negocio import validar_stock_disponible, obtener_stock_disponible, validar_vendedor, validar_cliente
from dominio.modelo import Pedido
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pedidos_escritura = Blueprint('pedidos_escritura', __name__)

# Database setup
DB_USERNAME = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="postgres")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5435")
DB_NAME = os.getenv('DB_NAME', default="ventas_servicio_db")

engine = None
if os.environ.get('UTEST') == "True":
    engine = create_engine("sqlite:///ventas_servicio.db")
else:
    # Configurar base de datos
    DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
db_session = Session()

@pedidos_escritura.route('/pedidos', methods=['POST'])
def registrar_pedido():
    logger.info("Inicio del proceso de registro de pedido")
    data = request.json
    logger.debug(f"Datos recibidos: {data}")

    # Validate input schema
    errores = PedidoInputSchema().validate(data)
    if errores:
        logger.warning(f"Errores de validación en el esquema de entrada: {errores}")
        return jsonify({"error": errores}), 400
    stock_disponible = obtener_stock_disponible()
    errores_stock, productos = validar_stock_disponible(data["productos"], stock_disponible)
    if errores_stock:
        logger.warning(f"Stock insuficiente: {errores_stock}")
        return jsonify({"error": "Stock insuficiente", "detalles": errores_stock}), 409
    
    # Validar si el vendedor id existe, puede venir en blanco o 0
    error_vendedor = validar_vendedor(data["vendedor_id"])
    if error_vendedor:
        return error_vendedor

    # Validar si el cliente id existe, no puede ser nulo
    error_cliente = validar_cliente(data["cliente_id"])
    if error_cliente:
        return error_cliente

    # Crear domain Pedido
    logger.info("Creando objeto de dominio Pedido")
    domain_pedido = Pedido(
        cliente_id=data["cliente_id"],
        vendedor_id=data["vendedor_id"],
        productos=productos
    )

    # Translate to infraestructura Pedido and save
    logger.info("Traduciendo Pedido de dominio a infraestructura y guardando en la base de datos")
    infra_pedido = to_infraestructura_pedido(domain_pedido)
    repositorio = RepositorioPedidos(db_session)
    repositorio.guardar(infra_pedido)

    logger.info("Pedido registrado exitosamente")
    return jsonify({"message": "Pedido registrado exitosamente"}), 201