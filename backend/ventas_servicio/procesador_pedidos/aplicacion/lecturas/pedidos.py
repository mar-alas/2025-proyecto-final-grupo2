from flask import Blueprint, jsonify, request
from infraestructura.repositorio import RepositorioPedidos

pedidos_lectura = Blueprint('pedidos_lectura', __name__)

repositorio = RepositorioPedidos(db_session=None)

@pedidos_lectura.route('/pedidos', methods=['GET'])
def obtener_pedidos():
    """
    Obtiene la lista de pedidos de un cliente con sus estados actuales.
    """
    cliente_id = request.args.get('cliente_id')  # Obtener el parámetro 'cliente_id' de la URL
    if not cliente_id:
        return jsonify({
            "error": "El parámetro 'cliente_id' es obligatorio",
            "mensaje": "Debe proporcionar un cliente_id para consultar los pedidos"
        }), 400

    try:
        # Obtener los pedidos del cliente
        pedidos = repositorio.obtener_por_cliente(cliente_id)
        if not pedidos:
            return jsonify({
                "error": "Cliente no encontrado",
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

        # Calcular índices para la paginación
        start = (page - 1) * page_size
        end = start + page_size

        # Obtener la página de pedidos
        pedidos_paginados = pedidos_resumen[start:end]

        return jsonify({
            "total": len(pedidos_resumen),
            "pages": (len(pedidos_resumen) + page_size - 1) // page_size,  # Número total de páginas
            "current_page": page,
            "pedidos": pedidos_paginados
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "mensaje": "Ha ocurrido un error procesando su solicitud. Por favor, inténtelo más tarde.",
            "referencia": str(e)  # Puede ser un UUID o un mensaje de error para depuración
        }), 500