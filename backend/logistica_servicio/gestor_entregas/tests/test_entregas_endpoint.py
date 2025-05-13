from datetime import datetime
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.entregas import consulta_entregas_bp

class TestConsultarEntregas(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(consulta_entregas_bp, url_prefix='/entregas')
        self.client = self.app.test_client()

    @patch("infraestructura.repositorio_entregas.RepositorioEntrega")
    def test_consultar_entregas_success(self, mock_repositorio_entrega):
        # Mock data
        mock_entregas = [
            MagicMock(
            id=1,
            cliente_id=123,
            fecha_entrega=datetime(2023, 10, 20).date(),
            hora_entrega=datetime(2023, 10, 20, 14, 30),
            cantidad=5,
            valor_total=100.0
            ),
            MagicMock(
            id=2,
            cliente_id=456,
            fecha_entrega=datetime(2023, 10, 16).date(),
            hora_entrega=datetime(2023, 10, 16, 10, 0),
            cantidad=3,
            valor_total=50.0
            )
        ]
        mock_repositorio = MagicMock()
        mock_repositorio.obtener_entregas.return_value = mock_entregas
        mock_repositorio_entrega.return_value = mock_repositorio

        # Make the request
        response = self.client.get('/entregas/', query_string={"cliente_id": 123})

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()

    def test_consultar_entregas_missing_cliente_id(self):
        # Make the request without cliente_id
        response = self.client.get('/entregas/')

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertEqual(response_data["error"], "Cliente ID es requerido")
        self.assertEqual(response_data["message"], "Debe proporcionar un cliente_id válido en la consulta")

    @patch("infraestructura.repositorio_entregas.RepositorioEntrega")
    def test_consultar_entregas_no_entregas_for_cliente(self, mock_repositorio_entrega):
        # Mock data
        mock_repositorio = MagicMock()
        mock_repositorio.obtener_entregas.return_value = []
        mock_repositorio_entrega.return_value = mock_repositorio

        # Make the request
        response = self.client.get('/entregas/', query_string={"cliente_id": 123})

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 0)
        self.assertEqual(len(response_data["entregas"]), 0)