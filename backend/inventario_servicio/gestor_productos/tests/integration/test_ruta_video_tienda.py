import pytest
from unittest.mock import patch
from flask import Flask, json
from aplicacion.escrituras.procesar_video_tienda import procesar_video_tienda_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(procesar_video_tienda_bp, url_prefix="/procesar")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@patch("infraestructura.video_processor")
def test_procesar_video_exitoso(mock_service, client):
    mock_service.return_value.procesar.return_value = {
        "mensaje": "Procesamiento fue exitoso",
        "recomendaciones": [{"producto": "Leche"}],
        "recomendacion_pedido": {
            "cliente_id": 123,
            "productos": [{"nombre": "Pan"}]
        }
    }

    payload = {
        "cliente_id": 123,
        "info_video": [
            {"nombre_producto": "Leche", "ubicacion": "Pasillo 3", "cantidad": 2},
            {"nombre_producto": "Cerveza", "ubicacion": "Pasillo 1", "cantidad": 10}
        ]
    }

    response = client.post("/procesar", json=payload)

    assert response.status_code == 201
    data = response.get_json()
    assert data["mensaje"] == "Procesamiento fue exitoso"
    assert isinstance(data["recomendaciones"], list)
    assert data["recomendacion_pedido"]["cliente_id"] == 123


@patch("infraestructura.video_processor")
def test_procesar_video_error_en_servicio(mock_service, client):
    mock_service.return_value.procesar.side_effect = Exception("Fallo interno")

    payload = {
        "cliente_id": 123,
        "info_video": []
    }

    response = client.post("/procesar", json=payload)

    assert response.status_code == 400


def test_procesar_video_falla_formato_json(client):
    response = client.post("/procesar", data="esto no es json", content_type="application/json")

    assert response.status_code == 500
    assert "Error al consultar la lista de productos" in response.get_json()["message"]
