import unittest
import jwt
from datetime import datetime, timedelta, timezone
from seedwork_compartido.dominio.seguridad.access_token_manager import generar_token, validar_token, SECRET_KEY


class TestJWTTokenUtils(unittest.TestCase):

    def setUp(self):
        self.payload = {'usuario_id': 123}

    def test_generar_token_devuelve_token_valido(self):
        token = generar_token(self.payload)
        self.assertIsInstance(token, str)

        # Decodifica sin verificar la firma para ver el contenido
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_payload['usuario_id'], 123)
        self.assertIn('exp', decoded_payload)

    def test_validar_token_valido_retorna_true(self):
        token = generar_token(self.payload)
        self.assertTrue(validar_token(token))

    def test_validar_token_expirado_retorna_false(self):
        from freezegun import freeze_time

        with freeze_time("2025-01-01 12:00:00") as frozen_time:
            token = generar_token({"user_id": 123}, expiracion_minutos=1)

            # Avanzar el tiempo después de generar el token
            frozen_time.move_to("2025-01-01 12:02:00")

            self.assertFalse(validar_token(token))

    def test_validar_token_invalido_retorna_false(self):
        token = "token_invalido_que_no_es_jwt"
        self.assertFalse(validar_token(token))

    def test_validar_token_firma_invalida_retorna_false(self):
        token = jwt.encode(self.payload, "otra_clave", algorithm="HS256")
        self.assertFalse(validar_token(token))

if __name__ == '__main__':
    unittest.main()
