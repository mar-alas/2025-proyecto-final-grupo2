import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.rutas_visitas_optimizada import ruta_visita_optimizada_bp

class TestConsultarRutaVisitaOptimizada(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ruta_visita_optimizada_bp)
        self.app.testing = True
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.rutas_visitas_optimizada.validar_token")
    @patch("aplicacion.lecturas.rutas_visitas_optimizada.RutasVisitas")
    @patch("aplicacion.lecturas.rutas_visitas_optimizada.RutaVisitasInputSchema")
    def test_consultar_ruta_visita_optimizada_success(self, mock_schema, mock_repo, mock_validar_token):
        # Arrange
        mock_validar_token.return_value = True
        mock_repo.return_value.obtener_rutas_por_vendedor_y_fecha.return_value = [
            MagicMock(cliente_id=1, nombre_cliente="Cliente A", barrio="Centro", fecha="2023-10-01", tiempo_estimado="10 min", distancia="5 km"),
            MagicMock(cliente_id=2, nombre_cliente="Cliente B", barrio="Norte", fecha="2023-10-01", tiempo_estimado="15 min", distancia="2 km")
        ]
        mock_schema.return_value.dump.return_value = [
            {"cliente_id": 1, "nombre_cliente": "Cliente A", "barrio": "Centro", "fecha": "2023-10-01", "tiempo_estimado": "10 min", "distancia": "5 km"},
            {"cliente_id": 2, "nombre_cliente": "Cliente B", "barrio": "Norte", "fecha": "2023-10-01", "tiempo_estimado": "15 min", "distancia": "2 km"}
        ]

        headers = {"Authorization": "Bearer valid_token"}
        query_string = {"vendedor_id": 1, "fecha": "2023-10-01"}

        # Act
        response = self.client.get("/ruta_visita_optimizada", headers=headers, query_string=query_string)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("ruta_visita", response.json)
        self.assertEqual(len(response.json["ruta_visita"]), 2)

    @patch("aplicacion.lecturas.rutas_visitas_optimizada.validar_token")
    def test_consultar_ruta_visita_optimizada_invalid_token(self, mock_validar_token):
        # Arrange
        mock_validar_token.return_value = False
        headers = {"Authorization": "Bearer invalid_token"}
        query_string = {"vendedor_id": 1, "fecha": "2023-10-01"}

        # Act
        response = self.client.get("/ruta_visita_optimizada", headers=headers, query_string=query_string)

        # Assert
        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json)
        self.assertEqual(response.json["message"], "forbidden")

    @patch("aplicacion.lecturas.rutas_visitas_optimizada.validar_token")
    def test_consultar_ruta_visita_optimizada_missing_parameters(self, mock_validar_token):
        # Arrange
        mock_validar_token.return_value = True
        headers = {"Authorization": "Bearer valid_token"}
        # Act
        response = self.client.get("/ruta_visita_optimizada", headers=headers)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertEqual(response.json["error"], "Parámetros inválidos")

    @patch("aplicacion.lecturas.rutas_visitas_optimizada.validar_token")
    def test_consultar_ruta_visita_optimizada_invalid_date_format(self, mock_validar_token):
        mock_validar_token.return_value = True
        headers = {"Authorization": "Bearer valid_token"}
        query_string = {"vendedor_id": 1, "fecha": "01-10-2023"}
        response = self.client.get("/ruta_visita_optimizada", query_string=query_string,  headers=headers)

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "error": "Formato de fecha inválido",
            "detalles": "La fecha debe estar en el formato YYYY-MM-DD",
        })

    @patch("aplicacion.lecturas.rutas_visitas_optimizada.validar_token")
    @patch("aplicacion.lecturas.rutas_visitas_optimizada.RutasVisitas")
    def test_consultar_ruta_visita_optimizada_no_ruta_found(self, mock_repo, mock_validar_token):
        # Arrange
        mock_validar_token.return_value = True
        mock_repo.return_value.obtener_rutas_por_vendedor_y_fecha.return_value = None

        headers = {"Authorization": "Bearer valid_token"}
        query_string = {"vendedor_id": 1, "fecha": "2023-10-01"}

        # Act
        response = self.client.get("/ruta_visita_optimizada", headers=headers, query_string=query_string)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"ruta_visita": []})
