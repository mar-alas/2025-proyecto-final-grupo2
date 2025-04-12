from datetime import datetime
from dateutil.parser import parse

class VisitaCliente:
    def __init__(self, cliente_id, vendedor_id, fecha, ubicacion_productos_ccp, ubicacion_productos_competencia):
        self.cliente_id = cliente_id
        self.vendedor_id = vendedor_id
        try:
            self.fecha = parse(fecha)  # Use dateutil to parse ISO 8601 strings
        except ValueError as e:
            raise ValueError(f"Formato de fecha inválido: {fecha}. Error: {e}")
        self.ubicacion_productos_ccp = ubicacion_productos_ccp
        self.ubicacion_productos_competencia = ubicacion_productos_competencia