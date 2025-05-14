from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion
import random

class ReglaAltaDemanda(ReglaRecomendacion):

    def __init__(self, productos_disponibles=None):
        self.productos_disponibles = productos_disponibles
        self.productos_alta_rotacion = self.elegir_productos_aleatorios(3)

    def elegir_productos_aleatorios(self, cantidad=3):
        if len(self.productos_disponibles) < cantidad:
            return []
        return random.sample(self.productos_disponibles, cantidad)

    def aplicar(self, producto: ProductoDetectadoVideo):
        # if producto.nombre in self.productos_alta_rotacion:
        if any(p.nombre.strip().lower() == producto.nombre.strip().lower() for p in self.productos_alta_rotacion):
            return [{
                "titulo_recomendacion": "Alta rotacion detectada",
                "cuerpo_recomendacion": f"{producto.nombre} suele agotarse. Considere comprar una presentacion grande."
            }]
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        if producto.nombre in self.productos_alta_rotacion:
            producto_encontrado = next((p for p in self.productos_disponibles  if p.nombre.strip().lower() == producto.nombre.strip().lower()), None)
            if producto_encontrado is None:
                return []
            
            return [{
                "id": producto_encontrado.id,
                "cantidad": producto_encontrado.inventario_inicial,
                "precio_unitario": producto_encontrado.precio
            }]
        
        return []
    
