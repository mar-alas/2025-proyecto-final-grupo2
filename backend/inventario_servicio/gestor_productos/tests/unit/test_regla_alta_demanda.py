import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_alta_demanda import ReglaAltaDemanda

@pytest.fixture
def productos_disponibles():
    return [
        ProductoDetectadoVideo(nombre="Cerveza", ubicacion="Pasillo 9", cantidad=10),
        ProductoDetectadoVideo(nombre="Leche", ubicacion="Pasillo 11", cantidad=5),
        ProductoDetectadoVideo(nombre="Pan", ubicacion="Pasillo 5", cantidad=15),
        ProductoDetectadoVideo(nombre="Galletas", ubicacion="Pasillo 10", cantidad=8),
        ProductoDetectadoVideo(nombre="Jabón", ubicacion="Pasillo 7", cantidad=2)
    ]

@pytest.fixture
def regla_alta_demanda(productos_disponibles):
    return ReglaAltaDemanda(productos_disponibles=productos_disponibles)

def test_aplicar_producto_alta_demanda():
    productos = [
        ProductoDetectadoVideo(nombre="Leche", ubicacion="Pasillo 11", cantidad=5),
        ProductoDetectadoVideo(nombre="Pan", ubicacion="Pasillo 5", cantidad=10),
        ProductoDetectadoVideo(nombre="Jugo", ubicacion="Pasillo 2", cantidad=8),
    ]
    regla = ReglaAltaDemanda(productos_disponibles=productos)
    regla.productos_alta_rotacion = productos  # Forzamos los productos como de alta rotación

    producto = ProductoDetectadoVideo(nombre="Leche", ubicacion="Pasillo 11", cantidad=5)
    resultado = regla.aplicar(producto)

    assert len(resultado) == 1
    assert "Leche suele agotarse" in resultado[0]["cuerpo_recomendacion"]


