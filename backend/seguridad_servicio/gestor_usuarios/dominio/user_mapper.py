from gestor_usuarios.dominio.user_dto import UserDTO

class UserMapper:

    @staticmethod
    def to_model_v2(user_dto: UserDTO):
        """Retorna un diccionario en lugar de una instancia del modelo de base de datos."""
        return {
            "name": user_dto.name,
            "email": user_dto.email,
            "password": user_dto.password,
            "role": user_dto.role,
            "country": user_dto.country,
            "city": user_dto.city,
            "address": user_dto.address,
        }
    
    @staticmethod
    def to_dto(model_instance) -> UserDTO:
        """Convierte una instancia del modelo a un UserDTO."""
        return UserDTO(
            id=model_instance.id,
            name=model_instance.name,
            email=model_instance.email,
            password=model_instance.password,
            role=model_instance.role,
            country=model_instance.country,
            city=model_instance.city,
            address=model_instance.address,
        )