from infraestructura.modelos import Pedido as InfraPedido, ProductoPedido as InfraProductoPedido
from dominio.modelo import Pedido

def to_infraestructura_pedido(domain_pedido):
    """Convert a domain Pedido to an infraestructura Pedido."""
    infra_pedido = InfraPedido(
        cliente_id=domain_pedido.cliente_id,
        vendedor_id=domain_pedido.vendedor_id,
        estado=domain_pedido.estado,
        subtotal=domain_pedido.subtotal,
        total=domain_pedido.total,
        productos=[
            InfraProductoPedido(
                producto_id=p["id"],
                cantidad=p["cantidad"],
                precio_unitario=p["precio_unitario"],
                subtotal=p["cantidad"] * p["precio_unitario"]
            )
            for p in domain_pedido.productos
        ]
    )
    return infra_pedido

def to_domain_pedido(infra_pedido):
    """Convert an infraestructura Pedido to a domain Pedido."""
    domain_pedido = Pedido(
        cliente_id=infra_pedido.cliente_id,
        vendedor_id=infra_pedido.vendedor_id,
        productos=[
            {
                "id": p.producto_id,
                "cantidad": p.cantidad,
                "precio_unitario": p.precio_unitario
            }
            for p in infra_pedido.productos
        ],
        estado=infra_pedido.estado
    )
    return domain_pedido