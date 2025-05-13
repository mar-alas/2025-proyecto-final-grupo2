from flask import Blueprint, jsonify, request
from infraestructura.repositorio_camion import RepositorioCamion
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas
from datetime import datetime

asignar_ruta_bp = Blueprint('asignar_ruta', __name__)

@asignar_ruta_bp.route('/asignar_ruta', methods=['POST'])
def asignar_ruta():
    """Endpoint to assign routes to trucks based on the given date."""
    try:
        # Get the 'fecha' parameter from the request
        fecha = request.json.get('fecha')
        if not fecha:
            return jsonify({
                "error": "El parámetro 'fecha' es requerido."
            }), 400

        # Validate the date format
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "error": "Formato de fecha inválido. Use el formato YYYY-MM-DD."
            }), 400

        # Initialize repositories
        repositorio_camion = RepositorioCamion()
        repositorio_entrega_programada = RepositorioEntregasProgramadas()

        # Get all trucks
        camiones = repositorio_camion.obtener_camiones()
        if not camiones:
            return jsonify({
                "error": "No hay camiones disponibles."
            }), 404

        # Iterate over all trucks and check for scheduled deliveries
        mensajes = []
        for camion in camiones:
            entregas_programadas = repositorio_entrega_programada.obtener_entregas_programadas_por_fecha_camion(fecha, camion['id'])
            if entregas_programadas:
                # Update the status of the scheduled delivery to "Enrutado"
                for entrega in entregas_programadas:
                    repositorio_entrega_programada.actualizar_entrega_programada(entrega.id, {"estado": "Enrutado"})
                mensajes.append(f"Camión {camion['id']} actualizado a 'Enrutado'.")
            else:
                mensajes.append(f"No hay entregas programadas asociadas a esta fecha {fecha} para el camión {camion['id']}.")

        # Return the response
        return jsonify({
            "mensajes": mensajes
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500