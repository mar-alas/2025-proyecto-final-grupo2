from dominio.user_dto import UserDTO
from werkzeug.security import generate_password_hash
from dominio.user import User


class UserMapper:
    """Convierte UserDTO en un modelo de base de datos"""
    
    @staticmethod
    def to_model(user_dto: UserDTO):
        return User(
            name=user_dto.name,
            email=user_dto.email,
            password=generate_password_hash(user_dto.password),
            role=user_dto.role,
            country=user_dto.country,
            city=user_dto.city,
            address=user_dto.address
        )
