import pytest
from gestor_usuarios.dominio.user import User
from gestor_usuarios.infraestructura.database import db
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

def test_crear_usuario(session):
    usuario = User(
        name="Jhon Doe",
        email="jhon@example.com",
        password="hashedpass123",
        role="admin",
        country="Colombia",
        city="Bogotá",
        address="Calle falsa 123",
        client_type="premium",
        geographic_coordinates="4.60971,-74.08175"
    )

    session.add(usuario)
    session.commit()

    usuario_en_db = session.query(User).filter_by(email="jhon@example.com").first()

    assert usuario_en_db is not None
    assert usuario_en_db.name == "Jhon Doe"
    assert usuario_en_db.email == "jhon@example.com"
    assert usuario_en_db.role == "admin"
    assert usuario_en_db.country == "Colombia"
    assert usuario_en_db.city == "Bogotá"
    assert usuario_en_db.address == "Calle falsa 123"
    assert usuario_en_db.client_type == "premium"
    assert usuario_en_db.geographic_coordinates == "4.60971,-74.08175"
    assert usuario_en_db.uuid is not None
    assert isinstance(usuario_en_db.uuid, str)
