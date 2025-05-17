from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion
from dominio.reglas_recomendacion_fallback import ReglaFallbackRecomendacion


class ProcesadorVideo:
    def __init__(self, reglas: list[ReglaRecomendacion], productos_disponibles: list = None):
        self.reglas = reglas
        self.fallback = ReglaFallbackRecomendacion(productos_disponibles)


    def procesar(self, cliente_id: int, info_video: list[dict]) -> dict:
        recomendaciones = []
        productos = []

        """ Flujo normal """
        for item in info_video:
            producto = ProductoDetectadoVideo(
                nombre = item.get("nombre_producto"),
                ubicacion = item.get("ubicacion"),
                cantidad = item.get("cantidad", 0)
            )

            for regla in self.reglas:
                recomendaciones.extend(regla.aplicar(producto))
                productos.extend(regla.sugerencias_pedido(producto))

        """ Fallback """
        recomendacion_fallback, productos_fallback = self.fallback.sugerencias_genericas_fallback()

        if recomendaciones is None or recomendaciones == []:
            recomendaciones.extend(recomendacion_fallback)

        if productos is None or productos == []:
            productos.extend(productos_fallback)
            

        return {
            "mensaje": "Procesamiento fue exitoso",
            "recomendaciones": recomendaciones,
            "recomendacion_pedido": {
                "cliente_id": cliente_id,
                "productos": productos
            }
        }
