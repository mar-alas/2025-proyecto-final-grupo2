from flask import Blueprint, jsonify, request
from infraestructura.repositorio import RepositorioPedidos
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token
import logging
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


pedidos_lectura = Blueprint('pedidos_lectura', __name__)

repositorio = RepositorioPedidos(db_session=None)

@pedidos_lectura.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    """
    Obtiene la lista de pedidos de un cliente con sus estados actuales.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No se proporcionó un token"}), 401

    token = auth_header.split(" ")[1]
    validation_result = validar_token(token=token)

    if not validation_result:
         return jsonify({"message": "forbidden"}), 403

    cliente_id = request.args.get('cliente_id')  # Obtener el parámetro 'cliente_id' de la URL
    if not cliente_id:
        logger.warning("El parámetro 'cliente_id' es obligatorio pero no fue proporcionado")
        return jsonify({
            "error": "El parámetro 'cliente_id' es obligatorio",
            "mensaje": "Debe proporcionar un cliente_id para consultar los pedidos"
        }), 400

    try:
        logger.info(f"Consultando pedidos para el cliente con ID {cliente_id}")
        # Obtener los pedidos del cliente
        pedidos = repositorio.obtener_por_cliente(cliente_id)
        if not pedidos:
            logger.info(f"No se encontraron pedidos para el cliente con ID {cliente_id}")
            return jsonify({
                "error": "El cliente no tiene pedidos",
                "mensaje": f"No se encontraron pedidos para el cliente con ID {cliente_id}"
            }), 404

        # Construir la respuesta
        pedidos_resumen = [
            {
                "id": pedido.id,
                "fecha": pedido.fecha_creacion.isoformat(),
                "cantidad_productos": sum(producto.cantidad for producto in pedido.productos),
                "estado": pedido.estado
            } for pedido in pedidos
        ]

        # Obtener parámetros de paginación
        page = int(request.args.get('page', 1))  # Página actual (por defecto 1)
        page_size = int(request.args.get('page_size', 10))  # Tamaño de página (por defecto 10)

        logger.info(f"Aplicando paginación: página {page}, tamaño de página {page_size}")
        # Calcular índices para la paginación
        start = (page - 1) * page_size
        end = start + page_size

        # Obtener la página de pedidos
        pedidos_paginados = pedidos_resumen[start:end]

        logger.info(f"Se encontraron {len(pedidos_resumen)} pedidos en total. Retornando {len(pedidos_paginados)} pedidos para la página {page}")
        return jsonify({
            "total": len(pedidos_resumen),
            "pages": (len(pedidos_resumen) + page_size - 1) // page_size,  # Número total de páginas
            "current_page": page,
            "pedidos": pedidos_paginados
        }), 200

    except Exception as e:
        logger.error(f"Error procesando la solicitud para el cliente con ID {cliente_id}: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Error interno del servidor",
            "mensaje": "Ha ocurrido un error procesando su solicitud. Por favor, inténtelo más tarde.",
            "referencia": str(e)  # Puede ser un UUID o un mensaje de error para depuración
        }), 500