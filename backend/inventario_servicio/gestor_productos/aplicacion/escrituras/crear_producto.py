from flask import Blueprint, jsonify, request
from dominio.access_token_manager import AccessTokenValidator
import logging


crear_producto_bp = Blueprint('crear_producto_bp', __name__)
logging.basicConfig(level=logging.INFO)

@crear_producto_bp.route('', methods=['POST'])
def crear_producto():
    try:
        logging.info("method: crear_producto()")
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
        
        
        return jsonify({
            "message": "Producto(es) registrado(s) exitosamente",
            "data": {
                "id": 1,
                "nombre": "Sal",
                "descripcion": "Sal refinada para consumo diario",
                "tiempo_entrega": "2 días",
                "precio": 50.0,
                "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
                "fecha_vencimiento": "2025-12-31",
                "estado": "en_stock",
                "inventario_inicial": 500,
                "imagenes_productos": ["sal1.jpg", "sal2.jpg"],
                "proveedor": "Proveedor Salinas S.A."
            }
        }), 201
    except Exception as e:
        logging.error("Excepcion ocurrida al crear prodcuto. method: crear_producto()")
        return jsonify({"message": f"Error en registro. Intentre mas tarde. Error:{str(e)}"}), 500