from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion

class ReglaAltaDemanda(ReglaRecomendacion):
    productos_alta_rotacion = {"Cerveza", "Pan", "Leche"}

    def aplicar(self, producto: ProductoDetectadoVideo):
        if producto.nombre in self.productos_alta_rotacion:
            return [{
                "titulo_recomendacion": "Alta rotación detectada",
                "cuerpo_recomendacion": f"{producto.nombre} suele agotarse. Considere comprar una presentación grande."
            }]
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        if producto.nombre in self.productos_alta_rotacion:
            return [{
                "id": hash(producto.nombre) % 100000,
                "cantidad": 24,
                "precio_unitario": 12000
            }]
        return []
