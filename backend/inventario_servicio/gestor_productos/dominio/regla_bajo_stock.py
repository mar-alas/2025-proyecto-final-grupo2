from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion


class ReglaStockBajo(ReglaRecomendacion):
    def aplicar(self, producto: ProductoDetectadoVideo):
        if producto.cantidad <= 5:
            return [{
                "titulo_recomendacion": "Reabastecer producto",
                "cuerpo_recomendacion": f"La cantidad de {producto.nombre} es baja. Recomendamos comprar 20 unidades mas."
            }]
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        if producto.cantidad <= 5:
            return [{
                "id": hash(producto.nombre) % 100000,
                "cantidad": 20,
                "precio_unitario": 10000
            }]
        return []
