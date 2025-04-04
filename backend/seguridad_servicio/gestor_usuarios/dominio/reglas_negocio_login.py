import re

def validar_data_presente(data):
    if data is None:
         return "Se requiere una solictud con payload/body."
    return None


def validar_campos_requeridos(data):
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data:
                return f"El campo {field} es requerido."
    return None


def validar_formato_email(email):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(patron, email):
        return None
    else:
        return "Formato de email invalido."
    

def validar_tamanio_email(email):
    MAX_LENGHT = 250
    
    if len(email) > MAX_LENGHT:
         return "Campo email es muy largo."
    return None


def validar_tamanio_password(password):
    MAX_LENGHT = 250
    
    if len(password) > MAX_LENGHT:
         return "Campo password es muy largo."
    return None


@staticmethod
def validar_login_data(data):
    validation_result = validar_data_presente(data)
    if validation_result:
        return validation_result

    validation_result = validar_campos_requeridos(data)
    if validation_result:
        return validation_result

    email = data.get('email')
    validation_result = validar_formato_email(email)
    if validation_result:
        return validation_result

    validation_result = validar_tamanio_email(email)
    if validation_result:
        return validation_result

    password = data.get('password')
    validation_result = validar_tamanio_password(password)
    if validation_result:
        return validation_result

    return None