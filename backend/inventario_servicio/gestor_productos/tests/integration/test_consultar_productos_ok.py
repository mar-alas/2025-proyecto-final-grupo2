from flask import Flask
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from dominio.product_repository import ProductRepository

class MockProduct:
    def to_dict(self):
        return {"id": 1, "nombre": "Mock Producto"}


def test_consultar_productos_ok(monkeypatch):

    monkeypatch.setattr(
        ProductRepository,
        "get_all",
        lambda self, code=None, name=None, status=None, page=1, limit=20: ([MockProduct()], 1)
    )

    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    response = client.get("/test")
    assert response.status_code == 200
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "products" in data
    assert "limit" in data
    assert "page" in data
    assert "total" in data
    assert "total_pages" in data
