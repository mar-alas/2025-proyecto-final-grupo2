import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_ubicacion_producto import ReglaPorUbicacion


@pytest.fixture
def regla_ubicacion():
    return ReglaPorUbicacion()

def test_aplicar_con_ubicacion_valida(regla_ubicacion):
    producto = ProductoDetectadoVideo(nombre="Arroz", ubicacion="Pasillo 3", cantidad=5)
    resultado = regla_ubicacion.aplicar(producto)
    
    assert len(resultado) == 1
    assert resultado[0]["titulo_recomendacion"] == "Producto complementario"
    assert "Lentejas" in resultado[0]["cuerpo_recomendacion"]
    assert "Fríjoles" in resultado[0]["cuerpo_recomendacion"]

def test_aplicar_con_ubicacion_invalida(regla_ubicacion):
    producto = ProductoDetectadoVideo(nombre="Cereal", ubicacion="Pasillo X", cantidad=2)
    resultado = regla_ubicacion.aplicar(producto)
    
    assert resultado == []

def test_sugerencias_pedido_siempres_vacio(regla_ubicacion):
    producto = ProductoDetectadoVideo(nombre="Aceite", ubicacion="Pasillo 2", cantidad=3)
    resultado = regla_ubicacion.sugerencias_pedido(producto)
    
    assert resultado == []
