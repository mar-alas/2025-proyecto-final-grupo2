from dominio.plan_venta_domain import DomainPlanVenta

def convertir_json_a_entidades_de_dominio(vendedor_id, metas):
    entidades_de_dominio = []

    for fecha_str, valor in metas.items(): 
        domain_plan = DomainPlanVenta(
            vendedor_id=vendedor_id,
            fecha=fecha_str, 
            valor=float(valor)
        )
        entidades_de_dominio.append(domain_plan)

    return entidades_de_dominio
