from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from infraestructura.repositorio import RepositorioReporteClientes
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

reporte_clientes_ventas_bp = Blueprint('reporte_clientes_ventas', __name__)
logger = logging.getLogger(__name__)

@reporte_clientes_ventas_bp.route('', methods=['GET'])
def reporte_clientes_ventas():
    try:
        """ Seguridad """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "No se proporcionó un token"}), 401

        token = auth_header.split(" ")[1]
        validation_result = validar_token(token=token)

        if not validation_result:
            return jsonify({"message": "forbidden"}), 403
        
        """ Filtros opcionales """
        vendedor_id = request.args.get('vendedor', type=int)
        zona = request.args.get('zona')
        producto_id = request.args.get('producto')

        """ Procesamiento """
        reporte_clientes_ventas = RepositorioReporteClientes()
        fallback = False

        clientes_con_ventas = reporte_clientes_ventas.obtener_clientes_con_ventas(
            vendedor_id=vendedor_id,
            zona=zona,
            producto_id=producto_id
        )

        """ Fallback """
        if clientes_con_ventas is None or clientes_con_ventas == [] or len(clientes_con_ventas) == 0:
            clientes_con_ventas = reporte_clientes_ventas.obtener_clientes_con_ventas_fallback()
            fallback = True
        
        return jsonify({
                "clientes": clientes_con_ventas,
                "fallback": fallback
            }), 200

    except Exception as e:
        logging.error(f"Error al consultar reporte de clientes con ventas: {str(e)}")
        return jsonify({"message": f"Error al consultar reporte de clientes con ventas. Intente mas tarde."}), 500