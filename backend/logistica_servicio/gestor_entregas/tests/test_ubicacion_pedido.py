import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.ubicacion_pedido import ubicacion_pedido_bp

class TestConsultarUbicacionesPedido(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(ubicacion_pedido_bp)
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.ubicacion_pedido.RepositorioEntrega")
    def test_consultar_ubicaciones_pedido_success(self, mock_repositorio_entrega):
        # Mock data
        mock_entrega = {
            "cliente_id": 1,
            "coordenadas_origen": "10.0,20.0",
            "coordenadas_destino": "40.0,60.0"
        }
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.return_value = mock_entrega

        # Make a GET request
        response = self.client.get('/ubicaciones_pedido?cliente_id=1&entrega_id=1&contador=15')

        # Assertions
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("coordenadas_cliente", data)
        self.assertIn("coordenadas_camion", data)
        self.assertAlmostEqual(data["coordenadas_camion"]["latitud"], 25.0)
        self.assertAlmostEqual(data["coordenadas_camion"]["longitud"], 40.0)

    def test_consultar_ubicaciones_pedido_missing_params(self):
        # Make a GET request without required parameters
        response = self.client.get('/ubicaciones_pedido')

        # Assertions
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Parámetros faltantes")

    def test_consultar_ubicaciones_pedido_invalid_contador(self):
        # Make a GET request with invalid contador
        response = self.client.get('/ubicaciones_pedido?cliente_id=1&entrega_id=1&contador=50')

        # Assertions
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Valor de contador inválido")

    @patch("aplicacion.lecturas.ubicacion_pedido.RepositorioEntrega")
    def test_consultar_ubicaciones_pedido_entrega_not_found(self, mock_repositorio_entrega):
        # Mock no entrega found
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.return_value = None

        # Make a GET request
        response = self.client.get('/ubicaciones_pedido?cliente_id=1&entrega_id=1&contador=1')

        # Assertions
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Entrega no encontrada")

    @patch("aplicacion.lecturas.ubicacion_pedido.RepositorioEntrega")
    def test_consultar_ubicaciones_pedido_internal_error(self, mock_repositorio_entrega):
        # Mock an exception
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.side_effect = Exception("Database error")

        # Make a GET request
        response = self.client.get('/ubicaciones_pedido?cliente_id=1&entrega_id=1&contador=1')

        # Assertions
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertEqual(data["error"], "Error interno del servidor")
        self.assertEqual(data["message"], "Database error")