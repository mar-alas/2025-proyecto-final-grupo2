import os

def obtener_config_pulsar():
    """
    Obtiene la configuración de Apache Pulsar desde variables de entorno o usa valores por defecto.
    """
    host = os.getenv('PULSAR_HOST', default="localhost")
    return {
        "pulsar_url": f"pulsar://{host}:6650"
    }
