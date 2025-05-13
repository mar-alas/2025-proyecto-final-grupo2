import pytest
from types import SimpleNamespace
from gestor_usuarios.dominio.user_dto import UserDTO
from gestor_usuarios.dominio.user_mapper import UserMapper

def test_user_mapper_to_model_v2():
    user_dto = UserDTO(
        id=1,
        name="Alice",
        email="alice@example.com",
        password="securepass",
        role="cliente",
        country="Colombia",
        city="Bogotá",
        address="Calle 123",
        client_type="premium",
        geographic_coordinates="4.60971,-74.08175"
    )

    model_data = UserMapper.to_model_v2(user_dto)

    assert model_data == {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "securepass",
        "role": "cliente",
        "country": "Colombia",
        "city": "Bogotá",
        "address": "Calle 123",
        "client_type": "premium",
        "geographic_coordinates": "4.60971,-74.08175"
    }

def test_user_mapper_to_dto():
    # Simula una instancia de modelo usando SimpleNamespace
    model_instance = SimpleNamespace(
        id=1,
        name="Bob",
        email="bob@example.com",
        password="12345",
        role="cliente",
        country="Perú",
        city="Lima",
        address="Av. Siempre Viva",
        client_type="regular",
        geographic_coordinates="-12.0464,-77.0428"
    )

    user_dto = UserMapper.to_dto(model_instance)

    assert isinstance(user_dto, UserDTO)
    assert user_dto.name == "Bob"
    assert user_dto.email == "bob@example.com"
    assert user_dto.password == "12345"
    assert user_dto.role == "cliente"
    assert user_dto.country == "Perú"
    assert user_dto.city == "Lima"
    assert user_dto.address == "Av. Siempre Viva"
    assert user_dto.client_type == "regular"
    assert user_dto.geographic_coordinates == "-12.0464,-77.0428"
