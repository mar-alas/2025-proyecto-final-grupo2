from flask import Blueprint, jsonify, request
from infraestructura.schema import PedidoInputSchema
from infraestructura.repositorio import RepositorioPedidos
from infraestructura.mappers import to_infraestructura_pedido
from dominio.reglas_negocio import validar_stock_disponible, obtener_stock_disponible, validar_vendedor, validar_cliente
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token
from infraestructura.despachador import Despachador
from dominio.modelo import Pedido
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
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

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No se proporcionó un token"}), 401

    token = auth_header.split(" ")[1]
    validation_result = validar_token(token=token)

    if not validation_result:
         return jsonify({"message": "forbidden"}), 403

    # Validate input schema
    errores = PedidoInputSchema().validate(data)
    if errores:
        logger.warning(f"Errores de validación en el esquema de entrada: {errores}")
        return jsonify({"error": errores}), 400

    stock_disponible = obtener_stock_disponible(token)
    errores_stock = validar_stock_disponible(data["productos"], stock_disponible)
    if errores_stock:
        logger.warning(f"Stock insuficiente: {errores_stock}")
        return jsonify({"error": "Stock insuficiente", "detalles": errores_stock}), 409
    
    # Validar si el vendedor id existe, puede venir en blanco o 0
    error_vendedor = validar_vendedor(data["vendedor_id"])
    if error_vendedor:
        return error_vendedor

    # Validar si el cliente id existe, no puede ser nulo
    error_cliente = validar_cliente(data["cliente_id"], token)
    if error_cliente:
        return error_cliente

    # Crear domain Pedido
    logger.info("Creando objeto de dominio Pedido")
    domain_pedido = Pedido(
        cliente_id=data["cliente_id"],
        vendedor_id=data["vendedor_id"],
        productos=data["productos"]
    )

    # Translate to infraestructura Pedido and save
    logger.info("Traduciendo Pedido de dominio a infraestructura y guardando en la base de datos")
    infra_pedido = to_infraestructura_pedido(domain_pedido)
    repositorio = RepositorioPedidos(db_session)
    repositorio.guardar(infra_pedido)

    try:
        despachador = Despachador()
        productos_pedidos = {}
        for p in infra_pedido.productos:
            despachador.publicar_mensaje('PedidoProcesado', {"producto_id": p.producto_id, "cantidad": p.cantidad})
            productos_pedidos[p.producto_id] = {"cantidad": p.cantidad, "precio_unitario": p.precio_unitario}
        despachador.publicar_mensaje('PedidoCreado', {"pedido_id": infra_pedido.id, "cliente_id": infra_pedido.cliente_id, "vendedor_id": infra_pedido.vendedor_id,
                                                      "productos": productos_pedidos, "estado": infra_pedido.estado, "fecha_creacion": str(infra_pedido.fecha_creacion),
                                                      "total": infra_pedido.total, "subtotal": infra_pedido.subtotal, "token": token})
        despachador.cerrar()

    except Exception as e:
        logger.error(f"Error publicando mensaje en el tópico PedidoProcesado: {e}")
        return jsonify({"error": "Error al procesar el pedido"}), 500

    logger.info("Pedido registrado exitosamente")
    return jsonify({"message": "Pedido registrado exitosamente"}), 201