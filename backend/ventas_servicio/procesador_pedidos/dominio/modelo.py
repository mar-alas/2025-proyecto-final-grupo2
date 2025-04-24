from datetime import datetime

class Pedido:
    def __init__(self, cliente_id, vendedor_id, productos, estado="pendiente"):
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        self.productos = productos
        self.estado = estado
        self.subtotal = sum(p["cantidad"] * p["precio_unitario"] for p in productos)
        self.total = self.subtotal