from dominio.product_mapper import crear_product_dto_desde_dict
from dominio.reglas_negocio_crear_producto import validar_datos_producto

class CrearProductoService:
    def __init__(self, repositorio_productos, event_publisher=None):
        self.repositorio = repositorio_productos
        self.event_publisher = event_publisher

    def crear(self, productos_input):
        productos = productos_input if isinstance(productos_input, list) else [productos_input]
        productos = productos[:100] 

        resultados = []
        exitosos = 0

        for idx, producto in enumerate(productos):
            mensaje_validacion = validar_datos_producto(producto)
            if mensaje_validacion:
                resultados.append({
                    "indice": idx,
                    "status": "error",
                    "producto": producto,
                    "error": mensaje_validacion
                })
                continue

            if self.repositorio.get_by_name(producto.get("nombre")):
                resultados.append({
                    "indice": idx,
                    "status": "error",
                    "producto": producto,
                    "error": f"El producto '{producto.get('nombre')}' ya esta registrado"
                })
                continue

            dto = crear_product_dto_desde_dict(producto)
            creado = self.repositorio.save(dto)

            resultados.append({
                "indice": idx,
                "status": "success",
                "producto": creado.to_dict()
            })
            exitosos += 1

            if self.event_publisher:
                evento = {
                    "evento": "ProductoRegistrado",
                    "producto": creado.to_dict()
                }
                self.event_publisher.publicar_mensaje("productos", evento)

        return {
            "total": len(productos),
            "exitosos": exitosos,
            "fallidos": len(productos) - exitosos,
            "resultados": resultados
        }
