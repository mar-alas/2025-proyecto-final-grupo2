from flask import Flask
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from infraestructura import get_all_products_repository

def test_consultar_productos_ok(monkeypatch):
    monkeypatch.setattr(
        get_all_products_repository.ProductoRepository,
        "obtener_todos",
        lambda self: [{"id": 1, "nombre": "Mock Producto"}]
    )

    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    response = client.get("/test")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Lista de productos recuperada exitosamente"
    assert data["data"][0]["nombre"] == "Mock Producto"


