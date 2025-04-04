import pytest
from unittest.mock import MagicMock, patch
from flask import Flask, json

from gestor_usuarios.aplicacion.escrituras.registrar_user import registrar_user_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(registrar_user_bp, url_prefix="/users")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@patch("gestor_usuarios.aplicacion.escrituras.registrar_user.UserRepository")
def test_registro_usuario_exitoso(mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by_email.side_effect = [None, MagicMock(id=123)]  # No existe al inicio, luego ya está creado
    mock_repo_class.return_value = mock_repo

    payload = {
        "name": "Jhon",
        "email": "jhon@example.com",
        "password": "secure123",
        "role": "admin",
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle Falsa 123"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Usuario registrado exitosamente."
    assert data["userId"] == 123
    mock_repo.save.assert_called_once()

@patch("gestor_usuarios.aplicacion.escrituras.registrar_user.UserRepository")
def test_usuario_ya_registrado(mock_repo_class, client):
    mock_repo = MagicMock()
    mock_repo.get_by_email.return_value = MagicMock()
    mock_repo_class.return_value = mock_repo

    payload = {
        "name": "Jhon",
        "email": "jhon@example.com",
        "password": "secure123"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 409
    assert response.get_json()["message"] == "El usuario ya se encuentra registrado."
    mock_repo.save.assert_not_called()

@patch("gestor_usuarios.aplicacion.escrituras.registrar_user.UserRepository")
def test_datos_invalidos(mock_repo_class, client):
    mock_repo_class.return_value = MagicMock()

    # No se pasa email ni password
    payload = {
        "name": "Jhon"
    }

    response = client.post("/users", json=payload)

    assert response.status_code == 400
    assert "message" in response.get_json()
