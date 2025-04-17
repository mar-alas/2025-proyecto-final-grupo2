from flask import Flask
from aplicacion.lecturas.consultar_productos import consultar_productos_bp
from infraestructura import get_all_products_repository
import jwt
import datetime


def generar_token_valido(secret_key='clave_secreta_para_firmar_token', role='director-compras'):
    payload = {
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def test_consultar_productos_falla(monkeypatch):
    def lanzar_excepcion(_):
        raise Exception("Error forzado")

    monkeypatch.setattr(
        get_all_products_repository.ProductoRepository,
        "obtener_todos",
        lanzar_excepcion
    )

    token = generar_token_valido()

    app = Flask(__name__)
    app.register_blueprint(consultar_productos_bp, url_prefix="/test")
    client = app.test_client()

    # Agregar token en los headers del request
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get("/test", headers=headers)

    assert response.status_code == 500
    assert "Error al consultar la lista de productos" in response.get_json()["message"]

