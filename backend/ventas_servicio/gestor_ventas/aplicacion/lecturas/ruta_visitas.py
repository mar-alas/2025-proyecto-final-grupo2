from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from infraestructura.repositorio import RutasVisitas
from infraestructura.schema import RutaVisitasInputSchema
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

ruta_visitas_bp = Blueprint('ruta_visitas', __name__)
logger = logging.getLogger(__name__)

@ruta_visitas_bp.route('/ruta_visita', methods=['GET'])
def consultar_ruta_visita():
    """Endpoint to retrieve the visit route for a specific vendor and date."""

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No se proporcionó un token"}), 401

    token = auth_header.split(" ")[1]
    validation_result = validar_token(token=token)

    if not validation_result:
         return jsonify({"message": "forbidden"}), 403
    
    vendedor_id = request.args.get('vendedor_id', type=int)
    fecha = request.args.get('fecha', type=str)

    if not vendedor_id or not fecha:
        return jsonify({
            "error": "Parámetros inválidos",
            "detalles": "Se requieren vendedor_id y fecha en el formato YYYY-MM-DD"
        }), 400

    try:
        # Validate date format
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "error": "Formato de fecha inválido",
            "detalles": "La fecha debe estar en el formato YYYY-MM-DD"
        }), 400

    # Retrieve data from the database
    repo = RutasVisitas()
    visitas = repo.obtener_rutas_por_vendedor_y_fecha(vendedor_id, fecha)

    if not visitas:
        return jsonify({
            "error": "Ruta no encontrada",
            "detalles": f"No se encontró una ruta para el vendedor {vendedor_id} en la fecha {fecha}"
        }), 404

    # Serialize the data using the schema
    schema = RutaVisitasInputSchema(many=True)
    visitas_serializadas = schema.dump(visitas)
    # Transform the serialized data to match the example output
    visitas_transformadas = [
        {
            "cliente_id": visita["cliente_id"],
            "nombre_cliente": visita["nombre_cliente"],
            "barrio": visita["barrio"],
            "fecha_completa": visita["fecha"],
            "trayecto": visita["tiempo_estimado"],
        }
        for visita in visitas_serializadas
    ]
    return jsonify({"ruta_visita": visitas_transformadas}), 200