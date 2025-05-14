from flask import Blueprint, jsonify
from infraestructura.repositorio_camion import RepositorioCamion
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas
from flask import request
from datetime import datetime

consulta_camiones_bp = Blueprint('consulta_camiones', __name__)

@consulta_camiones_bp.route('/ruta_camiones', methods=['GET'])
def consultar_camiones():
    """Endpoint to retrieve all trucks."""
    try:
        fecha = request.args.get('fecha')
        if not fecha:
            fecha = datetime.today().strftime('%Y-%m-%d')
        if fecha:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    "error": "Formato de fecha inválido. Use el formato YYYY-MM-DD."
                }), 400
        repositorio = RepositorioCamion()
        camiones = repositorio.obtener_camiones()

        # get entregas programadas por camion por fecha
        repositorio_entrega_programada = RepositorioEntregasProgramadas()

        if not camiones:
            camiones = []

        camiones_response = []
        for camion in camiones:
            camion_data = {
                "id": camion["id"],
                "placa": camion["placa"],
                "marca": camion["marca"],
                "modelo": camion["modelo"],
                "capacidad_carga_toneladas": camion["capacidad_carga_toneladas"],
                "volumen_carga_metros_cubicos": camion["volumen_carga_metros_cubicos"]
            }
            entrega_programada = repositorio_entrega_programada.obtener_entregas_programadas_por_fecha_camion(fecha, camion['id'])
            camion_data["estado_enrutamiento"] = entrega_programada[0].estado if entrega_programada else "Sin entregas programadas"
            camiones_response.append(camion_data)

        response = {
            "total": len(camiones_response),
            "camiones": camiones_response
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500