import random
from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion

class ReglaFallbackRecomendacion(ReglaRecomendacion):

    def __init__(self, productos_disponibles=None):
        self.productos_disponibles = productos_disponibles or []

    def aplicar(self, producto: ProductoDetectadoVideo) -> list[dict]:
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo) -> list[dict]:
        return []

    def sugerencias_genericas_fallback(self) -> tuple[list[dict], list[dict]]:
        if not self.productos_disponibles:
            return [], []

        producto_sugerido = random.choice(self.productos_disponibles)

        recomendacion = [{
            "titulo_recomendacion": "Producto Sugerido",
            "cuerpo_recomendacion": f"Considere adquirir {producto_sugerido.nombre}, es un producto destacado en nuestro catalogo."
        }]

        pedido = [{
            "id": producto_sugerido.id,
            "cantidad": producto_sugerido.inventario_inicial,
            "precio_unitario": producto_sugerido.precio
        }]

        return recomendacion, pedido
