import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from aplicacion.lecturas.generador_rutas import generar_ruta_endpoint

class TestGenerarRutaEndpoint(unittest.TestCase):

    @patch('aplicacion.lecturas.generador_rutas.Optimizador')
    def test_generar_ruta_endpoint(self, mock_optimizador):
        # Arrange
        app = Flask(__name__)
        app.register_blueprint(generar_ruta_endpoint.__globals__['generador_rutas_bp'])
        
        # Configure the mock optimizador
        mock_optimizador_instance = MagicMock()
        mock_optimizador_instance.optimizar_ruta.return_value = [
            (4.594132167917568, -74.13704414499277),
            (4.564711253902941, -74.176446888055)
        ]
        mock_optimizador.return_value = mock_optimizador_instance

        # Prepare test data
        test_data = {
            "punto_inicio": {"origen": [4.594121, -74.0817500]},
            "destinos": {
                "B": {"destino": [4.594132167917568, -74.13704414499277]},
                "C": {"destino": [4.564711253902941, -74.176446888055]}
            }
        }

        client = app.test_client()

        # Act - Use the test client without test_request_context
        # Let the test client handle the request context
        response = client.get('/generar_ruta', json=test_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_optimizador.assert_called_once_with(
            (4.594121, -74.08175),
            [(4.594132167917568, -74.13704414499277), (4.564711253902941, -74.176446888055)]
        )
        mock_optimizador_instance.optimizar_ruta.assert_called_once()

if __name__ == '__main__':
    unittest.main()