import unittest
from unittest.mock import patch, MagicMock
from aplicacion.lecturas.obtener_ruta import consulta_camiones_bp
from flask import Flask

class TestConsultarCamiones(unittest.TestCase):
    def setUp(self):
        # Create a Flask app and register the blueprint
        self.app = Flask(__name__)
        self.app.register_blueprint(consulta_camiones_bp, url_prefix='/')
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.obtener_ruta.RepositorioEntregasProgramadas")
    @patch("aplicacion.lecturas.obtener_ruta.RepositorioCamion")
    def test_consultar_camiones_with_entregas(self, mock_repositorio_camion, mock_repositorio_entregas_programadas):
        # Mock data for camiones
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
        mock_repositorio_camion_instance = MagicMock()
        mock_repositorio_camion_instance.obtener_camiones.return_value = mock_camiones
        mock_repositorio_camion.return_value = mock_repositorio_camion_instance

        # Mock data for entregas_programadas
        mock_entregas_programadas = [
            MagicMock(estado="En ruta")
        ]
        mock_repositorio_entregas_programadas_instance = MagicMock()
        mock_repositorio_entregas_programadas_instance.obtener_entregas_programadas_por_fecha_camion.side_effect = lambda fecha, camion_id: mock_entregas_programadas if camion_id == 1 else []
        mock_repositorio_entregas_programadas.return_value = mock_repositorio_entregas_programadas_instance

        # Call the function
        response = self.client.get('/ruta_camiones?fecha=2023-10-01')
        print(response)

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 2)
        self.assertEqual(len(response_data["camiones"]), 2)
        self.assertEqual(response_data["camiones"][0]["estado_enrutamiento"], "En ruta")
        self.assertEqual(response_data["camiones"][1]["estado_enrutamiento"], "Sin entregas programadas")

    @patch("aplicacion.lecturas.obtener_ruta.RepositorioEntregasProgramadas")
    @patch("aplicacion.lecturas.obtener_ruta.RepositorioCamion")
    def test_consultar_camiones_no_entregas(self, mock_repositorio_camion, mock_repositorio_entregas_programadas):
        # Mock data for camiones
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
        mock_repositorio_camion_instance = MagicMock()
        mock_repositorio_camion_instance.obtener_camiones.return_value = mock_camiones
        mock_repositorio_camion.return_value = mock_repositorio_camion_instance

        # Mock no entregas_programadas
        mock_repositorio_entregas_programadas_instance = MagicMock()
        mock_repositorio_entregas_programadas_instance.obtener_entregas_programadas_por_fecha_camion.return_value = []
        mock_repositorio_entregas_programadas.return_value = mock_repositorio_entregas_programadas_instance

        # Call the function
        response = self.client.get('/ruta_camiones?fecha=2023-10-01')

        # Assertions
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["total"], 1)
        self.assertEqual(len(response_data["camiones"]), 1)
        self.assertEqual(response_data["camiones"][0]["estado_enrutamiento"], "Sin entregas programadas")

    @patch("aplicacion.lecturas.obtener_ruta.RepositorioCamion")
    def test_consultar_camiones_invalid_date(self, mock_repositorio_camion):
        # Call the function with an invalid date
        response = self.client.get('/ruta_camiones?fecha=23-13-01')

        # Assertions
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertEqual(response_data["error"], "Formato de fecha inválido. Use el formato YYYY-MM-DD.")

    @patch("aplicacion.lecturas.obtener_ruta.RepositorioCamion")
    def test_consultar_camiones_exception(self, mock_repositorio_camion):
        # Mock exception
        mock_repositorio_camion_instance = MagicMock()
        mock_repositorio_camion_instance.obtener_camiones.side_effect = Exception("Database error")
        mock_repositorio_camion.return_value = mock_repositorio_camion_instance

        # Call the function
        response = self.client.get('/ruta_camiones')

        # Assertions
        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertEqual(response_data["error"], "Error interno del servidor")