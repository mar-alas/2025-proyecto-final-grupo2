import pulsar
import json
import logging

from infraestructura.config import Config
from dominio.event_publisher import EventPublisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PulsarPublisher(EventPublisher):
    def __init__(self):
        self.config = Config.PULSAR_CONFIG
        self.cliente = pulsar.Client(self.config["pulsar_url"])


    def publicar_mensaje(self, topico, mensaje):
        """Publica un mensaje en el tópico especificado."""
        try:
            productor = self.cliente.create_producer(topico)
            productor.send(json.dumps(mensaje).encode("utf-8"))
            logger.info(f"Mensaje publicado en {topico}: {mensaje}")
            self.cliente.close()
        except Exception as e:
            logger.info(f"Error enviando mensaje a {topico}: {str(e)}")