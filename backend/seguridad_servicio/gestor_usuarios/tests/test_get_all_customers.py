import pytest
from unittest.mock import patch
from flask import Flask
from gestor_usuarios.aplicacion.lecturas.get_all_customers import get_all_customers_bp

# Clase simple que simula lo que devuelve el repositorio real
class FakeUser:
    def __init__(self, id, name, email, country, city, address):
        self.id = id
        self.name = name
        self.email = email
        self.country = country
        self.city = city
        self.address = address

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(get_all_customers_bp, url_prefix='/api/v1/seguridad/gestor_usuarios/r/clientes')
    with app.test_client() as client:
        yield client

def test_get_all_customers_success(client):
    mock_users = [
        FakeUser(1, 'Juan Pérez', 'juan@example.com', 'Colombia', 'Bogotá', 'Calle 123'),
        FakeUser(2, 'Ana Gómez', 'ana@example.com', 'México', 'CDMX', 'Av Reforma')
    ]

    with patch('gestor_usuarios.aplicacion.lecturas.get_all_customers.UserRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_all_customers.return_value = mock_users

        response = client.get('/api/v1/seguridad/gestor_usuarios/r/clientes')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == 'Usuarios consultados exitosamente.'
        assert len(data['clientes']) == 2
        assert data['clientes'][0]['name'] == 'Juan Pérez'
        assert data['clientes'][1]['email'] == 'ana@example.com'

def test_get_all_customers_error(client):
    with patch('gestor_usuarios.aplicacion.lecturas.get_all_customers.UserRepository') as MockRepo:
        instance = MockRepo.return_value
        # Simula una excepción inesperada al invocar get_all_customers
        instance.get_all_customers.side_effect = Exception("Error inesperado")

        response = client.get('/api/v1/seguridad/gestor_usuarios/r/clientes')
        data = response.get_json()

        assert response.status_code == 500
        assert data['status'] == 'FAILED'
        assert data['message'] == 'Ocurrio un error inesperado al recuperar los clientes.'
        assert data['clientes'] == []


def test_get_all_customers_empty_list(client):
    with patch('gestor_usuarios.aplicacion.lecturas.get_all_customers.UserRepository') as MockRepo:
        instance = MockRepo.return_value
        instance.get_all_customers.return_value = []

        response = client.get('/api/v1/seguridad/gestor_usuarios/r/clientes')
        data = response.get_json()

        assert response.status_code == 200
        assert data['status'] == 'success'
        assert data['message'] == 'No hay clientes registrados.'
        assert data['clientes'] == []
