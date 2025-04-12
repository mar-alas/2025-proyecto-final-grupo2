import pytest
import jwt
from datetime import datetime, timedelta, timezone
from app import create_app
from unittest.mock import patch

SECRET = "clave_secreta_para_firmar_token"
URL_CREATE_PRODUCTS = "/api/v1/inventario/gestor_productos/productos"


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def generar_token_con_rol(rol: str, exp: datetime = None):
    payload = {"role": rol}
    if exp:
        payload["exp"] = exp
    return jwt.encode(payload, SECRET, algorithm="HS256")


class TestCrearProductoAutenticacion:

    def test_deberia_devolver_401_si_no_se_envia_token(self, client):
        response = client.post(URL_CREATE_PRODUCTS)
        assert response.status_code == 401
        assert "No se proporciono un token" in response.json["message"]

    def test_deberia_devolver_401_si_el_token_esta_mal_formado(self, client):
        response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": "Bearer"})
        assert response.status_code == 401
        assert "Formato del token invalido" in response.json["message"]

    def test_deberia_devolver_403_si_el_token_es_invalido(self, client):
        response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": "Bearer token_falso"})
        assert response.status_code == 403
        assert "Token invalido" in response.json["message"]

    def test_deberia_devolver_403_si_el_token_es_valido_pero_el_rol_no_tiene_permisos(self, client):
        token = generar_token_con_rol("bodeguero")
        response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
        assert "Permisos insuficientes" in response.json["message"]

    def test_deberia_devolver_403_si_el_token_esta_expirado(self, client):
        expirado = datetime.now(tz=timezone.utc) - timedelta(seconds=10)
        token = generar_token_con_rol("director-compras", expirado)
        response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
        assert "Token expirado" in response.json["message"]


class TestCrearProductoExitoso:

    def test_deberia_registrar_producto_exitosamente_con_token_valido(self, client):
        token = generar_token_con_rol("director-compras")
        payload = [{
            "nombre": "Producto Uno",
            "descripcion": "Descripción del producto",
            "tiempo_entrega": "2 días",
            "precio": 100.0,
            "condiciones_almacenamiento": "Lugar fresco y seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 50,
            "imagenes_productos": ["img1.jpg", "img2.jpg"],
            "proveedor": "Proveedor Uno S.A."
        }]
        response = client.post(
            URL_CREATE_PRODUCTS,
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert "registrado" in response.json["message"]


class TestCrearProductoErroresInternos:

    def test_deberia_devolver_500_si_el_validador_lanza_excepcion(self, client):
        with patch(
            "aplicacion.escrituras.crear_producto.AccessTokenValidator.validate",
            side_effect=Exception("Falla interna")
        ):
            token = generar_token_con_rol("director-compras")
            response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 500
            assert "Error en registro. Intentre mas tarde." in response.json["message"]

    def test_deberia_devolver_400_si_no_se_envia_cuerpo_json(self, client):
        token = generar_token_con_rol("director-compras")
        response = client.post(URL_CREATE_PRODUCTS, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400
        assert "Se requiere un cuerpo con formato JSON" in response.json["message"]

    def test_deberia_devolver_403_si_falta_campo_requerido(self, client):
        token = generar_token_con_rol("director-compras")
        producto_invalido = [{
            # Falta 'nombre'
            "descripcion": "Producto sin nombre",
            "tiempo_entrega": "2 días",
            "precio": 100.0,
            "condiciones_almacenamiento": "Lugar seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 50,
            "imagenes_productos": ["img1.jpg"],
            "proveedor": "Proveedor Uno"
        }]
        response = client.post(URL_CREATE_PRODUCTS, json=producto_invalido,
                               headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
        assert "nombre" in response.json["message"]

    def test_deberia_devolver_413_si_se_excede_limite_productos(self, client):
        token = generar_token_con_rol("director-compras")
        productos = [{
            "nombre": f"Producto {i}",
            "descripcion": "Desc",
            "tiempo_entrega": "2 días",
            "precio": 100.0,
            "condiciones_almacenamiento": "Seco",
            "fecha_vencimiento": "2025-12-31",
            "estado": "en_stock",
            "inventario_inicial": 50,
            "imagenes_productos": ["img.jpg"],
            "proveedor": "Proveedor"
        } for i in range(101)]  # 101 productos

        response = client.post(URL_CREATE_PRODUCTS, json=productos,
                               headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
        assert "exceder 100 productos" in response.json["message"]

