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


def _validar_campo_imagenes_como_lista(data):
    if not isinstance(data.get("imagenes_productos", []), list):
        return "El campo 'imagenes_productos' debe ser una lista."
    return None

def validar_datos_producto(producto):
    error = _validar_campos_requeridos_producto(producto)
    if error:
        return error

    tipo_dato_imagenes_validation = _validar_campo_imagenes_como_lista(producto)
    if tipo_dato_imagenes_validation:
        return tipo_dato_imagenes_validation

    return None
