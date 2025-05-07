from flask import Blueprint, request, jsonify
from infraestructura.repositorio_entregas import RepositorioDetalleEntrega, RepositorioEntrega
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas, RepositorioEntregaProgramadasDetalle
from infraestructura.repositorio_camion import RepositorioCamion
from haversine import haversine, Unit

entrega_detallada_bp = Blueprint('entrega_detallada', __name__)

@entrega_detallada_bp.route('/detalle', methods=['GET'])
def consultar_entrega_detallada():
    """Endpoint to retrieve detailed information for a specific delivery."""
    entrega_id = request.args.get('entrega_id', type=int)
    if not entrega_id:
        return jsonify({
            "error": "Entrega ID es requerido",
            "message": "Debe proporcionar un entrega_id válido en la consulta"
        }), 400

    try:
        repositorio_entrega = RepositorioEntrega()
        repositorio_entrega_programada = RepositorioEntregasProgramadas()
        repositorio_entrega_detalle = RepositorioDetalleEntrega()
        repositorio_camion = RepositorioCamion()
        
        entrega = repositorio_entrega.obtener_entrega_por_id(entrega_id)
        # entrega_programada = repositorio_entrega_programada.obtener_entrega_programada_por_id(entrega_id)
        entrega_detalle = repositorio_entrega_detalle.obtener_detalles_por_entrega(entrega_id)


        if not entrega_detalle:
            return jsonify({
                "error": "Entrega no encontrada",
                "message": f"No se encontró la entrega con ID {entrega_id}"
            }), 404
        
        # calcular distancia entre dos puntos
        destino = entrega["coordenadas_destino"]
        destino_tuple = tuple(map(float, destino.split(',')))
        origen = entrega["coordenadas_origen"]
        origen_tuple = tuple(map(float, origen.split(',')))
        # Calculate distance in kilometers
        distance = haversine(origen_tuple, destino_tuple, unit=Unit.KILOMETERS)
        distancia = f"{round(distance, 1)} km"
        tiempo_horas = round(distance / 60, 1)
        if tiempo_horas < 1:
            tiempo_minutos = round(distance / (60 / 60))  # Convert to minutes
            tiempo_estimado = f"{tiempo_minutos} minutos"
        else:
            tiempo_estimado = f"{tiempo_horas} horas"  # Assuming an average speed of 60 km/h
        camion = repositorio_camion.obtener_camion_por_id(entrega_detalle[0]['camion_id'])
        entregas_programadas = repositorio_entrega_programada.obtener_entregas_programadas_por_fecha_camion(entrega["fecha_entrega"], camion['id'])
        entrega_detallada = {
            "placas_vehiculo": camion['placa'],
            "pedidos_anteriores": len(entregas_programadas),
            "distancia_restante": distancia,
            "tiempo_estimado": tiempo_estimado,
            "cliente_id": entrega['cliente_id'],
            "pedido_id": entrega["pedido_id"]
        }

        return jsonify(entrega_detallada), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500