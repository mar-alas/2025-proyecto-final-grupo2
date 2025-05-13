import pytest
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion
from infraestructura.video_processor import ProcesadorVideo

class ReglaRecomendacionMock(ReglaRecomendacion):
    def aplicar(self, producto: ProductoDetectadoVideo):
        return [f"Recomendación para {producto.nombre}"]

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        return [{
            "id": 101,
            "cantidad": producto.cantidad + 1,
            "precio_unitario": 1000.0
        }]

def test_procesador_video_procesa_correctamente():
    reglas = [ReglaRecomendacionMock()]
    procesador = ProcesadorVideo(reglas)

    cliente_id = 123
    info_video = [
        {
            "nombre_producto": "Cerveza",
            "ubicacion": "Pasillo 1",
            "cantidad": 5
        },
        {
            "nombre_producto": "Papas",
            "ubicacion": "Pasillo 2",
            "cantidad": 2
        }
    ]

    resultado = procesador.procesar(cliente_id, info_video)

    assert resultado["mensaje"] == "Procesamiento fue exitoso"
    assert len(resultado["recomendaciones"]) == 2
    assert "Recomendación para Cerveza" in resultado["recomendaciones"]
    assert "Recomendación para Papas" in resultado["recomendaciones"]

    productos = resultado["recomendacion_pedido"]["productos"]
    assert len(productos) == 2
    assert productos[0]["cantidad"] == 6
    assert productos[1]["cantidad"] == 3
    assert resultado["recomendacion_pedido"]["cliente_id"] == cliente_id
