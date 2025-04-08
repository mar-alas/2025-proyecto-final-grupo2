from flask import Blueprint, jsonify, request
from infraestructura.repositorio import RepositorioStock
import logging
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

stock_bp = Blueprint('stock', __name__)
db_session = None
repositorio = RepositorioStock(db_session)

@stock_bp.route('/productos', methods=['GET'])
def obtener_inventario():
    logging.info("Obteniendo inventario de productos, validando el token")
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "No se proporcionó un token"}), 401

    token = auth_header.split(" ")[1]
    validation_result = validar_token(token=token)

    if not validation_result:
         return jsonify({"message": "forbidden"}), 403

    inventario = repositorio.obtener_inventario()
    return jsonify([
        {"producto_id": stock.producto_id, "inventario": stock.inventario, "nombre": stock.producto_nombre}
        for stock in inventario
    ])