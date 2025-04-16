import unittest
from infraestructura.get_all_products_repository import ProductoRepository

class TestProductoRepository(unittest.TestCase):
    def setUp(self):
        """Inicializa el repositorio sin mocks"""
        self.producto_repository = ProductoRepository()

    def test_obtener_todos_success(self):
        """Verifica que obtener_todos devuelve al menos un producto con la estructura esperada"""
        result = self.producto_repository.obtener_todos()

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        producto = result[0]
        self.assertIn("id", producto)
        self.assertIn("nombre", producto)
        self.assertIn("descripcion", producto)
        self.assertIn("tiempo_entrega", producto)
        self.assertIn("precio", producto)
        self.assertIn("condiciones_almacenamiento", producto)
        self.assertIn("fecha_vencimiento", producto)
        self.assertIn("estado", producto)
        self.assertIn("inventario_inicial", producto)
        self.assertIn("imagenes_productos", producto)
        self.assertIn("proveedor", producto)

    def test_obtener_todos_no_vacio(self):
        """Verifica que la lista no esté vacía"""
        result = self.producto_repository.obtener_todos()
        self.assertTrue(len(result) > 0)
