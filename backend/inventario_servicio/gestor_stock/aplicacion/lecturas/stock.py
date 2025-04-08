from flask import Blueprint, jsonify
from infraestructura.repositorio import RepositorioStock
from sqlalchemy.orm import Session

stock_bp = Blueprint('stock', __name__)
db_session = None
repositorio = RepositorioStock(db_session)

@stock_bp.route('/productos', methods=['GET'])
def obtener_inventario():
    inventario = repositorio.obtener_inventario()
    return jsonify([
        {"producto_id": stock.producto_id, "inventario": stock.inventario, "nombre": stock.producto_nombre}
        for stock in inventario
    ])