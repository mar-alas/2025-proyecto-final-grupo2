import pytest
from gestor_usuarios.dominio.user_dto import UserDTO 

def test_user_dto():
    """Prueba la creación de UserDTO con los datos correctos."""
    user_dto = UserDTO(name="John Doe", email="john@example.com", password="securepassword")

    assert user_dto.name == "John Doe"
    assert user_dto.email == "john@example.com"
    assert user_dto.password == "securepassword"
    assert user_dto.role is None  # Opcional
    assert user_dto.country is None  # Opcional
