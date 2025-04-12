from dominio.reglas_negocio_crear_producto import (
    _validar_campos_requeridos_producto,
    _validar_limite_productos,
    validar_datos_producto
)

class TestReglasNegocioProducto:

    def test_deberia_validar_campos_correctamente(self):
        producto = {
            "nombre": "Producto Test",
            "descripcion": "Desc",
            "tiempo_entrega": "1 día",
            "precio": 100.0,
            "condiciones_almacenamiento": "Fresco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 10,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor S.A."
        }
        assert _validar_campos_requeridos_producto(producto) is None

    def test_deberia_fallar_si_falta_campo(self):
        producto = {
            # Falta 'nombre'
            "descripcion": "Desc",
            "tiempo_entrega": "1 día",
            "precio": 100.0,
            "condiciones_almacenamiento": "Fresco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 10,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor S.A."
        }
        msg = _validar_campos_requeridos_producto(producto)
        assert "nombre" in msg

    def test_deberia_fallar_si_excede_limite(self):
        productos = [{}] * 101  # Productos vacíos
        msg = _validar_limite_productos(productos)
        assert "El registro masivo no puede exceder 100 productos por solicitud" in msg

    def test_deberia_validar_lista_correcta_de_productos(self):
        productos = [{
            "nombre": "Prod",
            "descripcion": "Desc",
            "tiempo_entrega": "2 días",
            "precio": 10.0,
            "condiciones_almacenamiento": "Seco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 10,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor"
        }]
        assert validar_datos_producto(productos) is None


    def test_deberia_fallar_si_no_es_lista(self):
        assert validar_datos_producto({"nombre": "Producto"}) == "Se esperaba una lista de productos."


    def test_deberia_validar_lista_de_multiples_productos_correctos(self):
        productos = [{
            "nombre": f"Prod {i}",
            "descripcion": "Desc",
            "tiempo_entrega": "2 días",
            "precio": 10.0,
            "condiciones_almacenamiento": "Seco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 10,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor"
        } for i in range(5)]  # Menos de 100

        assert validar_datos_producto(productos) is None


    def test_deberia_fallar_si_lista_correcta_supera_limite(self):
        productos = [{
            "nombre": f"Prod {i}",
            "descripcion": "Desc",
            "tiempo_entrega": "2 días",
            "precio": 10.0,
            "condiciones_almacenamiento": "Seco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 10,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor"
        } for i in range(101)]

        msg = validar_datos_producto(productos)
        assert msg == "El registro masivo no puede exceder 100 productos por solicitud"
