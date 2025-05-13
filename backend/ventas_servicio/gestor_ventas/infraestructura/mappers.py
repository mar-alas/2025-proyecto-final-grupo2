from infraestructura.modelos import VisitaCliente as InfraVisitaCliente
from infraestructura.modelos import PlanVentaVendedor

def to_infraestructura_visita(domain_visita):
    """Convert a domain VisitaCliente to an infraestructura VisitaCliente."""
    return InfraVisitaCliente(
        cliente_id=domain_visita.cliente_id,
        vendedor_id=domain_visita.vendedor_id,
        fecha=domain_visita.fecha,
        ubicacion_productos_ccp=domain_visita.ubicacion_productos_ccp,
        ubicacion_productos_competencia=domain_visita.ubicacion_productos_competencia
    )

def to_plan_venta_entity(domain_plan_venta):
    return PlanVentaVendedor(
        vendedor_id=domain_plan_venta.vendedor_id,
        fecha=domain_plan_venta.fecha,
        valor=domain_plan_venta.valor
    )
