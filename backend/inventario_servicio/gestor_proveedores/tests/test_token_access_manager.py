import pytest
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token, generar_token

SECRET_KEY = 'clave_secreta_para_firmar_token'


def test_generar_token():
    payload = {'user_id': 123}
    token = generar_token(payload)
    
    assert token is not None
    assert isinstance(token, str)

    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    assert decoded_payload['user_id'] == 123
    assert 'exp' in decoded_payload


def test_validar_token_valido():
    payload = {'user_id': 123}
    token = generar_token(payload)
    
    is_valid = validar_token(token)
    assert is_valid is True


def test_validar_token_expirado():
    payload = {'user_id': 123}
    token = generar_token(payload, expiracion_minutos=-1)
    
    is_valid = validar_token(token)
    assert is_valid is False


def test_validar_token_invalido():
    token_invalido = 'token_invalido'
    
    is_valid = validar_token(token_invalido)
    assert is_valid is False


def test_validar_token_malformado():
    malformado = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    
    is_valid = validar_token(malformado)
    assert is_valid is False
