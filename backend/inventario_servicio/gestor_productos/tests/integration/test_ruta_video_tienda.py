import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from aplicacion.escrituras.procesar_video_tienda import procesar_video_tienda_bp
from infraestructura.database import db

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(procesar_video_tienda_bp, url_prefix="/procesar")
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client


@patch("aplicacion.escrituras.procesar_video_tienda.AccessTokenValidator.validate")
@patch("aplicacion.escrituras.procesar_video_tienda.ProcesadorVideo")
def test_procesar_video_exitoso(mock_procesador_class, mock_validate, client):
    mock_validate.return_value = (True, "")
    mock_instance_procesador = MagicMock()
    mock_instance_procesador.procesar.return_value = {
        "mensaje": "Procesamiento fue exitoso",
        "recomendaciones": [{"producto": "Leche"}],
        "recomendacion_pedido": {
            "cliente_id": 123,
            "productos": [{"nombre": "Pan"}]
        }
    }

    mock_procesador_class.return_value = mock_instance_procesador

    payload = {
        "cliente_id": 123,
        "info_video": [
            {"nombre_producto": "Leche", "ubicacion": "Pasillo 3", "cantidad": 2},
            {"nombre_producto": "Cerveza", "ubicacion": "Pasillo 1", "cantidad": 10}
        ]
    }

    headers = {"Authorization": "Bearer fake_token"}
    response = client.post("/procesar", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data["mensaje"] == "Procesamiento fue exitoso"
    assert isinstance(data["recomendaciones"], list)
    assert data["recomendacion_pedido"]["cliente_id"] == 123


@patch("aplicacion.escrituras.procesar_video_tienda.AccessTokenValidator.validate")
@patch("aplicacion.escrituras.procesar_video_tienda.ProcesadorVideo")
def test_procesar_video_error_en_servicio(mock_procesador, mock_validate, client):
    mock_validate.return_value = (True, "")
    mock_procesador.procesar.side_effect = Exception("Fallo interno")

    payload = {
        "cliente_id": 123,
        "info_video": [
            {"nombre_producto": "Algo", "ubicacion": "X", "cantidad": 1}
        ]
    }

    headers = {"Authorization": "Bearer fake_token"}
    response = client.post("/procesar", json=payload, headers=headers)

    assert response.status_code == 500
    assert "Error al consultar la lista de productos" in response.get_json()["message"]


@patch("aplicacion.escrituras.procesar_video_tienda.AccessTokenValidator.validate")
def test_procesar_video_falla_formato_json(mock_validate, client):
    mock_validate.return_value = (True, "")
    headers = {"Authorization": "Bearer fake_token"}
    response = client.post("/procesar", data="esto no es json", content_type="application/json", headers=headers)

    assert response.status_code == 500
    assert "Error al consultar la lista de productos" in response.get_json()["message"]
