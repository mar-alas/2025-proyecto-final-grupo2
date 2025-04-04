import pulsar
import json
from seedwork_compartido.infraestructura.config_broker import obtener_config_pulsar
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConexionPulsar:
    def __init__(self):
        self.config = obtener_config_pulsar()
        self.cliente = pulsar.Client(self.config["pulsar_url"])


    def publicar_mensaje(self, topico, mensaje):
        """Publica un mensaje en el tópico especificado."""
        try:
            productor = self.cliente.create_producer(topico)
            productor.send(json.dumps(mensaje).encode("utf-8"))
            logger.info(f"Mensaje publicado en {topico}: {mensaje}")
        except Exception as e:
            logger.info(f"Error enviando mensaje a {topico}: {str(e)}")

    def cerrar(self):
        """Cierra la conexión con Pulsar."""
        self.cliente.close()
