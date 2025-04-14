import unittest
from datetime import date
from unittest.mock import MagicMock

from dominio.product import Product
from dominio.eventos.producto_creado import ProductoCreado


class TestProduct(unittest.TestCase):

    def test_to_dict_returns_expected_structure(self):
        # Mock de imagen asociada
        mock_image = MagicMock()
        mock_image.to_dict.return_value = {"id": 1, "imagen_url": "http://img.com/1.jpg"}

        # Crear producto con datos fijos
        producto = Product(
            nombre="Producto de prueba",
            descripcion="Descripción de prueba",
            tiempo_entrega="3 días",
            precio=199.99,
            condiciones_almacenamiento="Lugar seco",
            fecha_vencimiento=date(2025, 12, 31),
            estado="en_stock",
            inventario_inicial=100,
            proveedor="Proveedor X",
            imagenes_productos=[mock_image]
        )

        producto.id = 123  # Simulamos un ID como si lo hubiera asignado SQLAlchemy

        expected_dict = {
            "id": 123,
            "nombre": "Producto de prueba",
            "descripcion": "Descripción de prueba",
            "tiempo_entrega": "3 días",
            "precio": 199.99,
            "condiciones_almacenamiento": "Lugar seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 100,
            "proveedor": "Proveedor X",
            "imagenes_productos": [{"id": 1, "imagen_url": "http://img.com/1.jpg"}]
        }

        self.assertEqual(producto.to_dict(), expected_dict)

    def test_to_dict_handles_no_fecha_vencimiento_and_no_images(self):
        producto = Product(
            nombre="Producto sin fecha",
            descripcion=None,
            tiempo_entrega=None,
            precio=10.5,
            condiciones_almacenamiento=None,
            fecha_vencimiento=None,
            estado="agotado",
            inventario_inicial=0,
            proveedor=None,
            imagenes_productos=None
        )
        producto.id = 456

        result = producto.to_dict()

        self.assertEqual(result["fecha_vencimiento"], None)
        self.assertEqual(result["imagenes_productos"], [])
        self.assertEqual(result["id"], 456)
        self.assertEqual(result["estado"], "agotado")

    def test_created_product_event_returns_expected_event_without_db_dependency(self):
        class DummyProduct:
            id = 789
            inventario_inicial = 50

            def created_product_event(self):
                return ProductoCreado(
                    producto_id=self.id,
                    inventario_inicial=self.inventario_inicial
                )

        dummy = DummyProduct()
        evento = dummy.created_product_event()

        self.assertIsInstance(evento, ProductoCreado)
        self.assertEqual(evento.producto_id, 789)
        self.assertEqual(evento.inventario_inicial, 50)


    def test_created_product_event_returns_expected_event(self):
        # Creamos un producto simulando la mínima estructura sin usar la BD real
        producto = Product(
            nombre="Producto X",
            descripcion="Desc",
            tiempo_entrega="5 días",
            precio=100.0,
            condiciones_almacenamiento="Fresco",
            fecha_vencimiento=None,
            estado="disponible",
            inventario_inicial=20,
            proveedor="Proveedor Y",
            imagenes_productos=[]
        )
        producto.id = 99  # Simulamos ID manualmente

        evento = producto.created_product_event()

        self.assertEqual(evento.producto_id, 99)
        self.assertEqual(evento.inventario_inicial, 20)
        self.assertEqual(evento.to_dict(), {
            "producto_id": 99,
            "inventario_inicial": 20
        })
