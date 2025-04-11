import unittest
from unittest.mock import patch, MagicMock
from flask import jsonify
from dominio.reglas_negocio import validar_cliente, validar_productos

from flask import Flask

class TestReglasNegocio(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

    @patch('dominio.reglas_negocio.requests.get')
    def test_validar_cliente_existe(self, mock_get):
        # Mock response for existing client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "clientes": [{"id": 1, "nombre": "Cliente 1"}]
        }
        mock_get.return_value = mock_response

        cliente_id = 1
        token = "valid_token"
        response = validar_cliente(cliente_id, token)
        self.assertEqual(response, None)

    @patch('dominio.reglas_negocio.requests.get')
    def test_validar_cliente_no_existe(self, mock_get):
        # Mock response for non-existing client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "clientes": [{"id": 2, "nombre": "Cliente 2"}]  # Mock a different client ID
        }
        mock_get.return_value = mock_response

        cliente_id = 1  # This client ID does not exist in the mocked response
        token = "valid_token"

        with self.app.app_context():  # Ensure the test runs within the application context
            response = validar_cliente(cliente_id, token)
            self.assertIsNotNone(response)

    @patch('dominio.reglas_negocio.requests.get')
    def test_validar_productos_existen(self, mock_get):
        # Mock response for existing products
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "inventario": 350,
                "nombre": "Frijoles",
                "precio": 90.0,
                "producto_id": 5
            },
            {
                "inventario": 500,
                "nombre": "Sal",
                "precio": 50.0,
                "producto_id": 1
            },
            {
                "inventario": 300,
                "nombre": "Arroz",
                "precio": 120.0,
                "producto_id": 2
            },
            {
                "inventario": 400,
                "nombre": "Azúcar",
                "precio": 80.0,
                "producto_id": 3
            },
            {
                "inventario": 250,
                "nombre": "Aceite",
                "precio": 150.0,
                "producto_id": 4
            }
        ]
        mock_get.return_value = mock_response

        token = "valid_token"
        productos = [{"id_producto": 1}, {"id_producto": 2}]

        with self.app.app_context():  # Ensure the test runs within the application context
            response = validar_productos(token, productos)
            self.assertIsNone(response)  # No errors should be returned

    @patch('dominio.reglas_negocio.requests.get')
    def test_validar_productos_no_existen(self, mock_get):
        # Mock response for non-existing products
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "inventario": 350,
                "nombre": "Frijoles",
                "precio": 90.0,
                "producto_id": 5
            }
        ]
        mock_get.return_value = mock_response

        token = "valid_token"
        productos = [{"id_producto": 1}, {"id_producto": 2}]

        with self.app.app_context():  # Ensure the test runs within the application context
            response = validar_productos(token, productos)
            self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()