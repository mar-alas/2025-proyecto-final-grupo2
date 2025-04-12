def _validar_campos_requeridos_producto(producto):
    campos_requeridos = [
        'nombre',
        'descripcion',
        'tiempo_entrega',
        'precio',
        'condiciones_almacenamiento',
        'fecha_vencimiento',
        'estado',
        'inventario_inicial',
        'imagenes_productos',
        'proveedor'
    ]
    for campo in campos_requeridos:
        if campo not in producto or producto[campo] in (None, '', []):
            return f"El campo '{campo}' es requerido y no puede estar vacio."
    return None


def _validar_limite_productos(data):
    if len(data) > 100:
        return  f"El registro masivo no puede exceder 100 productos por solicitud"
    return None


def validar_datos_producto(data):
    if not isinstance(data, list):
        return "Se esperaba una lista de productos."

    limit_validation = _validar_limite_productos(data)
    if limit_validation:
        return limit_validation

    for i, producto in enumerate(data):
        error = _validar_campos_requeridos_producto(producto)
        if error:
            return f"Error en el producto #{i+1}: {error}"

    return None