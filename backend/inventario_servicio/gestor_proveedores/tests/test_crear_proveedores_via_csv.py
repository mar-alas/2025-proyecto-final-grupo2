import pytest
from unittest.mock import patch
from flask import Flask
from flask.testing import FlaskClient


from aplicacion.escrituras.crear_proveedores_via_csv import crear_proveedores_via_csv_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(crear_proveedores_via_csv_bp, url_prefix="/proveedores/csv")
    return app


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token")
def test_token_no_proporcionado(mock_validar_token, client):
    response = client.post("/proveedores/csv", headers={})
    assert response.status_code == 401
    assert response.json["error"] == "No se proporciono un token"


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=False)
def test_token_invalido(mock_validar_token, client):
    response = client.post("/proveedores/csv", headers={"Authorization": "Bearer token_invalido"})
    assert response.status_code == 403
    assert response.json["message"] == "forbidden"


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
def test_body_no_json(mock_validar_token, client):
    response = client.post("/proveedores/csv", data="no es json", headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "formato JSON" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value="Falta el campo 'filepath'")
def test_body_invalido(mock_validar_body, mock_validar_token, client):
    body = {}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "Falta el campo" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_url_csv", return_value="URL inválida")
def test_url_csv_invalida(mock_validar_url, mock_validar_body, mock_validar_token, client):
    body = {"filepath": "no-es-url"}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "URL inválida" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.download_file_from_url", side_effect=Exception("Error al descargar"))
def test_falla_descarga_csv(mock_descarga, mock_validar_url, mock_validar_body, mock_validar_token, client):
    body = {"filepath": "http://valida.com/archivo.csv"}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "Error al descargar" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.download_file_from_url", return_value="contenido_csv")
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_contenido", return_value="El archivo está vacío")
def test_contenido_invalido(mock_validar_contenido, mock_descarga, mock_validar_url, mock_validar_body, mock_validar_token, client):
    body = {"filepath": "http://valida.com/archivo.csv"}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "vacío" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.download_file_from_url", return_value="contenido_csv")
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_contenido", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.obtener_lista_proveedores_desde_csv", return_value=[])
def test_lista_proveedores_vacia(mock_obtener, mock_validar_contenido, mock_descarga, mock_validar_url, mock_validar_body, mock_validar_token, client):
    body = {"filepath": "http://valida.com/archivo.csv"}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 400
    assert "lista de productos" in response.json["message"]


@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_token", return_value=True)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_body", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_url_csv", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.download_file_from_url", return_value="contenido_csv")
@patch("aplicacion.escrituras.crear_proveedores_via_csv.validar_contenido", return_value=None)
@patch("aplicacion.escrituras.crear_proveedores_via_csv.obtener_lista_proveedores_desde_csv", return_value=[{"id": 1, "nombre": "Proveedor A"}])
@patch("aplicacion.escrituras.crear_proveedores_via_csv.despachador_comandos.publicar_evento")
def test_creacion_exitosa(mock_publicar, mock_obtener, mock_validar_contenido, mock_descarga, mock_validar_url, mock_validar_body, mock_validar_token, client):
    body = {"filepath": "http://valida.com/archivo.csv"}
    response = client.post("/proveedores/csv", json=body, headers={"Authorization": "Bearer valido"})
    assert response.status_code == 201
    assert "exitosamente" in response.json["message"]
    mock_publicar.assert_called_once()
