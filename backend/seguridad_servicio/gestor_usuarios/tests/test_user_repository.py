from unittest.mock import MagicMock
import pytest
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.dominio.user_dto import UserDTO


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
