from flask import Flask
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from dominio.product_repository import ProductRepository
import jwt
import datetime

# Mock del producto
class MockProduct:
    def to_dict(self):
        return {"id": 1, "nombre": "Mock Producto"}

# Función para generar un token válido
def generar_token_valido(secret_key='clave_secreta_para_firmar_token', role='director-compras'):
    payload = {
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

# Test principal
def test_consultar_productos_ok(monkeypatch):
    # Mockear la respuesta del repositorio
    monkeypatch.setattr(
        ProductRepository,
        "get_all",
        lambda self, code=None, name=None, status=None, page=1, limit=20: ([MockProduct()], 1)
    )

    # Crear app y cliente
    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    # Generar token y agregarlo al header
    token = generar_token_valido()
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Ejecutar request con token
    response = client.get("/test", headers=headers)

    # Verificaciones
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert "products" in data
    assert "limit" in data
    assert "page" in data
    assert "total" in data
    assert "total_pages" in data

def test_consultar_productos_token_expirado(monkeypatch):
    payload = {
        "role": "director-compras",
        "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)  # ya expirado
    }
    token = jwt.encode(payload, 'clave_secreta_para_firmar_token', algorithm='HS256')
    headers = {"Authorization": f"Bearer {token}"}

    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    response = client.get("/test", headers=headers)
    assert response.status_code == 403
    assert response.get_json()["message"] == "Token expirado"