import unittest
from datetime import date
from unittest.mock import MagicMock

from dominio.product import Product


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
