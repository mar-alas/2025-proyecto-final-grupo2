import pytest
import jwt
import time
from gestor_usuarios.dominio.access_token_manager import generar_token, validar_token, SECRET_KEY

def test_generar_token_y_validar_token_valido():
    payload = {"user_id": "123", "role": "admin"}
    token = generar_token(payload, expiracion_minutos=1)  # duración corta para test

    assert isinstance(token, str)
    assert validar_token(token) is True

def test_token_expirado():
    payload = {"user_id": "123", "role": "admin"}
    token = generar_token(payload, expiracion_minutos=0)  # expiración inmediata
    time.sleep(1)  # esperar a que expire

    assert validar_token(token) is False

def test_token_invalido():
    token_invalido = "esto.no.es.un.token.valido"

    assert validar_token(token_invalido) is False

def test_token_firmado_con_otra_clave():
    payload = {"user_id": "123", "role": "admin"}
    token = jwt.encode(payload, "otra_clave", algorithm="HS256")

    assert validar_token(token) is False


def test_validar_token_lanza_excepcion_generica():
    token_malformado = None 
    resultado = validar_token(token_malformado)
    assert resultado is False