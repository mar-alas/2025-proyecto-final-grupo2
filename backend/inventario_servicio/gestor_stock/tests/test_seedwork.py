import unittest
from unittest.mock import patch, MagicMock
from seedwork_compartido.dominio.seguridad.access_token_manager import generar_token, validar_token
from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
from seedwork_compartido.infraestructura.config_broker import obtener_config_pulsar
import jwt
import datetime

class TestAccessTokenManager(unittest.TestCase):

    @patch('seedwork_compartido.dominio.seguridad.access_token_manager.jwt.encode')
    def test_generar_token(self, mock_encode):
        mock_encode.return_value = "mocked_token"
        payload = {"user_id": 1}
        token = generar_token(payload, expiracion_minutos=10)
        self.assertEqual(token, "mocked_token")
        mock_encode.assert_called_once()

    @patch('seedwork_compartido.dominio.seguridad.access_token_manager.jwt.decode')
    def test_validar_token_valido(self, mock_decode):
        mock_decode.return_value = {"user_id": 1}
        token = "valid_token"
        self.assertTrue(validar_token(token))
        mock_decode.assert_called_once()

    @patch('seedwork_compartido.dominio.seguridad.access_token_manager.jwt.decode')
    def test_validar_token_expirado(self, mock_decode):
        mock_decode.side_effect = jwt.ExpiredSignatureError
        token = "expired_token"
        self.assertFalse(validar_token(token))
        mock_decode.assert_called_once()

    @patch('seedwork_compartido.dominio.seguridad.access_token_manager.jwt.decode')
    def test_validar_token_invalido(self, mock_decode):
        mock_decode.side_effect = jwt.InvalidTokenError
        token = "invalid_token"
        self.assertFalse(validar_token(token))
        mock_decode.assert_called_once()

class TestConfigBroker(unittest.TestCase):

    @patch('seedwork_compartido.infraestructura.config_broker.os.getenv')
    def test_obtener_config_pulsar(self, mock_getenv):
        mock_getenv.return_value = "mocked_host"
        config = obtener_config_pulsar()
        self.assertEqual(config["pulsar_url"], "pulsar://mocked_host:6650")
        mock_getenv.assert_called_once_with('PULSAR_HOST', default="localhost")


if __name__ == '__main__':
    unittest.main()