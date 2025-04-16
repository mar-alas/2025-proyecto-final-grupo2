from flask import Blueprint, jsonify
import logging
from dominio.get_all_products_service import GetAllProductsService
from dominio.product_repository import ProductRepository
from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage


logging.basicConfig(level=logging.INFO)
consultar_productos_bp = Blueprint('consultar_productos_bp', __name__)


@consultar_productos_bp.route('', methods=['GET'])
def consultar_productos():
    try:
        product_repository = ProductRepository(db.session, Product, ProductImage)
        get_all_products_service = GetAllProductsService(product_repository)
        productos = get_all_products_service.ejecutar()
        productos_dict = [producto.to_dict() for producto in productos]
        return jsonify({
            "message": "Lista de productos recuperada exitosamente",
            "data": productos_dict
        }), 200
    except Exception as e:
        logging.error(f"Error al consultar productos: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de productos. Intente mas tarde."}), 500