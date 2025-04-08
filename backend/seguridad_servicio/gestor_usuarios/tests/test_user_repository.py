from unittest.mock import MagicMock
import pytest
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.dominio.user_dto import UserDTO
from types import SimpleNamespace
from gestor_usuarios.dominio.user_mapper import UserMapper


# Un modelo de usuario de mentira que solo guarda los datos como kwargs
class FakeUserModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def user_repo(mock_db):
    return UserRepository(mock_db, user_model_class=FakeUserModel)

def test_save_user_crea_instancia_correcta(user_repo, mock_db):
    user_dto = UserDTO(
        id=1,
        name="Test User",
        email="test@example.com",
        password="1234",
        role=None,
        country=None,
        city=None,
        address=None
    )

    user_repo.save(user_dto)

    # Verifica que se haya llamado a add() con una instancia del modelo inyectado
    args, _ = mock_db.add.call_args
    saved_user = args[0]
    assert isinstance(saved_user, FakeUserModel)
    assert saved_user.name == "Test User"
    assert saved_user.email == "test@example.com"
    mock_db.commit.assert_called_once()


def test_get_by_email_retorna_usuario(user_repo, mock_db):
    fake_user = FakeUserModel(name="Test", email="test@example.com", password="1234")

    # Simular la cadena: query(...).filter_by(...).first()
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.first.return_value = fake_user
    mock_query.filter_by.return_value = mock_filter
    mock_db.query.return_value = mock_query

    result = user_repo.get_by_email("test@example.com")

    mock_db.query.assert_called_once_with(FakeUserModel)
    mock_query.filter_by.assert_called_once_with(email="test@example.com")
    mock_filter.first.assert_called_once()
    assert result.email == "test@example.com"


def test_get_all_customers_retorna_lista_de_dtos(user_repo, mock_db):
    # Crea una lista de usuarios simulados con rol 'cliente'
    fake_users = [
        SimpleNamespace(
            id=1,
            name="Cliente 1",
            email="cliente1@example.com",
            password="123",
            role="cliente",
            country="Colombia",
            city="Bogotá",
            address="Calle 1"
        ),
        SimpleNamespace(
            id=2,
            name="Cliente 2",
            email="cliente2@example.com",
            password="456",
            role="cliente",
            country="México",
            city="CDMX",
            address="Calle 2"
        )
    ]

    # Mock de la cadena: query(...).filter_by(role='cliente').all()
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_filter.all.return_value = fake_users
    mock_query.filter_by.return_value = mock_filter
    mock_db.query.return_value = mock_query

    # Ejecutar
    result = user_repo.get_all_customers()

    # Verificaciones
    mock_db.query.assert_called_once_with(FakeUserModel)
    mock_query.filter_by.assert_called_once_with(role="cliente")
    mock_filter.all.assert_called_once()

    assert len(result) == 2
    assert all(isinstance(dto, type(UserMapper.to_dto(fake_users[0]))) for dto in result)
    assert result[0].email == "cliente1@example.com"
    assert result[1].email == "cliente2@example.com"