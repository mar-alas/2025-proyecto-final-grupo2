import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.entrega_detallada import consultar_entrega_detallada

class TestConsultarEntregaDetallada(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app and context
        self.app = Flask(__name__)
        self.app.add_url_rule('/detalle', view_func=consultar_entrega_detallada, methods=['GET'])
        self.client = self.app.test_client()

    @patch("aplicacion.lecturas.entrega_detallada.RepositorioEntrega")
    @patch("aplicacion.lecturas.entrega_detallada.RepositorioEntregasProgramadas")
    @patch("aplicacion.lecturas.entrega_detallada.RepositorioDetalleEntrega")
    @patch("aplicacion.lecturas.entrega_detallada.RepositorioCamion")
    @patch("aplicacion.lecturas.entrega_detallada.haversine")
    def test_consultar_entrega_detallada_success(
        self, mock_haversine, mock_repositorio_camion, mock_repositorio_detalle_entrega,
        mock_repositorio_entregas_programadas, mock_repositorio_entrega
    ):
        # Mock data
        entrega_id = 1
        mock_entrega = {
            "coordenadas_destino": "10.0,20.0",
            "coordenadas_origen": "5.0,15.0",
            "cliente_id": 123,
            "pedido_id": 456,
            "fecha_entrega": "2023-10-01"
        }
        mock_entrega_detalle = [{"camion_id": 1}]
        mock_camion = {"id": 1, "placa": "TEST123"}
        mock_entregas_programadas = [{"id": 1}, {"id": 2}]
        mock_haversine.return_value = 120.0  # 120 km

        # Mock repository methods
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.return_value = mock_entrega
        mock_repositorio_detalle_entrega.return_value.obtener_detalles_por_entrega.return_value = mock_entrega_detalle
        mock_repositorio_camion.return_value.obtener_camion_por_id.return_value = mock_camion
        mock_repositorio_entregas_programadas.return_value.obtener_entregas_programadas_por_fecha_camion.return_value = mock_entregas_programadas

        # Make the request
        with self.app.test_request_context('/detalle?entrega_id=1'):
            response = self.client.get('/detalle?entrega_id=1')

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "placas_vehiculo": "TEST123",
            "pedidos_anteriores": 2,
            "distancia_restante": "120.0 km",
            "tiempo_estimado": "2.0 horas",
            "cliente_id": 123,
            "pedido_id": 456
        })

    def test_consultar_entrega_detallada_missing_entrega_id(self):
        # Make the request without entrega_id
        with self.app.test_request_context('/detalle'):
            response = self.client.get('/detalle')

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            "error": "Entrega ID es requerido",
            "message": "Debe proporcionar un entrega_id válido en la consulta"
        })

    @patch("aplicacion.lecturas.entrega_detallada.RepositorioEntrega")
    @patch("aplicacion.lecturas.entrega_detallada.RepositorioDetalleEntrega")
    def test_consultar_entrega_detallada_not_found(
        self, mock_repositorio_detalle_entrega, mock_repositorio_entrega
    ):
        # Mock no entrega found
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.return_value = None
        mock_repositorio_detalle_entrega.return_value.obtener_detalles_por_entrega.return_value = None

        # Make the request
        with self.app.test_request_context('/detalle?entrega_id=1'):
            response = self.client.get('/detalle?entrega_id=1')

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            "error": "Entrega no encontrada",
            "message": "No se encontró la entrega con ID 1"
        })

    @patch("aplicacion.lecturas.entrega_detallada.RepositorioEntrega")
    def test_consultar_entrega_detallada_internal_error(self, mock_repositorio_entrega):
        # Mock an exception
        mock_repositorio_entrega.return_value.obtener_entrega_por_id.side_effect = Exception("Database error")

        # Make the request
        with self.app.test_request_context('/detalle?entrega_id=1'):
            response = self.client.get('/detalle?entrega_id=1')

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "error": "Error interno del servidor",
            "message": "Database error"
        })

if __name__ == "__main__":
    unittest.main()