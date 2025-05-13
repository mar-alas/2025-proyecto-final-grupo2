import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_bajo_stock import ReglaStockBajo

@pytest.fixture
def regla_stock_bajo():
    return ReglaStockBajo()

def test_aplicar_cantidad_baja(regla_stock_bajo):
    producto = ProductoDetectadoVideo(nombre="Papel Higiénico", ubicacion="Pasillo 5", cantidad=3)
    resultado = regla_stock_bajo.aplicar(producto)

    assert len(resultado) == 1
    assert resultado[0]["titulo_recomendacion"] == "Reabastecer producto"
    assert "Papel Higiénico" in resultado[0]["cuerpo_recomendacion"]

def test_aplicar_cantidad_alta(regla_stock_bajo):
    producto = ProductoDetectadoVideo(nombre="Detergente", ubicacion="Pasillo 6", cantidad=10)
    resultado = regla_stock_bajo.aplicar(producto)

    assert resultado == []

def test_sugerencias_pedido_cantidad_baja(regla_stock_bajo):
    producto = ProductoDetectadoVideo(nombre="Jabón", ubicacion="Pasillo 7", cantidad=2)
    resultado = regla_stock_bajo.sugerencias_pedido(producto)

    assert len(resultado) == 1
    assert resultado[0]["cantidad"] == 20
    assert resultado[0]["precio_unitario"] == 10000
    assert isinstance(resultado[0]["id"], int)

def test_sugerencias_pedido_cantidad_alta(regla_stock_bajo):
    producto = ProductoDetectadoVideo(nombre="Shampoo", ubicacion="Pasillo 8", cantidad=15)
    resultado = regla_stock_bajo.sugerencias_pedido(producto)

    assert resultado == []
