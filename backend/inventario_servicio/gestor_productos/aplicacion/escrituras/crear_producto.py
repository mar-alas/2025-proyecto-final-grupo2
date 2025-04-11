from flask import Blueprint, jsonify, request

crear_producto_bp = Blueprint('crear_producto_bp', __name__)

@crear_producto_bp.route('', methods=['POST'])
def crear_producto():
    try:
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
        return jsonify({"message": f"Error en registro. Intentre mas tarde. Error:{str(e)}"}), 500