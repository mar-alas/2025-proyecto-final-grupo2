import pytest
from unittest.mock import patch
from flask import Flask
from gestor_usuarios.aplicacion.lecturas.home import home_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    with app.test_client() as client:
        yield client

def test_home_success(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"status": "success"}

def test_home_exception(client):
    with patch("gestor_usuarios.aplicacion.lecturas.home.jsonify", side_effect=Exception("Forced Error")):
        response = client.get('/')
        assert response.status_code == 500