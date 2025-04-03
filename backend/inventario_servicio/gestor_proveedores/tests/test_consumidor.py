import unittest
from unittest.mock import MagicMock, patch
from infraestructura.consumidor import ConsumidorProveedores
from infraestructura.repositorio import RepositorioProveedores
from infraestructura.despachador import DespachadorProveedores
from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
from dominio.modelo import Proveedor
import json

class TestConsumidorProveedores(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_conexion = MagicMock(spec=ConexionPulsar)
        self.mock_conexion.cliente = MagicMock()  # Add the 'cliente' attribute
        self.mock_repositorio = MagicMock(spec=RepositorioProveedores)
        self.mock_despachador = MagicMock(spec=DespachadorProveedores)

        # Patch the dependencies with correct import paths
        self.patcher_conexion = patch(
            'infraestructura.consumidor.ConexionPulsar',
            return_value=self.mock_conexion
        )
        self.patcher_repositorio = patch(
            'infraestructura.consumidor.RepositorioProveedores',
            return_value=self.mock_repositorio
        )
        self.patcher_despachador = patch(
            'infraestructura.consumidor.DespachadorProveedores',
            return_value=self.mock_despachador
        )

        self.patcher_conexion.start()
        self.patcher_repositorio.start()
        self.patcher_despachador.start()

        # Initialize the ConsumidorProveedores instance
        self.consumidor = ConsumidorProveedores(
            topico_comandos="comandos",
            topico_eventos="eventos",
            db_session=MagicMock()
        )

    def tearDown(self):
        self.patcher_conexion.stop()
        self.patcher_repositorio.stop()
        self.patcher_despachador.stop()

    def test_procesar_comando_registrar_proveedor(self):
        # Mock input data
        mensaje = json.dumps({
            "comando": "RegistrarProveedor",
            "data": {
                "nombre": "Proveedor Test",
                "email": "test@example.com",
                "numero_contacto": "123456789",
                "pais": "Colombia",
                "caracteristicas": "Caracteristicas Test",
                "condiciones_comerciales_tributarias": "Condiciones Test",
                "correlation_id": "test-correlation-id"
            }
        })

        # Mock the repository to simulate saving the Proveedor
        def guardar_side_effect(proveedor):
            # Simulate setting the fecha_registro attribute
            proveedor.fecha_registro = MagicMock()
            proveedor.fecha_registro.isoformat.return_value = "2025-03-30T12:00:00Z"
            return proveedor

        self.mock_repositorio.guardar.side_effect = guardar_side_effect

        # Call the method
        self.consumidor.procesar_comando(mensaje)

        # Verify repository save method was called
        self.mock_repositorio.guardar.assert_called_once()
        proveedor_saved = self.mock_repositorio.guardar.call_args[0][0]
        self.assertEqual(proveedor_saved.nombre, "Proveedor Test")
        self.assertEqual(proveedor_saved.email, "test@example.com")

        # Verify event dispatcher was called
        self.mock_despachador.publicar_evento.assert_called_once()
        evento_publicado = self.mock_despachador.publicar_evento.call_args[0][0]
        self.assertEqual(evento_publicado["evento"], "ProveedorRegistrado")
        self.assertEqual(evento_publicado["data"]["nombre"], "Proveedor Test")
        self.assertEqual(evento_publicado["data"]["correlation_id"], "test-correlation-id")

    def test_esperar_evento(self):
        # Mock event data
        evento = {
            "evento": "ProveedorRegistrado",
            "data": {
                "id": 1,
                "nombre": "Proveedor Test",
                "correlation_id": "test-correlation-id"
            }
        }
        mensaje_mock = MagicMock()
        mensaje_mock.data.return_value = json.dumps(evento).encode('utf-8')

        # Mock Pulsar consumer behavior
        consumidor_mock = MagicMock()
        consumidor_mock.receive.side_effect = [mensaje_mock]
        self.mock_conexion.cliente.subscribe.return_value = consumidor_mock

        # Call the method
        resultado = self.consumidor.esperar_evento(
            tipo_evento="ProveedorRegistrado",
            correlation_id="test-correlation-id",
            timeout=5
        )

        # Verify the result
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["evento"], "ProveedorRegistrado")
        self.assertEqual(resultado["data"]["nombre"], "Proveedor Test")

        # Verify Pulsar consumer interactions
        consumidor_mock.acknowledge.assert_called_once_with(mensaje_mock)

if __name__ == '__main__':
    unittest.main()