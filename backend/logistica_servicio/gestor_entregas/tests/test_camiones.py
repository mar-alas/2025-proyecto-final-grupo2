import unittest
from unittest.mock import patch, MagicMock
from aplicacion.lecturas.camiones import consulta_camiones_bp
from flask import Flask

class TestConsultarCamiones(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(consulta_camiones_bp, url_prefix='/')
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.camiones.RepositorioCamion")
    @patch("aplicacion.lecturas.camiones.jsonify")
    def test_consultar_camiones_success(self, mock_jsonify, mock_repositorio_camion):
        # Mock data
        mock_camiones = [
            {
                "id": 1,
                "placa": "ABC123",
                "marca": "Marca1",
                "modelo": "Modelo1",
                "capacidad_carga_toneladas": 10,
                "volumen_carga_metros_cubicos": 20
            },
            {
                "id": 2,
                "placa": "DEF456",
                "marca": "Marca2",
                "modelo": "Modelo2",
                "capacidad_carga_toneladas": 15,
                "volumen_carga_metros_cubicos": 25
            }
        ]
        mock_repositorio_instance = MagicMock()
        mock_repositorio_instance.obtener_camiones.return_value = mock_camiones
        mock_repositorio_camion.return_value = mock_repositorio_instance

        mock_jsonify.side_effect = lambda x: x  # Mock jsonify to return the input directly

        # Call the function
        response = self.client.get('/camiones')

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 2)
        self.assertEqual(len(response_data["camiones"]), 2)
        self.assertEqual(response_data["camiones"][0]["placa"], "ABC123")
        self.assertEqual(response_data["camiones"][1]["placa"], "DEF456")
        mock_repositorio_instance.obtener_camiones.assert_called_once()

    @patch("aplicacion.lecturas.camiones.RepositorioCamion")
    @patch("aplicacion.lecturas.camiones.jsonify")
    def test_consultar_camiones_empty(self, mock_jsonify, mock_repositorio_camion):
        # Mock no camiones
        mock_repositorio_instance = MagicMock()
        mock_repositorio_instance.obtener_camiones.return_value = []
        mock_repositorio_camion.return_value = mock_repositorio_instance

        mock_jsonify.side_effect = lambda x: x  # Mock jsonify to return the input directly

        response = self.client.get('/camiones')
        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 0)
        self.assertEqual(len(response_data["camiones"]), 0)
    
    @patch("aplicacion.lecturas.camiones.RepositorioCamion")
    @patch("aplicacion.lecturas.camiones.jsonify")
    def test_consultar_camiones_exception(self, mock_jsonify, mock_repositorio_camion):
        # Mock exception
        mock_repositorio_instance = MagicMock()
        mock_repositorio_instance.obtener_camiones.side_effect = Exception("Database error")
        mock_repositorio_camion.return_value = mock_repositorio_instance

        mock_jsonify.side_effect = lambda x: x  # Mock jsonify to return the input directly
        response = self.client.get('/camiones')
        # Assertions
        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertEqual(response_data["error"], "Error interno del servidor")

    @patch("aplicacion.lecturas.camiones.RepositorioCamion")
    @patch("aplicacion.lecturas.camiones.jsonify")
    def test_consultar_camiones_invalid_date(self, mock_jsonify, mock_repositorio_camion):
        # Mock jsonify to return the input directly
        mock_jsonify.side_effect = lambda x: x

        # Call the function with an invalid date
        response = self.client.get('/camiones?fecha=23-13-01')

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertEqual(response_data["error"], "Formato de fecha inválido. Use el formato YYYY-MM-DD.")

    @patch("aplicacion.lecturas.camiones.RepositorioCamion")
    @patch("aplicacion.lecturas.camiones.jsonify")
    def test_consultar_camiones_valid_date(self, mock_jsonify, mock_repositorio_camion):
        # Mock data
        mock_camiones = [
            {
                "id": 1,
                "placa": "ABC123",
                "marca": "Marca1",
                "modelo": "Modelo1",
                "capacidad_carga_toneladas": 10,
                "volumen_carga_metros_cubicos": 20
            }
        ]
        mock_repositorio_instance = MagicMock()
        mock_repositorio_instance.obtener_camiones.return_value = mock_camiones
        mock_repositorio_camion.return_value = mock_repositorio_instance

        mock_jsonify.side_effect = lambda x: x  # Mock jsonify to return the input directly

        # Call the function with a valid date
        response = self.client.get('/camiones?fecha=2023-10-01')

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 1)
        self.assertEqual(len(response_data["camiones"]), 1)
        self.assertEqual(response_data["camiones"][0]["placa"], "ABC123")
        mock_repositorio_instance.obtener_camiones.assert_called_once()