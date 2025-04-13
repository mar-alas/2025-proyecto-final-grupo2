import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'inventario_servicio_db')}:"
        f"{os.getenv('DB_PORT', 5432)}/"
        f"{os.getenv('DB_NAME', 'inventario_servicio_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PULSAR_CONFIG =  { 
        "pulsar_url": f"pulsar://{os.getenv('PULSAR_HOST', default='localhost')}:6650"
    }