import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


class AccessTokenValidator:
    def __init__(self, secret_key='clave_secreta_para_firmar_token', algorithms=None, required_role='director-compras'):
        self.secret_key = secret_key
        self.algorithms = algorithms or ['HS256']
        self.required_role = required_role

    def validate(self, token: str):
        """
        Valida el token y el rol.
        
        :param token: JWT string
        :return: Tuple (es_valido: bool, mensaje: str)
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithms)
            role = payload.get("role")
            if role != self.required_role:
                return False, "Permisos insuficientes"
            return True, "Token valido"
        except ExpiredSignatureError:
            return False, "Token expirado"
        except InvalidTokenError:
            return False, "Token invalido"
