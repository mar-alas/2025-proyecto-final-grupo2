import unittest
from unittest.mock import MagicMock, patch
from infraestructura.logistica_entregas import LogisticaEntregas

class TestLogisticaEntregas(unittest.TestCase):
    def setUp(self):
        self.logistica_entregas = LogisticaEntregas()
        self.logistica_entregas.repositorio_detalle_entrega = MagicMock()
        self.logistica_entregas.repositorio_camion = MagicMock()
        self.logistica_entregas.repositorio_entregas_programadas = MagicMock()
        self.logistica_entregas.repositorio_entrega_programadas_detalles = MagicMock()
        self.logistica_entregas.repositorio_entrega = MagicMock()

    @patch("random.choice")
    def test_asignar_camion_a_entrega_success(self, mock_random_choice):
        # Mock data
        mock_camion = {"id": 1, "placa": "TEST123"}
        mock_random_choice.return_value = mock_camion
        self.logistica_entregas.repositorio_camion.obtener_camiones.return_value = [mock_camion]
        self.logistica_entregas.repositorio_detalle_entrega.registrar_detalle_entrega.return_value = 100

        # Call the method
        detalle_id, camion_id = self.logistica_entregas.asignar_camion_a_entrega(1)

        # Assertions
        self.assertEqual(detalle_id, 100)
        self.assertEqual(camion_id, 1)
        self.logistica_entregas.repositorio_camion.obtener_camiones.assert_called_once()
        self.logistica_entregas.repositorio_detalle_entrega.registrar_detalle_entrega.assert_called_once_with({
            "entrega_id": 1,
            "camion_id": 1
        })

    def test_asignar_camion_a_entrega_no_camiones(self):
        # Mock no available camiones
        self.logistica_entregas.repositorio_camion.obtener_camiones.return_value = []

        # Call the method and assert exception
        with self.assertRaises(Exception) as context:
            self.logistica_entregas.asignar_camion_a_entrega(1)
        self.assertEqual(str(context.exception), "No hay camiones disponibles para asignar.")

    def test_convert_str_to_list_success(self):
        # Call the method
        result = self.logistica_entregas.convert_str_to_list("10.0,20.0")

        # Assertions
        self.assertEqual(result, [10.0, 20.0])

    @patch("requests.post")
    def test_asignar_entregas_programadas_no_entregas(self, mock_post):
        # Mock no scheduled deliveries
        self.logistica_entregas.repositorio_detalle_entrega.obtener_entregas_programadas.return_value = []

        # Call the method and assert exception
        with self.assertRaises(Exception) as context:
            self.logistica_entregas.asignar_entregas_programadas("2023-10-01", 1, "Test Address")
        self.assertEqual(str(context.exception), "No hay entregas programadas para la fecha dada.")
        # Mock data
        mock_entrega_programada = MagicMock()
        mock_entrega_programada.id = 1  # Mock the 'id' attribute
        mock_entregas_programadas = [mock_entrega_programada]  # Mock as a list of objects

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ruta": "mocked_route"}
        mock_post.return_value = mock_response

        self.logistica_entregas.repositorio_entregas_programadas.obtener_entregas_programadas_por_fecha_camion.return_value = mock_entregas_programadas
        self.logistica_entregas.repositorio_entrega.obtener_entrega_por_id.return_value = {
            "direccion_entrega": "Existing Address",
            "coordenadas_destino": "15.0,25.0"
        }
        self.logistica_entregas.repositorio_entrega_programadas_detalles.agregar_detalle.return_value = 2

        # Call the method
        entrega_programada_id, entrega_programada_detalle_id = self.logistica_entregas.actualizar_entregas_programadas(
            entrega_id=1,
            fecha="2023-10-01",
            camion_id=1,
            destino_coordenadas="10.0,20.0",
            destino_direccion="Test Address",
            origen="5.0,15.0"
        )

        # Assertions
        self.assertEqual(entrega_programada_id, 1)  # Ensure the correct ID is returned
        self.assertEqual(entrega_programada_detalle_id, 2)  # Ensure the detail ID is correct

    @patch("requests.post")
    def test_actualizar_entregas_programadas_error(self, mock_post):
        # Mock response with error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Call the method and assert exception
        with self.assertRaises(Exception) as context:
            self.logistica_entregas.actualizar_entregas_programadas(
                entrega_id=1,
                fecha="2023-10-01",
                camion_id=1,
                destino_coordenadas="10.0,20.0",
                destino_direccion="Test Address",
                origen="5.0,15.0"
            )
        self.assertEqual(str(context.exception), "Error al calcular la ruta.")