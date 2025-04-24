import jwt
import pytest
from datetime import datetime, timezone, timedelta
from dominio.access_token_manager import AccessTokenValidator

SECRET = "clave_secreta_para_firmar_token"

def generar_token(payload):
    return jwt.encode(payload, SECRET, algorithm="HS256")


@pytest.fixture
def validator():
    return AccessTokenValidator(secret_key=SECRET, allowed_roles=["director-compras"])


def test_token_valido_y_rol_correcto(validator):
    token = generar_token({"role": "director-compras"})
    valido, mensaje = validator.validate(token)
    assert valido
    assert mensaje == "Token valido"


def test_token_valido_con_rol_incorrecto(validator):
    token = generar_token({"role": "bodeguero"})
    valido, mensaje = validator.validate(token)
    assert not valido
    assert mensaje == "Permisos insuficientes"


def test_token_expirado(validator):
    token = jwt.encode(
        {
            "role": "director-compras", 
            "exp": datetime.now(tz=timezone.utc) - timedelta(seconds=1)
        },
        SECRET, algorithm="HS256"
    )
    valido, mensaje = validator.validate(token)
    assert not valido
    assert mensaje == "Token expirado"


def test_token_invalido(validator):
    token = "esto-no-es-un-token"
    valido, mensaje = validator.validate(token)
    assert not valido
    assert mensaje == "Token invalido"


