import pytest
from unittest.mock import patch, MagicMock
from gestor_usuarios.aplicacion.lecturas.login import login_user_bp
from flask import Flask

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(login_user_bp, url_prefix="/login")
    app.config["TESTING"] = True
    return app.test_client()

def test_login_exitoso(client):
    data = {"email": "test@example.com", "password": "123456"}

    mock_user = MagicMock()
    mock_user.id = "abc-123"
    mock_user.role = "admin"
    mock_user.password = "hashed-password"

    with patch("gestor_usuarios.aplicacion.lecturas.login.UserRepository.get_by_email", return_value=mock_user), \
         patch("gestor_usuarios.aplicacion.lecturas.login.check_password_hash", return_value=True), \
         patch("gestor_usuarios.aplicacion.lecturas.login.generar_token", return_value="fake-token"):
        
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 200
        assert body["message"] == "Inicio de sesion exitoso."
        assert body["userId"] == "abc-123"
        assert body["role"] == "admin"
        assert body["accessToken"] == "fake-token"

def test_login_usuario_no_encontrado(client):
    data = {"email": "notfound@example.com", "password": "123456"}

    with patch("gestor_usuarios.aplicacion.lecturas.login.UserRepository.get_by_email", return_value=None):
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 404
        assert body["message"] == "Usuario no encontrado."

def test_login_password_incorrecta(client):
    data = {"email": "test@example.com", "password": "wrongpass"}

    mock_user = MagicMock()
    mock_user.password = "hashed-pass"

    with patch("gestor_usuarios.aplicacion.lecturas.login.UserRepository.get_by_email", return_value=mock_user), \
         patch("gestor_usuarios.aplicacion.lecturas.login.check_password_hash", return_value=False):
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 400
        assert body["message"] == "Contrasena incorrecta."

def test_login_datos_invalidos(client):
    data = {"email": ""}  # faltó la contraseña

    with patch("gestor_usuarios.aplicacion.lecturas.login.validar_login_data", return_value="Datos incompletos"):
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 400
        assert body["message"] == "Datos incompletos"


def test_login_password_encriptada(client):
    data = {"email": "test@example.com", "password": "encrypted-pass", "isEncrypted": True}

    mock_user = MagicMock()
    mock_user.id = "abc-123"
    mock_user.role = "admin"
    mock_user.password = "hashed-password"

    with patch("gestor_usuarios.aplicacion.lecturas.login.UserRepository.get_by_email", return_value=mock_user), \
         patch("gestor_usuarios.aplicacion.lecturas.login.decrypt_password", return_value="plain-pass"), \
         patch("gestor_usuarios.aplicacion.lecturas.login.check_password_hash", return_value=True), \
         patch("gestor_usuarios.aplicacion.lecturas.login.generar_token", return_value="fake-token"):
        
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 200
        assert body["message"] == "Inicio de sesion exitoso."


def test_login_password_encriptada_invalida(client):
    data = {"email": "test@example.com", "password": "bad-encrypted-pass", "isEncrypted": True}

    mock_user = MagicMock()
    mock_user.password = "hashed-password"

    with patch("gestor_usuarios.aplicacion.lecturas.login.UserRepository.get_by_email", return_value=mock_user), \
         patch("gestor_usuarios.aplicacion.lecturas.login.decrypt_password", side_effect=ValueError("error de decrypt")), \
         patch("gestor_usuarios.aplicacion.lecturas.login.check_password_hash"):
        response = client.post("/login", json=data)
        body = response.get_json()

        assert response.status_code == 400
        assert body["message"] == "Contrasena incorrecta."
