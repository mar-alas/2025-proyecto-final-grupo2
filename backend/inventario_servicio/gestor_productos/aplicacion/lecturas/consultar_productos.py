from flask import Blueprint, jsonify
import logging
from dominio.get_all_products_service import GetAllProductsService
from infraestructura.get_all_products_repository import ProductoRepository


logging.basicConfig(level=logging.INFO)
consultar_productos_bp = Blueprint('consultar_productos_bp', __name__)


@consultar_productos_bp.route('', methods=['GET'])
def consultar_productos():
    try:
        get_all_products_service = GetAllProductsService(ProductoRepository())
        productos = get_all_products_service.ejecutar()
        return jsonify({
            "message": "Lista de productos recuperada exitosamente",
            "data": productos
        }), 200
    except Exception as e:
        logging.error(f"Error al consultar productos: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de productos. Intente mas tarde."}), 500