import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_alta_demanda import ReglaAltaDemanda

@pytest.fixture
def regla_alta_demanda():
    return ReglaAltaDemanda()

def test_aplicar_producto_alta_demanda(regla_alta_demanda):
    producto = ProductoDetectadoVideo(nombre="Cerveza", ubicacion="Pasillo 9", cantidad=8)
    resultado = regla_alta_demanda.aplicar(producto)

    assert len(resultado) == 1
    assert resultado[0]["titulo_recomendacion"] == "Alta rotación detectada"
    assert "Cerveza" in resultado[0]["cuerpo_recomendacion"]

def test_aplicar_producto_normal(regla_alta_demanda):
    producto = ProductoDetectadoVideo(nombre="Galletas", ubicacion="Pasillo 10", cantidad=8)
    resultado = regla_alta_demanda.aplicar(producto)

    assert resultado == []

def test_sugerencias_pedido_producto_alta_demanda(regla_alta_demanda):
    producto = ProductoDetectadoVideo(nombre="Leche", ubicacion="Pasillo 11", cantidad=5)
    resultado = regla_alta_demanda.sugerencias_pedido(producto)

    assert len(resultado) == 1
    assert resultado[0]["cantidad"] == 24
    assert resultado[0]["precio_unitario"] == 12000
    assert isinstance(resultado[0]["id"], int)

def test_sugerencias_pedido_producto_normal(regla_alta_demanda):
    producto = ProductoDetectadoVideo(nombre="Cereal", ubicacion="Pasillo 12", cantidad=5)
    resultado = regla_alta_demanda.sugerencias_pedido(producto)

    assert resultado == []
