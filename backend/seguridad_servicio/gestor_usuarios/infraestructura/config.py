import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'seguridad-servicio-db')}:"
        f"{os.getenv('DB_PORT', 5432)}/"
        f"{os.getenv('DB_NAME', 'seguridad_servicio_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False