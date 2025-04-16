from flask import Flask
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from infraestructura import get_all_products_repository


def test_consultar_productos_falla(monkeypatch):
    def lanzar_excepcion(_):
        raise Exception("Error forzado")

    monkeypatch.setattr(
        get_all_products_repository.ProductoRepository,
        "obtener_todos",
        lanzar_excepcion
    )

    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    response = client.get("/test")
    assert response.status_code == 500
    assert "Error al consultar la lista de productos" in response.get_json()["message"]
