import unittest
import jwt
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from seedwork_compartido.dominio.seguridad.access_token_manager import generar_token, validar_token, SECRET_KEY

class TestJWTTokenUtils(unittest.TestCase):

    def setUp(self):
        self.payload = {'usuario_id': 123}

    def test_generar_token_devuelve_token_valido(self):
        token = generar_token(self.payload)
        self.assertIsInstance(token, str)

        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_payload['usuario_id'], 123)
        self.assertIn('exp', decoded_payload)

    def test_validar_token_valido_retorna_true(self):
        token = generar_token(self.payload)
        self.assertTrue(validar_token(token))

    def test_validar_token_expirado_retorna_false(self):
        # Creamos un token con expiración de 1 minuto
        with patch('access_token_manager.datetime') as mock_datetime:
            # Simula que el token se genera en t0
            t0 = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
            mock_datetime.datetime.now.return_value = t0
            mock_datetime.datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            mock_datetime.timedelta = timedelta
            mock_datetime.timezone = timezone

            token = generar_token(self.payload, expiracion_minutos=1)

        # Ahora simulamos que estamos 2 minutos después
        with patch('access_token_manager.datetime') as mock_datetime:
            t1 = datetime(2025, 1, 1, 12, 2, 0, tzinfo=timezone.utc)
            mock_datetime.datetime.now.return_value = t1
            mock_datetime.datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            mock_datetime.timedelta = timedelta
            mock_datetime.timezone = timezone

            self.assertFalse(validar_token(token))

    def test_validar_token_invalido_retorna_false(self):
        token = "esto_no_es_un_token_valido"
        self.assertFalse(validar_token(token))

    def test_validar_token_con_firma_invalida_retorna_false(self):
        token = jwt.encode(self.payload, 'clave_incorrecta', algorithm='HS256')
        self.assertFalse(validar_token(token))

if __name__ == '__main__':
    unittest.main()