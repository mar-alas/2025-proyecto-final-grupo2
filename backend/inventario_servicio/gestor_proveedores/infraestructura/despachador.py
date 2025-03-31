from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DespachadorProveedores:
    def __init__(self, topico_eventos):
        self.conexion = ConexionPulsar()
        self.topico_eventos = topico_eventos

    def publicar_evento(self, evento):
        try:
            self.conexion.publicar_mensaje(self.topico_eventos, evento)
            logger.info(f"Evento publicado exitosamente en el tópico {self.topico_eventos}: {evento}")
        except Exception as e:
            logger.info(f"Error al publicar el evento en el tópico {self.topico_eventos}: {e}")