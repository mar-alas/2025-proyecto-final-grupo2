from unittest.mock import MagicMock, patch
import pytest
from flask import Flask
from gestor_usuarios.aplicacion.escrituras.registrar_user import registrar_user_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(registrar_user_bp, url_prefix="/api/users")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_registrar_user_exception(client):
    # Datos de entrada válidos
    payload = {
        "name": "Usuario Error",
        "email": "error@ejemplo.com",
        "password": "secreta123",
        "role": "admin",
        "country": "CO",
        "city": "Bogotá",
        "address": "Calle Falsa 123"
    }

    # Mock a UserRepository para que lance excepción en .save()
    with patch("gestor_usuarios.aplicacion.escrituras.registrar_user.UserRepository") as MockRepo:
        instance = MockRepo.return_value
        instance.get_by_email.return_value = None  # Para que no entre al 409
        instance.save.side_effect = Exception("Error forzado")

        response = client.post("/api/users", json=payload)

        assert response.status_code == 500
        assert "Error en registro" in response.json["message"]
