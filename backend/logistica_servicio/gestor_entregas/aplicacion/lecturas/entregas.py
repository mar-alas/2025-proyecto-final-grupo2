from flask import Blueprint, request, jsonify
from infraestructura.repositorio_entregas import RepositorioEntrega
from datetime import datetime

consulta_entregas_bp = Blueprint('consulta_entregas', __name__)

@consulta_entregas_bp.route('/', methods=['GET'])
def consultar_entregas():
    """Endpoint to retrieve deliveries for a specific client."""
    cliente_id = request.args.get('cliente_id', type=int)
    if not cliente_id:
        return jsonify({
            "error": "Cliente ID es requerido",
            "message": "Debe proporcionar un cliente_id válido en la consulta"
        }), 400

    try:
        repositorio = RepositorioEntrega()
        entregas = repositorio.obtener_entregas()
        entregas_cliente = [entrega for entrega in entregas if entrega['cliente_id'] == cliente_id]

        if not entregas_cliente:
            entregas_cliente = []

        entregas_response = []
        for entrega in entregas_cliente:
            if entrega["fecha_entrega"] > datetime.now().date():
                entrega_data = {
                    "id": entrega["id"],
                    "fecha_entrega": entrega["fecha_entrega"].strftime('%y-%m-%d'),
                    "hora_entrega": entrega["hora_entrega"].strftime('%H:%M'),
                    "cantidad_productos": entrega["cantidad"],
                    "valor_total": entrega["valor_total"]
                }
                entregas_response.append(entrega_data)
        response = {
            "total": len(entregas_response),
            "pages": 1,  # Pagination can be added later
            "current_page": 1,
            "entregas": entregas_response
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "message": str(e)
        }), 500