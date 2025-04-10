import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gestor_usuarios.infraestructura.database.__init__ import db, init_db

@pytest.fixture
def app():
    """Crea una aplicación Flask de prueba con configuración de base de datos en memoria."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app

def test_init_db(app):
    """Prueba que init_db inicializa correctamente la base de datos."""
    with app.app_context():
        init_db(app)  # Llama a la función que inicializa la DB

        # Verifica que db esté vinculado a la app y tenga una conexión activa
        assert db.engine is not None
        assert db.session is not None
