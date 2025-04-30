import pytest
from unittest.mock import patch
from flask import Flask
from gestor_usuarios.aplicacion.lecturas.get_all_sellers import get_all_sellers_bp

# Fake seller class to simulate repository results
class FakeSeller:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(get_all_sellers_bp, url_prefix='/api/v1/seguridad/gestor_usuarios/r/vendedores')
    with app.test_client() as client:
        yield client

def test_get_all_sellers_success(client):
    mock_sellers = [
        FakeSeller(1, 'Carlos Pérez', 'carlos@example.com'),
        FakeSeller(2, 'Ana Gómez', 'ana@example.com')
    ]

    with patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.UserRepository') as MockRepo, \
         patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.validar_token') as mock_validar_token:
        
        mock_validar_token.return_value = True
        instance = MockRepo.return_value
        instance.get_all_sellers.return_value = mock_sellers

        response = client.get('/api/v1/seguridad/gestor_usuarios/r/vendedores', headers={"Authorization": "Bearer fake-token"})
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == 'Usuarios consultados exitosamente.'
        assert len(data['vendedores']) == 2
        assert data['vendedores'][0]['name'] == 'Carlos Pérez'
        assert data['vendedores'][1]['email'] == 'ana@example.com'

def test_get_all_sellers_error(client):
    with patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.UserRepository') as MockRepo, \
         patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.validar_token') as mock_validar_token:
        
        mock_validar_token.return_value = True
        instance = MockRepo.return_value
        instance.get_all_sellers.side_effect = Exception("Error inesperado")

        response = client.get(
            '/api/v1/seguridad/gestor_usuarios/r/vendedores',
            headers={"Authorization": "Bearer fake-token"}
        )
        data = response.get_json()

        assert response.status_code == 500
        assert data['status'] == 'FAILED'
        assert data['message'] == 'Ocurrio un error inesperado al recuperar los vendedores.'
        assert data['vendedores'] == []

def test_get_all_sellers_empty_list(client):
    with patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.UserRepository') as MockRepo, \
         patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.validar_token') as mock_validar_token:
        
        mock_validar_token.return_value = True
        instance = MockRepo.return_value
        instance.get_all_sellers.return_value = []

        response = client.get(
            '/api/v1/seguridad/gestor_usuarios/r/vendedores',
            headers={"Authorization": "Bearer fake-token"}
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == 'No hay vendedores registrados.'
        assert data['vendedores'] == []

def test_get_all_sellers_missing_token(client):
    response = client.get('/api/v1/seguridad/gestor_usuarios/r/vendedores')
    data = response.get_json()

    assert response.status_code == 401
    assert data['status'] == 'FAILED'
    assert data['message'] == 'No se proporciono un token'

def test_get_all_sellers_invalid_token(client):
    with patch('gestor_usuarios.aplicacion.lecturas.get_all_sellers.validar_token') as mock_validar_token:
        mock_validar_token.return_value = False

        response = client.get(
            '/api/v1/seguridad/gestor_usuarios/r/vendedores',
            headers={"Authorization": "Bearer token_invalido"}
        )
        data = response.get_json()

        assert response.status_code == 403
        assert data['status'] == 'FAILED'
        assert data['message'] == 'forbidden'