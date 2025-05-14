import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_bajo_stock import ReglaStockBajo

class ProductoMock:
    def __init__(self, nombre, id=1, inventario_inicial=20, precio=10000):
        self.nombre = nombre
        self.id = id
        self.inventario_inicial = inventario_inicial
        self.precio = precio

def test_sugerencias_pedido_cantidad_baja():
    productos_disponibles = [
        ProductoMock(nombre="Jabon", id=101, inventario_inicial=20, precio=10000)
    ]
    regla = ReglaStockBajo(productos_disponibles=productos_disponibles)

    producto = ProductoDetectadoVideo(nombre="Jabon", ubicacion="Pasillo 7", cantidad=2)
    resultado = regla.sugerencias_pedido(producto)

    assert len(resultado) == 1
    assert resultado[0]["cantidad"] == 20
    assert resultado[0]["precio_unitario"] == 10000
    assert resultado[0]["id"] == 101
