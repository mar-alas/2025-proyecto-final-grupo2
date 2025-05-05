import uuid
from gestor_usuarios.infraestructura.database import db

class User(db.Model):
    __tablename__ = "users"

    uuid = db.Column(db.String(36), primary_key=False, default=lambda: str(uuid.uuid4()))
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Se almacenará el hash
    role = db.Column(db.String(50), nullable=True)  # Opcional
    country = db.Column(db.String(100), nullable=True)  # Opcional
    city = db.Column(db.String(100), nullable=True)  # Opcional
    address = db.Column(db.String(255), nullable=True)  # Opcional
    client_type = db.Column(db.String(50), nullable=True)  # Opcional
    geographic_coordinates = db.Column(db.String(100), nullable=True)  # Opcional

    def __init__(self, name, email, password, role=None, country=None, city=None, address=None, client_type=None, geographic_coordinates=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.country = country
        self.city = city
        self.address = address
        self.client_type = client_type
        self.geographic_coordinates = geographic_coordinates
