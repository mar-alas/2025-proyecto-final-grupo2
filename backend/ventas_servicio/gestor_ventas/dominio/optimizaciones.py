def optimizar_ruta(visitas):
    """
    Optimizar la ruta de visitas
    Por ahora se ordena por tiempo estimado
    """
    # Sort visits by estimated time
    visitas.sort(key=lambda x: x.distancia)
    return visitas
