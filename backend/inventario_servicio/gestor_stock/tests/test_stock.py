import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.stock import stock_bp
from infraestructura.repositorio import RepositorioStock

class TestStockLecturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(stock_bp)
        cls.client = cls.app.test_client()

    @patch('aplicacion.lecturas.stock.validar_token')
    @patch('infraestructura.repositorio.RepositorioStock.obtener_inventario')
    def test_obtener_inventario_exitoso(self, mock_obtener_inventario, mock_validar_token):
        # Mock token validation
        mock_validar_token.return_value = True

        # Mock inventory data
        mock_obtener_inventario.return_value = [
            MagicMock(producto_id=1, inventario=10, producto_nombre="Producto 1", producto_precio=50.0),
            MagicMock(producto_id=2, inventario=5, producto_nombre="Producto 2", producto_precio=120.0)
        ]

        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.get('/productos', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['producto_id'], 1)
        self.assertEqual(data[0]['inventario'], 10)
        self.assertEqual(data[0]['nombre'], "Producto 1")
        self.assertEqual(data[0]['precio'], 50.0)
        self.assertEqual(data[1]['producto_id'], 2)
        self.assertEqual(data[1]['inventario'], 5)
        self.assertEqual(data[1]['nombre'], "Producto 2")
        self.assertEqual(data[1]['precio'], 120.0)

    @patch('aplicacion.lecturas.stock.validar_token')
    def test_obtener_inventario_sin_token(self, mock_validar_token):
        headers = {}  # No Authorization header
        response = self.client.get('/productos', headers=headers)

        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No se proporcionó un token")

    @patch('aplicacion.lecturas.stock.validar_token')
    def test_obtener_inventario_token_invalido(self, mock_validar_token):
        # Mock token validation to fail
        mock_validar_token.return_value = False

        headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get('/productos', headers=headers)

        self.assertEqual(response.status_code, 403)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "forbidden")

    @patch('aplicacion.lecturas.stock.validar_token')
    @patch('infraestructura.repositorio.RepositorioStock.obtener_inventario')
    def test_obtener_inventario_vacio(self, mock_obtener_inventario, mock_validar_token):
        # Mock token validation
        mock_validar_token.return_value = True

        # Mock empty inventory data
        mock_obtener_inventario.return_value = []

        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.get('/productos', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()