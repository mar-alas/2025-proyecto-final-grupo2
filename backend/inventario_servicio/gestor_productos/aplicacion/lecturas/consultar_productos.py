import math
from flask import Blueprint, jsonify, request
import logging
from dominio.get_all_products_service import GetAllProductsService
from dominio.product_repository import ProductRepository
from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage
from dominio.access_token_manager import AccessTokenValidator


logging.basicConfig(level=logging.INFO)
consultar_productos_bp = Blueprint('consultar_productos_bp', __name__)


@consultar_productos_bp.route('', methods=['GET'])
def consultar_productos():
    try:

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

        status = request.args.get("status")
        status_validation = _status_is_valid(status)
        if status_validation:
            return status_validation

        params = _params(request)
        get_all_products_service = GetAllProductsService(ProductRepository(db.session, Product, ProductImage), params)
        productos, total = get_all_products_service.ejecutar()
        
        limit = params["limit"]
        return jsonify({
            "total": total,
            "page": params["page"],
            "total_pages": math.ceil(total / limit) if limit else 1,
            "limit": limit,
            "products": [producto.to_dict() for producto in productos]
        }), 200

    except Exception as e:
        logging.error(f"Error al consultar productos: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de productos. Intente mas tarde."}), 500
    

def _status_is_valid(status):
    if status and status not in ["in_stock", "out_of_stock", "in_production", "en_stock", "agotado", "en_produccion"]:
        return jsonify({
            "message": "Parametros invalidos",
            "detalles": {"status": "El estado proporcionado no es valido"}
        }), 400
    return None


def _params(request):
    return {
            "code": request.args.get("code"),
            "name": request.args.get("name"),
            "status": request.args.get("status"),
            "page": int(request.args.get("page", 1)),
            "limit": int(request.args.get("limit", 20))
    }