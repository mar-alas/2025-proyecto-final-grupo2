import pytest
from gestor_usuarios.dominio.reglas_negocio_login import (
    validar_data_presente,
    validar_campos_requeridos,
    validar_formato_email,
    validar_tamanio_email,
    validar_tamanio_password,
    validar_login_data
)

def test_validar_data_presente():
    assert validar_data_presente(None) == "Se requiere una solictud con payload/body."
    assert validar_data_presente({}) is None

def test_validar_campos_requeridos():
    assert validar_campos_requeridos({}) == "El campo email es requerido."
    assert validar_campos_requeridos({"email": "user@example.com"}) == "El campo password es requerido."
    assert validar_campos_requeridos({"email": "user@example.com", "password": "securepassword"}) is None

def test_validar_formato_email():
    assert validar_formato_email("invalid-email") == "Formato de email invalido."
    assert validar_formato_email("user@example.com") is None

def test_validar_tamanio_email():
    long_email = "a" * 251 + "@example.com"
    assert validar_tamanio_email(long_email) == "Campo email es muy largo."
    assert validar_tamanio_email("user@example.com") is None

def test_validar_tamanio_password():
    long_password = "a" * 251
    assert validar_tamanio_password(long_password) == "Campo password es muy largo."
    assert validar_tamanio_password("securepassword") is None

def test_validar_login_data():
    """Pruebas para validar_login_data"""
    assert validar_login_data(None) == "Se requiere una solictud con payload/body."
    assert validar_login_data({}) == "El campo email es requerido."
    assert validar_login_data({"email": "user@example.com"}) == "El campo password es requerido."
    assert validar_login_data({"email": "invalid-email", "password": "password"}) == "Formato de email invalido."
    long_email = "a" * 251 + "@example.com"
    assert validar_login_data({"email": long_email, "password": "password"}) == "Campo email es muy largo."
    long_password = "a" * 251
    assert validar_login_data({"email": "user@example.com", "password": long_password}) == "Campo password es muy largo."
    assert validar_login_data({"email": "user@example.com", "password": "securepassword"}) is None
