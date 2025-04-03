from flask import Blueprint, jsonify

productos_lectura = Blueprint('productos_lectura', __name__)

@productos_lectura.route('/productos', methods=['GET'])
def obtener_productos():
    # Mock data following the ProductoResponse schema
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
        },
        {
            "id": 2,
            "nombre": "Arroz",
            "descripcion": "Arroz blanco de grano largo",
            "tiempo_entrega": "3 días",
            "precio": 120.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 300,
            "imagenes_productos": ["arroz1.jpg", "arroz2.jpg"],
            "proveedor": "Proveedor Arrocero S.A."
        },
        {
            "id": 3,
            "nombre": "Azúcar",
            "descripcion": "Azúcar blanca refinada",
            "tiempo_entrega": "2 días",
            "precio": 80.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 400,
            "imagenes_productos": ["azucar1.jpg", "azucar2.jpg"],
            "proveedor": "Proveedor Dulce S.A."
        },
        {
            "id": 4,
            "nombre": "Aceite",
            "descripcion": "Aceite vegetal para cocinar",
            "tiempo_entrega": "4 días",
            "precio": 150.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 250,
            "imagenes_productos": ["aceite1.jpg", "aceite2.jpg"],
            "proveedor": "Proveedor Oleico S.A."
        },
        {
            "id": 5,
            "nombre": "Frijoles",
            "descripcion": "Frijoles negros empaquetados",
            "tiempo_entrega": "3 días",
            "precio": 90.0,
            "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 350,
            "imagenes_productos": ["frijoles1.jpg", "frijoles2.jpg"],
            "proveedor": "Proveedor Legumbres S.A."
        }
    ]
    return jsonify(productos), 200