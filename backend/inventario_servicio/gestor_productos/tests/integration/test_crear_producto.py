import pytest
from flask import Flask, json
from unittest.mock import patch, MagicMock
from aplicacion.escrituras.crear_producto import crear_producto_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(crear_producto_bp, url_prefix="/productos")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def headers_validos():
    return {"Authorization": "Bearer token_valido"}

def test_producto_unico_exitoso(client, headers_validos):
    producto = {
        "nombre": "Producto Uno",
        "descripcion": "Descripción",
        "tiempo_entrega": "2 días",
        "precio": 100.0,
        "condiciones_almacenamiento": "Seco",
        "fecha_vencimiento": "2025-12-31",
        "estado": "en_stock",
        "inventario_inicial": 10,
        "imagenes_productos": ["img1.jpg"],
        "proveedor": "Proveedor A"
    }

    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", return_value=(True, "")), \
         patch("aplicacion.escrituras.crear_producto.validar_datos_producto", return_value=None), \
         patch("aplicacion.escrituras.crear_producto.ProductRepository") as mock_repo:

        repo_instance = mock_repo.return_value
        repo_instance.get_by_name.return_value = None
        producto_mock = MagicMock()
        producto_mock.to_dict.return_value = producto
        repo_instance.save.return_value = producto_mock

        response = client.post("/productos", json=producto, headers=headers_validos)
        assert response.status_code == 201
        assert response.json["nombre"] == "Producto Uno"

def test_producto_unico_con_error_de_validacion(client, headers_validos):
    producto = {"descripcion": "Falta nombre"}

    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", return_value=(True, "")), \
         patch("aplicacion.escrituras.crear_producto.validar_datos_producto", return_value="El campo 'nombre' es requerido."):

        response = client.post("/productos", json=producto, headers=headers_validos)
        assert response.status_code == 207
        body = response.json
        assert body["fallidos"] == 1
        assert body["resultados"][0]["error"] == "El campo 'nombre' es requerido."

def test_multiples_productos_con_errores_y_exitos(client, headers_validos):
    productos = [
        {
            "nombre": "Exitoso",
            "descripcion": "OK",
            "tiempo_entrega": "1 día",
            "precio": 10,
            "condiciones_almacenamiento": "Fresco",
            "fecha_vencimiento": "2025-01-01",
            "estado": "en_stock",
            "inventario_inicial": 20,
            "imagenes_productos": [],
            "proveedor": "Proveedor X"
        },
        {
            "descripcion": "Falta nombre"
        }
    ]

    def validacion_mock(producto):
        return None if "nombre" in producto else "El campo 'nombre' es requerido."

    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", return_value=(True, "")), \
         patch("aplicacion.escrituras.crear_producto.validar_datos_producto", side_effect=validacion_mock), \
         patch("aplicacion.escrituras.crear_producto.ProductRepository") as mock_repo:

        repo_instance = mock_repo.return_value
        repo_instance.get_by_name.return_value = None
        producto_mock = MagicMock()
        producto_mock.to_dict.return_value = productos[0]
        repo_instance.save.return_value = producto_mock

        response = client.post("/productos", json=productos, headers=headers_validos)
        assert response.status_code == 207
        assert response.json["total"] == 2
        assert response.json["exitosos"] == 1
        assert response.json["fallidos"] == 1

def test_token_invalido(client):
    response = client.post("/productos", json={}, headers={"Authorization": "Bearer invalido"})
    assert response.status_code == 403 or response.status_code == 401 

def test_sin_token(client):
    response = client.post("/productos", json={})
    assert response.status_code == 401
    assert "token" in response.json["message"]

def test_request_no_json(client, headers_validos):
    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", return_value=(True, "")):
        response = client.post("/productos", data="no es json", headers=headers_validos)
        assert response.status_code == 400
        assert "JSON" in response.json["message"]

def test_producto_duplicado(client, headers_validos):
    producto = {
        "nombre": "Duplicado",
        "descripcion": "desc",
        "tiempo_entrega": "2 días",
        "precio": 100.0,
        "condiciones_almacenamiento": "Seco",
        "fecha_vencimiento": "2025-12-31",
        "estado": "en_stock",
        "inventario_inicial": 10,
        "imagenes_productos": [],
        "proveedor": "Proveedor A"
    }

    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", return_value=(True, "")), \
         patch("aplicacion.escrituras.crear_producto.validar_datos_producto", return_value=None), \
         patch("aplicacion.escrituras.crear_producto.ProductRepository") as mock_repo:

        repo_instance = mock_repo.return_value
        repo_instance.get_by_name.return_value = True

        response = client.post("/productos", json=producto, headers=headers_validos)
        assert response.status_code == 207
        assert response.json["fallidos"] == 1
        assert "ya esta registrado" in response.json["resultados"][0]["error"]

def test_excepcion_general(client, headers_validos):
    with patch("aplicacion.escrituras.crear_producto.AccessTokenValidator.validate", side_effect=Exception("Boom!")):
        response = client.post("/productos", json={}, headers=headers_validos)
        assert response.status_code == 500
        assert "Error en registro" in response.json["message"]

def test_token_mal_formado(client):
    headers = {"Authorization": "Bearer"}
    response = client.post("/productos", json={}, headers=headers)
    assert response.status_code == 401
    assert "formato" in response.json["message"].lower()

