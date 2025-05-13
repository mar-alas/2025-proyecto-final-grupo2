import json
from unittest import TestCase
import unittest
from urllib import request
from infraestructura.consumidor import ConsumidorLogistica
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import requests
from pulsar import ConsumerType
import pulsar


class TestConsumidorLogistica(TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_conexion = MagicMock()
        self.mock_repositorio = MagicMock()
        self.mock_logistica_entregas = MagicMock()
        self.mock_logger = MagicMock()

        # Patch dependencies
        self.patcher_conexion = patch(
            'infraestructura.consumidor.ConexionPulsar',
            return_value=self.mock_conexion
        )
        self.patcher_repositorio = patch(
            'infraestructura.consumidor.RepositorioEntrega',
            return_value=self.mock_repositorio
        )
        self.patcher_logistica_entregas = patch(
            'infraestructura.consumidor.LogisticaEntregas',
            return_value=self.mock_logistica_entregas
        )
        self.patcher_logger = patch(
            'infraestructura.consumidor.logging.getLogger',
            return_value=self.mock_logger
        )

        self.patcher_conexion.start()
        self.patcher_repositorio.start()
        self.patcher_logistica_entregas.start()
        self.patcher_logger.start()

        # Initialize the ConsumidorLogistica instance
        self.consumidor = ConsumidorLogistica(topico_pedido="test-topico")

    def tearDown(self):
        self.patcher_conexion.stop()
        self.patcher_repositorio.stop()
        self.patcher_logistica_entregas.stop()
        self.patcher_logger.stop()

    def test_procesar_registro_pedido(self):
        # Mock input data
        mensaje = json.dumps({
            "pedido_id": 1,
            "cliente_id": 123,
            "fecha_creacion": "2023-10-01 12:00:00.000000",
            "estado": "Pendiente",
            "productos": {
                "1": {"cantidad": 2},
                "2": {"cantidad": 3}
            },
            "total": 5000,
            "token": "test-token"
        })

        # Mock methods
        self.consumidor.get_client_data = MagicMock(return_value={
            "address": "Test Address",
            "geographic_coordinates": "4.7110,-74.0721"
        })
        self.consumidor.get_delivery_date = MagicMock(return_value=(
            datetime(2023, 10, 5), 5
        ))
        self.mock_repositorio.registrar_entrega.return_value = 10
        self.mock_logistica_entregas.asignar_camion_a_entrega.return_value = (20, 30)

        # Call the method
        self.consumidor.procesar_registro_pedido(mensaje)

        # Verify interactions
        self.consumidor.get_client_data.assert_called_once_with(123, "test-token")
        self.consumidor.get_delivery_date.assert_called_once_with(
            {"1": {"cantidad": 2}, "2": {"cantidad": 3}},
            "2023-10-01 12:00:00.000000",
            "test-token"
        )
        self.mock_repositorio.registrar_entrega.assert_called_once()
        self.mock_logistica_entregas.asignar_camion_a_entrega.assert_called_once_with(10)
        self.mock_logistica_entregas.actualizar_entregas_programadas.assert_called_once()

    def test_escuchar(self):
        # Mock Pulsar consumer behavior
        mensaje_mock = MagicMock()
        mensaje_mock.data.return_value = json.dumps({
            "pedido_id": 1,
            "cliente_id": 123,
            "fecha_creacion": "2023-10-01 12:00:00.000000",
            "estado": "Pendiente",
            "productos": {
                "1": {"cantidad": 2},
                "2": {"cantidad": 3}
            },
            "total": 5000,
            "token": "test-token"
        }).encode('utf-8')

        consumidor_mock = MagicMock()
        consumidor_mock.receive.side_effect = [mensaje_mock, Exception("StopIteration")]
        self.mock_conexion.cliente.subscribe.return_value = consumidor_mock

        # Mock procesar_registro_pedido
        self.consumidor.procesar_registro_pedido = MagicMock()

        # Call the method
        self.consumidor.escuchar(max_iterations=1)

        # Verify interactions
        self.mock_conexion.cliente.subscribe.assert_called_once_with(
            "test-topico",
            subscription_name="logistica_pedido_sub",
            consumer_type=ConsumerType.Shared
        )
        self.consumidor.procesar_registro_pedido.assert_called_once()
        consumidor_mock.acknowledge.assert_called_once_with(mensaje_mock)

    def test_escuchar_no_messages(self):
        # Mock Pulsar consumer behavior with no messages
        consumidor_mock = MagicMock()
        consumidor_mock.receive.side_effect = [pulsar.Timeout(), Exception("StopIteration")]
        self.mock_conexion.cliente.subscribe.return_value = consumidor_mock

        # Mock procesar_registro_pedido
        self.consumidor.procesar_registro_pedido = MagicMock()

        # Call the method
        self.consumidor.escuchar(max_iterations=1)

        # Verify interactions
        self.mock_conexion.cliente.subscribe.assert_called_once_with(
            "test-topico",
            subscription_name="logistica_pedido_sub",
            consumer_type=ConsumerType.Shared
        )
        self.consumidor.procesar_registro_pedido.assert_not_called()

    def test_escuchar_exception_handling(self):
        # Mock Pulsar consumer behavior
        consumidor_mock = MagicMock()
        consumidor_mock.receive.side_effect = [Exception("Test exception"), Exception("StopIteration")]
        self.mock_conexion.cliente.subscribe.return_value = consumidor_mock

        # Call the method
        self.consumidor.escuchar(max_iterations=1)

        # Verify that the exception was logged
        self.mock_logger.error.assert_called_with("Error en el proceso de escucha: Exception: Test exception")
        
    @patch('infraestructura.consumidor.requests.get')
    def test_get_client_data_success(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "clientes": [
                {
                    "id": 123,
                    "address": "Test Address",
                    "geographic_coordinates": "4.7110,-74.0721"
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        result = self.consumidor.get_client_data(123, "test-token")

        # Verify the result
        self.assertEqual(result, {
            "address": "Test Address",
            "geographic_coordinates": "4.7110,-74.0721"
        })

        # Verify the request
        mock_get.assert_called_once_with(
            'http://localhost:3011/api/v1/seguridad/gestor_usuarios/r/clientes',
            verify=False,
            headers={"Authorization": "Bearer test-token"}
        )

    @patch('infraestructura.consumidor.requests.get')
    def test_get_client_data_client_not_found(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "clientes": [
                {
                    "id": 456,
                    "address": "Other Address",
                    "geographic_coordinates": "5.0000,-75.0000"
                }
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Call the method
        result = self.consumidor.get_client_data(123, "test-token")

        # Verify the result
        self.assertIsNone(result)

        # Verify the request
        mock_get.assert_called_once_with(
            'http://localhost:3011/api/v1/seguridad/gestor_usuarios/r/clientes',
            verify=False,
            headers={"Authorization": "Bearer test-token"}
        )
        self.mock_logger.error.assert_called_once_with(
            "Error al consultar los clientes: cliente_id no existe"
        )

    @patch('infraestructura.consumidor.requests.get')
    def test_get_client_data_request_failure(self, mock_get):
        # Mock response to raise an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.return_value = mock_response

        # Call the method and verify it raises an exception
        with self.assertRaises(requests.exceptions.HTTPError):
            self.consumidor.get_client_data(123, "test-token")

        # Verify the request
        mock_get.assert_called_once_with(
            'http://localhost:3011/api/v1/seguridad/gestor_usuarios/r/clientes',
            verify=False,
            headers={"Authorization": "Bearer test-token"}
        )

    @patch('infraestructura.consumidor.requests.get')
    def test_get_delivery_date_success(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "products": [
                {"id": 1, "tiempo_entrega": "3 días"},
                {"id": 2, "tiempo_entrega": "5 días"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock input data
        entrega_productos = {
            "1": {"cantidad": 2},
            "2": {"cantidad": 3}
        }
        fecha_pedido = "2023-10-01 12:00:00.000000"
        token = "test-token"

        # Call the method
        result = self.consumidor.get_delivery_date(entrega_productos, fecha_pedido, token)

        # Verify the result
        expected_date = datetime(2023, 10, 6, 12, 0, 0)  # 5 days from the fecha_pedido at midnight
        self.assertEqual(result, (expected_date, 5))

        # Verify the request
        mock_get.assert_called_once_with(
            'http://localhost:3001/api/v2/inventario/gestor_productos/productos',
            verify=False,
            headers={"Authorization": "Bearer test-token"}
        )

    @patch('infraestructura.consumidor.requests.get')
    def test_get_delivery_date_missing_product_data(self, mock_get):
        # Mock response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "products": [
                {"id": 1, "tiempo_entrega": "3 días"}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock input data
        entrega_productos = {
            "1": {"cantidad": 2},
            "2": {"cantidad": 3}
        }
        fecha_pedido = "2023-10-01 12:00:00.000000"
        token = "test-token"

        # Call the method
        result = self.consumidor.get_delivery_date(entrega_productos, fecha_pedido, token)

        # Verify the result
        expected_date = datetime(2023, 10, 4)  # 3 days from the fecha_pedido (default for missing product)
        self.assertEqual(result[1], 5)  # Total quantity
        self.assertTrue((expected_date - result[0]).days <= 5)  # Delivery date within range

    @patch('infraestructura.consumidor.requests.get')
    def test_get_delivery_date_request_failure(self, mock_get):
        # Mock response to raise an HTTP error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.return_value = mock_response

        # Mock input data
        entrega_productos = {
            "1": {"cantidad": 2},
            "2": {"cantidad": 3}
        }
        fecha_pedido = "2023-10-01 12:00:00.000000"
        token = "test-token"

        # Call the method and verify it raises an exception
        with self.assertRaises(requests.exceptions.HTTPError):
            self.consumidor.get_delivery_date(entrega_productos, fecha_pedido, token)

        # Verify the request
        mock_get.assert_called_once_with(
            'http://localhost:3001/api/v2/inventario/gestor_productos/productos',
            verify=False,
            headers={"Authorization": "Bearer test-token"}
        )

if __name__ == '__main__':
    unittest.main()