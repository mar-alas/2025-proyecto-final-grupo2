from infraestructura.modelos import VisitaCliente as InfraVisitaCliente

def to_infraestructura_visita(domain_visita):
    """Convert a domain VisitaCliente to an infraestructura VisitaCliente."""
    return InfraVisitaCliente(
        cliente_id=domain_visita.cliente_id,
        vendedor_id=domain_visita.vendedor_id,
        fecha=domain_visita.fecha,
        ubicacion_productos_ccp=domain_visita.ubicacion_productos_ccp,
        ubicacion_productos_competencia=domain_visita.ubicacion_productos_competencia
    )