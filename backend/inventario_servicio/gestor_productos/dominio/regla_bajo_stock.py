from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion


class ReglaStockBajo(ReglaRecomendacion):

    def __init__(self, productos_disponibles=None):
        self.productos_disponibles = productos_disponibles

    def aplicar(self, producto: ProductoDetectadoVideo):
        if producto.cantidad <= 5:
            return [{
                "titulo_recomendacion": "Reabastecer producto",
                "cuerpo_recomendacion": f"La cantidad de {producto.nombre} es baja. Recomendamos comprar {producto.cantidad * 2} unidades mas."
            }]
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        if producto.cantidad <= 5:
            
            producto_encontrado = next((p for p in self.productos_disponibles  if p.nombre.strip().lower() == producto.nombre.strip().lower()), None)
            if producto_encontrado is None:
                return []
            
            return [{
                "id": producto_encontrado.id,
                "cantidad": producto_encontrado.inventario_inicial,
                "precio_unitario": producto_encontrado.precio
            }]
    
        return []
