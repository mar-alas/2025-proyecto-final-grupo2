import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from aplicacion.escrituras.crear_producto import crear_producto_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(crear_producto_bp, url_prefix="/productos")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch("aplicacion.escrituras.crear_producto.AccessTokenValidator")
@patch("aplicacion.escrituras.crear_producto.CrearProductoService")
@patch("aplicacion.escrituras.crear_producto.PulsarPublisher")
@patch("aplicacion.escrituras.crear_producto.ProductRepository")
def test_crear_producto_exitosamente(
    mock_product_repo,
    mock_pulsar_publisher,
    mock_crear_producto_service,
    mock_token_validator,
    client,
):
    # Arrange
    token = "Bearer valid.token"
    producto_mock = {
        "id": "123",
        "nombre": "Producto de prueba",
        "descripcion": "Descripción",
        "precio": 100
    }

    # Configurar mocks
    mock_token_validator.return_value.validate.return_value = (True, "OK")
    mock_crear_producto_service.return_value.crear.return_value = {
        "total": 1,
        "exitosos": 1,
        "resultados": [{"producto": producto_mock}]
    }

    payload = {
        "nombre": "Producto de prueba",
        "descripcion": "Descripción",
        "precio": 100
    }

    # Act
    response = client.post(
        "/productos",
        headers={"Authorization": token},
        json=payload
    )

    # Assert
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data == producto_mock


def test_crear_producto_falla_sin_token(client):
    payload = {
        "nombre": "Producto de prueba",
        "descripcion": "Descripción",
        "precio": 100
    }

    response = client.post("/productos", json=payload)

    assert response.status_code == 401
    assert response.get_json() == {
        "status": "FAILED",
        "message": "No se proporciono un token"
    }


def test_crear_producto_falla_token_mal_formado(client):
    payload = {
        "nombre": "Producto de prueba",
        "descripcion": "Descripción",
        "precio": 100
    }

    response = client.post("/productos", headers={"Authorization": "BearerOnly"}, json=payload)

    assert response.status_code == 401
    assert response.get_json() == {
        "status": "FAILED",
        "message": "Formato del token invalido"
    }


@patch("aplicacion.escrituras.crear_producto.AccessTokenValidator")
def test_crear_producto_falla_token_invalido(mock_token_validator, client):
    mock_token_validator.return_value.validate.return_value = (False, "Token expirado")

    payload = {
        "nombre": "Producto de prueba",
        "descripcion": "Descripción",
        "precio": 100
    }

    response = client.post("/productos", headers={"Authorization": "Bearer invalido.token"}, json=payload)

    assert response.status_code == 403
    assert response.get_json() == {
        "status": "FAILED",
        "message": "Token expirado"
    }


@patch("aplicacion.escrituras.crear_producto.AccessTokenValidator")
def test_crear_producto_falla_sin_json(mock_token_validator, client):
    mock_token_validator.return_value.validate.return_value = (True, "OK")

    response = client.post("/productos", headers={"Authorization": "Bearer token.valido"}, data="no es json")

    assert response.status_code == 400
    assert response.get_json() == {
        "status": "FAILED",
        "message": "Se requiere un cuerpo con formato JSON"
    }


@patch("aplicacion.escrituras.crear_producto.AccessTokenValidator")
@patch("aplicacion.escrituras.crear_producto.CrearProductoService")
@patch("aplicacion.escrituras.crear_producto.PulsarPublisher")
@patch("aplicacion.escrituras.crear_producto.ProductRepository")
def test_crear_producto_parcialmente_exitoso(
    mock_product_repo,
    mock_pulsar_publisher,
    mock_crear_producto_service,
    mock_token_validator,
    client
):
    mock_token_validator.return_value.validate.return_value = (True, "OK")
    mock_crear_producto_service.return_value.crear.return_value = {
        "total": 3,
        "exitosos": 2,
        "resultados": [
            {"producto": {"nombre": "ok1"}},
            {"producto": {"nombre": "ok2"}},
            {"error": "Falta campo X"}
        ]
    }

    payload = [
        {"nombre": "ok1", "precio": 100},
        {"nombre": "ok2", "precio": 200},
        {"descripcion": "sin nombre"}
    ]

    response = client.post("/productos", headers={"Authorization": "Bearer token.valido"}, json=payload)

    assert response.status_code == 207
    data = response.get_json()
    assert data["total"] == 3
    assert data["exitosos"] == 2



@patch("aplicacion.escrituras.crear_producto.AccessTokenValidator")
@patch("aplicacion.escrituras.crear_producto.ProductRepository")
@patch("aplicacion.escrituras.crear_producto.PulsarPublisher", side_effect=Exception("Fallo interno"))
def test_crear_producto_error_interno(
    mock_pulsar,
    mock_repo,
    mock_token_validator,
    client
):
    mock_token_validator.return_value.validate.return_value = (True, "OK")
    
    payload = {"nombre": "Test", "precio": 100}

    response = client.post("/productos", headers={"Authorization": "Bearer valido"}, json=payload)

    assert response.status_code == 500
    assert "Error en registro" in response.get_json()["message"]
