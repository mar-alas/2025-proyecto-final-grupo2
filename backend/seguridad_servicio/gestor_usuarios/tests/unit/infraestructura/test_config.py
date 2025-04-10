import os
import pytest
from gestor_usuarios.infraestructura.config import Config

@pytest.fixture
def reset_env():
    """Fixture para limpiar variables de entorno antes de cada test."""
    original_env = os.environ.copy()
    os.environ.clear()
    yield
    os.environ.clear()
    os.environ.update(original_env)

def test_default_values(reset_env):
    """Prueba que la configuración usa los valores por defecto."""
    config = Config()
    expected_uri = "postgresql://postgres:postgres@seguridad-servicio-db:5432/seguridad_servicio_db"
    assert config.SQLALCHEMY_DATABASE_URI == expected_uri

def test_custom_values(reset_env):
    """Prueba que la configuración usa las variables de entorno personalizadas."""
    os.environ.update({
        "DB_USER": "postgresql",
        "DB_PASSWORD": "postgres",
        "DB_HOST": "seguridad-servicio-db",
        "DB_PORT": "5432",
        "DB_NAME": "seguridad_servicio_db"
    })

    config = Config()
    expected_uri = "postgresql://postgres:postgres@seguridad-servicio-db:5432/seguridad_servicio_db"
    assert config.SQLALCHEMY_DATABASE_URI == expected_uri
