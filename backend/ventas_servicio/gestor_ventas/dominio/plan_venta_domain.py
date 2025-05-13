from dataclasses import dataclass
from datetime import date

@dataclass
class DomainPlanVenta:
    vendedor_id: int
    fecha: str
    valor: float
