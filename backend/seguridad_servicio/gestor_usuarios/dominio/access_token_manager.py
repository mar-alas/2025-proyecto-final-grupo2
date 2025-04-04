import jwt
import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

# Clave secreta para firmar los tokens
SECRET_KEY = 'clave_secreta_para_firmar_token'

# Función para generar un token JWT
def generar_token(payload, expiracion_minutos=2880):
    """
    Genera un token JWT con el payload y un tiempo de expiración.
    
    :param payload: Diccionario con los datos que se incluirán en el token.
    :param expiracion_minutos: Tiempo de expiración del token en minutos.
    :return: Token JWT como string.
    """
    expiracion = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiracion_minutos)
    payload['exp'] = expiracion
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Función para validar un token JWT
def validar_token(token):
    """
    Valida un token JWT.
    
    :param token: El token JWT a validar.
    :return: True si el token es válido, False si es inválido o ha expirado.
    """
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except ExpiredSignatureError:
        return False
    except InvalidTokenError:
        return False
