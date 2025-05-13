from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion

class ProcesadorVideo:
    def __init__(self, reglas: list[ReglaRecomendacion]):
        self.reglas = reglas

    def procesar(self, cliente_id: int, info_video: list[dict]) -> dict:
        recomendaciones = []
        productos = []

        for item in info_video:
            producto = ProductoDetectadoVideo(
                nombre = item.get("nombre_producto"),
                ubicacion = item.get("ubicacion"),
                cantidad = item.get("cantidad", 0)
            )

            for regla in self.reglas:
                recomendaciones.extend(regla.aplicar(producto))
                productos.extend(regla.sugerencias_pedido(producto))

        return {
            "mensaje": "Procesamiento fue exitoso",
            "recomendaciones": recomendaciones,
            "recomendacion_pedido": {
                "cliente_id": cliente_id,
                "productos": productos
            }
        }
