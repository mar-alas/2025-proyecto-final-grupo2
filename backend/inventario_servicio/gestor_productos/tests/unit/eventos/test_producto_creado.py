import unittest
from  dominio.eventos.producto_creado import ProductoCreado

class TestProductoCreado(unittest.TestCase):

    def test_init_sets_attributes_correctly(self):
        evento = ProductoCreado(producto_id=10, inventario_inicial=50)

        self.assertEqual(evento.producto_id, 10)
        self.assertEqual(evento.inventario_inicial, 50)

    def test_to_dict_returns_expected_dict(self):
        evento = ProductoCreado(producto_id=99, inventario_inicial=200)

        expected_dict = {
            "producto_id": 99,
            "inventario_inicial": 200
        }

        self.assertEqual(evento.to_dict(), expected_dict)

