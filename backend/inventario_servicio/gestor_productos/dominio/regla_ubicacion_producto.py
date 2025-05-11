from dominio.producto_detectado_video import ProductoDetectadoVideo
from dominio.regla_recomendacion_base_video import ReglaRecomendacion

class ReglaPorUbicacion(ReglaRecomendacion):
    complementarios = {
        "Pasillo 1": ["Sal", "Pimienta"],
        "Pasillo 2": ["Aceite", "Vinagre"],
        "Pasillo 3": ["Lentejas", "Fríjoles"]
    }

    def aplicar(self, producto: ProductoDetectadoVideo):
        if producto.ubicacion in self.complementarios:
            sugerencias = ", ".join(self.complementarios[producto.ubicacion])
            return [{
                "titulo_recomendacion": "Producto complementario",
                "cuerpo_recomendacion": f"Ya que está en {producto.ubicacion}, aproveche para comprar {sugerencias}."
            }]
        return []

    def sugerencias_pedido(self, producto: ProductoDetectadoVideo):
        return []
