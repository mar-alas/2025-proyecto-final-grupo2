import pytest
from gestor_usuarios.dominio.reglas_negocio import (
    validar_campos_requeridos,
    validar_formato_email,
    validar_tamanio_name,
    validar_role,
    role_esta_presente,
    country_esta_presente,
    city_esta_presente,
    address_esta_presente,
    validar_datos_usuario
)


def test_validar_campos_requeridos():
    data_valida = {"name": "John", "email": "john@example.com", "password": "12345"}
    assert validar_campos_requeridos(data_valida) is None
    
    data_invalida = {"name": "John", "email": "john@example.com"}  # Falta 'password'
    assert validar_campos_requeridos(data_invalida) == "El campo password es requerido."

def test_validar_formato_email():
    assert validar_formato_email("user@example.com") is None
    assert validar_formato_email("invalid-email") == "Formato de correo invalido."
    assert validar_formato_email("user@com") == "Formato de correo invalido."

def test_validar_tamanio_name():
    assert validar_tamanio_name("A" * 250) is None
    assert validar_tamanio_name("A" * 251) == "Campo name es muy largo."

def test_validar_role():
    assert validar_role({"role": "admin"}) is True
    assert validar_role({"role": "invalid_role"}) is False

def test_role_esta_presente():
    assert role_esta_presente({"role": "admin"}) is True
    assert role_esta_presente({}) is False

def test_country_esta_presente():
    assert country_esta_presente({"country": "Colombia"}) is True
    assert country_esta_presente({}) is False

def test_city_esta_presente():
    assert city_esta_presente({"city": "Bogotá"}) is True
    assert city_esta_presente({}) is False

def test_address_esta_presente():
    assert address_esta_presente({"address": "Calle 123"}) is True
    assert address_esta_presente({}) is False

def test_validar_datos_usuario():
    # Caso válido
    data_valida = {"name": "John", "email": "john@example.com", "password": "12345"}
    assert validar_datos_usuario(data_valida) is None
    
    # Falta campo requerido
    data_sin_password = {"name": "John", "email": "john@example.com"}
    assert validar_datos_usuario(data_sin_password) == "El campo password es requerido."
    
    # Email inválido
    data_email_invalido = {"name": "John", "email": "invalid-email", "password": "12345"}
    assert validar_datos_usuario(data_email_invalido) == "Formato de correo invalido."
    
    # Nombre demasiado largo
    data_nombre_largo = {"name": "A" * 251, "email": "john@example.com", "password": "12345"}
    assert validar_datos_usuario(data_nombre_largo) == "Campo name es muy largo."