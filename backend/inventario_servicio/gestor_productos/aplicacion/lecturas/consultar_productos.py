from flask import Blueprint, jsonify
import logging

logging.basicConfig(level=logging.INFO)
consultar_productos_bp = Blueprint('consultar_productos_bp', __name__)

@consultar_productos_bp.route('', methods=['GET'])
def consultar_productos():
    try:
        productos = [
                {
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
        ]
        return jsonify({
            "message": "Lista de productos recuperada exitosamente",
            "data": productos
        }), 200
    except Exception as e:
        logging.error(f"Error al consultar productos: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de productos. Intente mas tarde."}), 500