from flask import Blueprint, request, jsonify
import logging
from infraestructura.repositorio import RepositorioReporteVentasHistorico
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

reporte_historico_ventas_bp = Blueprint('reporte_historico_ventas', __name__)
logger = logging.getLogger(__name__)

@reporte_historico_ventas_bp.route('', methods=['GET'])
def reporte_historico_ventas():
    try:
        """ Seguridad """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "No se proporcionó un token"}), 401

        token = auth_header.split(" ")[1]
        validation_result = validar_token(token=token)

        if not validation_result:
            return jsonify({"message": "forbidden"}), 403
        

        """ Procesamiento """
        repositorio = RepositorioReporteVentasHistorico()
        total, datos_mensuales, total_fallback, datos_mensuales_fallback = repositorio.obtener_reporte_ventas_historico()
        
        return {
                "historico_ventas": {
                    "total": total,
                    "datos_mensuales": datos_mensuales
                },
                "historico_ventas_fallback": {
                    "total": total_fallback,
                    "datos_mensuales": datos_mensuales_fallback
                }
            }, 200

    except Exception as e:
        logging.error(f"Error al consultar reporte historico de ventas: {str(e)}")
        return jsonify({"message": f"Error al consultar reporte historico de ventas. Intente mas tarde."}), 500