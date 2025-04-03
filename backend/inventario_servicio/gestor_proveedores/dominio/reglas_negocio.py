def validar_datos_no_vacios(data, campos_requeridos=None):
    """
    Valida que los datos no estén vacíos y que los campos requeridos estén presentes y no sean vacíos.

    Args:
        data (dict): Diccionario con los datos a validar.
        campos_requeridos (list): Lista de campos requeridos. Si es None, se validan todos los campos del diccionario.

    Returns:
        dict: Diccionario con los errores encontrados. Si no hay errores, retorna un diccionario vacío.
    """
    errores = {}

    if not data:
        return {"error": "Los datos no pueden estar vacíos."}

    if campos_requeridos is None:
        campos_requeridos = data.keys()

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            errores[campo] = f"El campo '{campo}' es obligatorio y no puede estar vacío."

    return errores