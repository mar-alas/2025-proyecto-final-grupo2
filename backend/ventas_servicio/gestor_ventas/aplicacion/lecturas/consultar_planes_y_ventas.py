from flask import Blueprint, request, jsonify
import logging
from infraestructura.repositorio import RepositorioMetasPlanes
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

reporte_metas_planes_bp = Blueprint('reporte_metas_planes', __name__)
logger = logging.getLogger(__name__)

@reporte_metas_planes_bp.route('', methods=['GET'])
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
        repositorio = RepositorioMetasPlanes()
        metas = repositorio.generar_metas_ventas()
        planes = repositorio.generar_planes_ventas()
        
        return {
                "metas": metas,
                "planes": planes
            }, 200
        
    except Exception as e:
        logging.error(f"Error al consultar reporte de planes y metas: {str(e)}")
        return jsonify({"message": f"Error al consultar reporte de planes y metas. Intente mas tarde."}), 500