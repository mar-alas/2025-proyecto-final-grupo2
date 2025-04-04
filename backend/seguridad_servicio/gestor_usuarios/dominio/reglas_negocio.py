import re

def validar_campos_requeridos(data):
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if field not in data:
                return f"El campo {field} es requerido."
    return None


def validar_formato_email(email):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(patron, email):
        return None
    else:
        return "Formato de correo invalido."
    

def validar_tamanio_name(name):
    MAX_LENGHT = 250
    
    if len(name) > MAX_LENGHT:
         return "Campo name es muy largo."
    return None


def validar_role(data):
    valid_roles = ['user', 'admin', 'cliente', 'vendedor', 'proveedor']
    role = data.get('role')
    return role in valid_roles

def role_esta_presente(data):
    return bool(data.get('role'))

def country_esta_presente(data):
    return bool(data.get('country'))


def city_esta_presente(data):
    return bool(data.get('city'))


def address_esta_presente(data):
    return bool(data.get('address'))

def validar_datos_usuario(data):
    """Valida los datos de un usuario antes de registrarlo."""
    
    validation_result = validar_campos_requeridos(data)
    if validation_result:
        return validation_result

    validation_result = validar_formato_email(data.get('email'))
    if validation_result:
        return validation_result

    validation_result = validar_tamanio_name(data.get('name'))
    if validation_result:
        return validation_result

    return None 