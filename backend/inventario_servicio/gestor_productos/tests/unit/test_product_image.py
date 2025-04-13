import unittest
from dominio.product_image import ProductImage  # Ajusta si es necesario


class TestProductImage(unittest.TestCase):
    def test_to_dict_returns_expected_dict(self):
        image = ProductImage(
            imagen_url="http://example.com/image.jpg",
            producto_id=1
        )
        image.id = 99  # Simular ID como si lo asignara la DB

        result = image.to_dict()

        expected = {
            "id": 99,
            "imagen_url": "http://example.com/image.jpg"
        }

        self.assertEqual(result, expected)
