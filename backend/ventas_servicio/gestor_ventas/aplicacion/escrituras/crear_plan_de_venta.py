from flask import Blueprint, jsonify, request
from dominio.access_token_manager import AccessTokenValidator
from infraestructura.repositorio import RepositorioPlanesVenta
from dominio.planes_venta_a_entidades import convertir_json_a_entidades_de_dominio

crear_plan_venta_bp = Blueprint('crear_plan_venta_bp', __name__)


@crear_plan_venta_bp.route('', methods=['PUT'])
def crear_plan_venta():
    try:
        """ Seguridad """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"status": "FAILED", "message": "No se proporciono un token"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"status": "FAILED", "message": "Formato del token invalido"}), 401

        validator = AccessTokenValidator()
        es_valido, mensaje = validator.validate(token)

        if not es_valido:
            return jsonify({"status": "FAILED", "message": mensaje}), 403
        
        if not request.is_json:
            return jsonify({"status": "FAILED", "message": "Se requiere un cuerpo con formato JSON"}), 400
        

        data = request.get_json()
        lista_vendedores = None

        if "vendedores" in data and isinstance(data["vendedores"], list):
            lista_vendedores = data["vendedores"]
        elif "id" in data and "metas" in data:
            lista_vendedores = [data]
        else:
            return jsonify({"mensaje": "Formato de datos invalido"}), 400


        """ Procesamiento """
        repositorioPlanesVenta = RepositorioPlanesVenta()

        for vendedor in lista_vendedores:
            vendedor_id = vendedor.get("id")
            metas = vendedor.get("metas")

            if vendedor_id is None or metas is None:
                return jsonify({"mensaje": "Error de validacion en los datos enviados."}), 400

            entidades_plan_venta = convertir_json_a_entidades_de_dominio(vendedor_id, metas)
            for plan_venta in entidades_plan_venta:
                repositorioPlanesVenta.guardar_o_actualizar(plan_venta)
        
        return jsonify({"mensaje": "Planes de venta registrados exitosamente."}), 200

    except Exception as e:
        return jsonify({"message": f"Error interno del servidor al procesar la solicitud. Intente mas tarde. Error:{str(e)}"}), 500

