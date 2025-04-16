class ProductoCreado:
    def __init__(self, producto_id, inventario_inicial):
        self.producto_id = producto_id
        self.inventario_inicial = inventario_inicial

    def to_dict(self):
        return {
            "producto_id": self.producto_id,
            "inventario_inicial": self.inventario_inicial
        }
