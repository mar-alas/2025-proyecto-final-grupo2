from flask import Blueprint, request, jsonify
from infraestructura.repositorio_entregas import RepositorioEntrega

ubicacion_pedido_bp = Blueprint('ubicacion_pedido', __name__)

@ubicacion_pedido_bp.route('/ubicaciones_pedido', methods=['GET'])
def consultar_ubicaciones_pedido():
    """Endpoint to retrieve the real-time location of a truck and client for a specific delivery."""
    cliente_id = request.args.get('cliente_id', type=int)
    entrega_id = request.args.get('entrega_id', type=int)
    contador = request.args.get('contador', type=int, default=1)

    if not cliente_id or not entrega_id:
        return jsonify({
            "error": "Parámetros faltantes",
            "message": "Debe proporcionar cliente_id y entrega_id válidos en la consulta"
        }), 400

    if contador < 1 or contador > 30:
        return jsonify({
            "error": "Valor de contador inválido",
            "message": "El contador debe estar entre 1 y 30"
        }), 400

    try:
        repositorio_entrega = RepositorioEntrega()
        entrega = repositorio_entrega.obtener_entrega_por_id(entrega_id)

        if not entrega or entrega["cliente_id"] != cliente_id:
            return jsonify({
                "error": "Entrega no encontrada",
                "message": f"No se encontró la entrega con ID {entrega_id} para el cliente con ID {cliente_id}"
            }), 404

        # Extract origin and destination coordinates
        origen = entrega["coordenadas_origen"]
        destino = entrega["coordenadas_destino"]

        # Convert coordinates to tuples of floats
        origen_lat, origen_lon = map(float, origen.split(','))
        destino_lat, destino_lon = map(float, destino.split(','))

        # Calculate deltas
        delta_lat = (destino_lat - origen_lat) / 30
        delta_lon = (destino_lon - origen_lon) / 30

        # Calculate current position based on contador
        current_lat = origen_lat + (contador * delta_lat)
        current_lon = origen_lon + (contador * delta_lon)

        # Build the response
        response = {
            "coordenadas_cliente": {
                "latitud": destino_lat,
                "longitud": destino_lon
            },
            "coordenadas_camion": {
                "latitud": current_lat,
                "longitud": current_lon
            }
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500