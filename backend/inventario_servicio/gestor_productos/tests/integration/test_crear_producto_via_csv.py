import pytest
from flask import Flask, json
from unittest.mock import patch
from aplicacion.escrituras.crear_productos_via_csv import crear_producto_via_csv_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(crear_producto_via_csv_bp, url_prefix="/productos-csv")
    with app.test_client() as client:
        yield client


def test_sin_token(client):
    response = client.post("/productos-csv")
    assert response.status_code == 401
    assert response.get_json()["message"] == "No se proporciono un token"


def test_token_mal_formado(client):
    headers = {"Authorization": "BearerOnly"}
    response = client.post("/productos-csv", headers=headers)
    assert response.status_code == 401
    assert response.get_json()["message"] == "Formato del token invalido"


@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_token_invalido(mock_validator, client):
    mock_validator.return_value.validate.return_value = (False, "Token no válido")
    headers = {"Authorization": "Bearer fake.token"}
    response = client.post("/productos-csv", headers=headers)
    assert response.status_code == 403
    assert response.get_json()["message"] == "Token no válido"


@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_sin_json(mock_validator, client):
    mock_validator.return_value.validate.return_value = (True, "OK")
    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, data="texto plano")
    assert response.status_code == 400
    assert response.get_json()["message"] == "Se requiere un cuerpo con formato JSON"


@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value="Campo filepath es requerido")
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_body_invalido(mock_validator, mock_validar_body, client):
    mock_validator.return_value.validate.return_value = (True, "OK")
    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={})
    assert response.status_code == 400
    assert "Campo filepath" in response.get_json()["message"]


@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_url_csv", return_value="URL inválida")
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_url_csv_invalida(mock_validator, mock_validar_url, mock_validar_body, client):
    mock_validator.return_value.validate.return_value = (True, "OK")
    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={"filepath": "bad-url"})
    assert response.status_code == 400
    assert "URL inválida" in response.get_json()["message"]


@patch("aplicacion.escrituras.crear_productos_via_csv.download_file_from_url", side_effect=Exception("descarga fallida"))
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_descarga_falla(mock_validator, mock_body, mock_url, mock_download, client):
    mock_validator.return_value.validate.return_value = (True, "OK")
    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={"filepath": "https://file.csv"})
    assert response.status_code == 400
    assert "descarga fallida" in response.get_json()["message"]


@patch("aplicacion.escrituras.crear_productos_via_csv.obtener_lista_productos_desde_csv", return_value=[])
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_contenido", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.download_file_from_url", return_value="data")
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_lista_vacia(
    mock_validator, mock_body, mock_url, mock_download, mock_validar_contenido, mock_mapper, client
):
    mock_validator.return_value.validate.return_value = (True, "OK")
    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={"filepath": "https://file.csv"})
    assert response.status_code == 400
    assert "No se logro obtener la lista" in response.get_json()["message"]


@patch("aplicacion.escrituras.crear_productos_via_csv.CrearProductoService")
@patch("aplicacion.escrituras.crear_productos_via_csv.PulsarPublisher")
@patch("aplicacion.escrituras.crear_productos_via_csv.ProductRepository")
@patch("aplicacion.escrituras.crear_productos_via_csv.obtener_lista_productos_desde_csv", return_value=[{"producto": "mock"}])
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_contenido", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.download_file_from_url", return_value="csv data")
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_exito_creacion_producto_unico(
    mock_validator,
    mock_validar_body,
    mock_validar_url,
    mock_download,
    mock_validar_contenido,
    mock_mapper,
    mock_repo,
    mock_pub,
    mock_service,
    client
):
    mock_validator.return_value.validate.return_value = (True, "OK")
    mock_service.return_value.crear.return_value = {
        "total": 1,
        "exitosos": 1,
        "resultados": [{"producto": {"id": 1, "nombre": "mock"}}]
    }

    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={"filepath": "https://ok.csv"})
    assert response.status_code == 201
    assert response.get_json()["nombre"] == "mock"


@patch("aplicacion.escrituras.crear_productos_via_csv.CrearProductoService")
@patch("aplicacion.escrituras.crear_productos_via_csv.PulsarPublisher")
@patch("aplicacion.escrituras.crear_productos_via_csv.ProductRepository")
@patch("aplicacion.escrituras.crear_productos_via_csv.obtener_lista_productos_desde_csv", return_value=[{"producto": "mock1"}, {"producto": "mock2"}])
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_contenido", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.download_file_from_url", return_value="csv data")
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_productos_via_csv.AccessTokenValidator")
def test_exito_creacion_multiples_productos(
    mock_validator,
    mock_validar_body,
    mock_validar_url,
    mock_download,
    mock_validar_contenido,
    mock_mapper,
    mock_repo,
    mock_pub,
    mock_service,
    client
):
    mock_validator.return_value.validate.return_value = (True, "OK")
    mock_service.return_value.crear.return_value = {
        "total": 2,
        "exitosos": 2,
        "resultados": [
            {"producto": {"id": 1, "nombre": "mock1"}},
            {"producto": {"id": 2, "nombre": "mock2"}}
        ]
    }

    headers = {"Authorization": "Bearer token.valido"}
    response = client.post("/productos-csv", headers=headers, json={"filepath": "https://ok.csv"})
    assert response.status_code == 207
    body = response.get_json()
    assert isinstance(body, dict)
    assert len(body["resultados"]) == 2
