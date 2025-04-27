import unittest
from flask import Flask
from unittest.mock import patch, MagicMock
from aplicacion.lecturas.ruta_visitas import ruta_visitas_bp

class TestRutaVisita(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ruta_visitas_bp)
        self.app.testing = True
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.ruta_visitas.validar_token")
    @patch("aplicacion.lecturas.ruta_visitas.RutasVisitas")
    @patch("aplicacion.lecturas.ruta_visitas.RutaVisitasInputSchema")
    def test_consultar_ruta_visita_success(self, mock_schema, mock_repo, mock_validar_token):
        mock_validar_token.return_value = True
        mock_repo.return_value.obtener_rutas_por_vendedor_y_fecha.return_value = [
            {
                "cliente_id": 1,
                "nombre_cliente": "Cliente A",
                "barrio": "Barrio A",
                "fecha": "2023-10-01",
                "tiempo_estimado": "30 minutos"
            }
        ]
        mock_schema.return_value.dump.return_value = [
            {
                "cliente_id": 1,
                "nombre_cliente": "Cliente A",
                "barrio": "Barrio A",
                "fecha": "2023-10-01",
                "tiempo_estimado": "30 minutos"
            }
        ]

        headers = {"Authorization": "Bearer valid_token"}
        response = self.client.get(
            "/ruta_visita?vendedor_id=1&fecha=2023-10-01", headers=headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "ruta_visita": [
                {
                    "cliente_id": 1,
                    "nombre_cliente": "Cliente A",
                    "barrio": "Barrio A",
                    "fecha_completa": "2023-10-01",
                    "trayecto": "30 minutos",
                }
            ]
        })

    def test_consultar_ruta_visita_no_token(self):
        response = self.client.get("/ruta_visita?vendedor_id=1&fecha=2023-10-01")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "No se proporcionó un token"})

    @patch("aplicacion.lecturas.ruta_visitas.validar_token")
    def test_consultar_ruta_visita_invalid_token(self, mock_validar_token):
        mock_validar_token.return_value = False
        headers = {"Authorization": "Bearer invalid_token"}
        response = self.client.get(
            "/ruta_visita?vendedor_id=1&fecha=2023-10-01", headers=headers
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"message": "forbidden"})

    @patch("aplicacion.lecturas.ruta_visitas.validar_token")
    def test_consultar_ruta_visita_missing_params(self, mock_validar_token):
        mock_validar_token.return_value = True
        headers = {"Authorization": "Bearer valid_token"}
        response = self.client.get("/ruta_visita", headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "error": "Parámetros inválidos",
            "detalles": "Se requieren vendedor_id y fecha en el formato YYYY-MM-DD",
        })

    @patch("aplicacion.lecturas.ruta_visitas.validar_token")
    def test_consultar_ruta_visita_invalid_date_format(self, mock_validar_token):
        mock_validar_token.return_value = True
        headers = {"Authorization": "Bearer valid_token"}
        response = self.client.get(
            "/ruta_visita?vendedor_id=1&fecha=01-10-2023", headers=headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "error": "Formato de fecha inválido",
            "detalles": "La fecha debe estar en el formato YYYY-MM-DD",
        })

    @patch("aplicacion.lecturas.ruta_visitas.validar_token")
    @patch("aplicacion.lecturas.ruta_visitas.RutasVisitas")
    def test_consultar_ruta_visita_not_found(self, mock_repo, mock_validar_token):
        mock_validar_token.return_value = True
        mock_repo.return_value.obtener_rutas_por_vendedor_y_fecha.return_value = []
        headers = {"Authorization": "Bearer valid_token"}
        response = self.client.get(
            "/ruta_visita?vendedor_id=1&fecha=2023-10-01", headers=headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"ruta_visita": []})


if __name__ == "__main__":
    unittest.main()