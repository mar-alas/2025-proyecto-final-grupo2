import pytest
from flask import Flask
from gestor_usuarios.aplicacion.lecturas.ping import ping_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(ping_bp, url_prefix='/api/v1/seguridad/gestor_usuarios')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_ping_endpoint(client):
    response = client.get('/api/v1/seguridad/gestor_usuarios/ping')
    assert response.status_code == 200
    assert response.json == {"message": "pong"}