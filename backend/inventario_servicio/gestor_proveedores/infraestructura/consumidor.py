from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
from infraestructura.repositorio import RepositorioProveedores
from infraestructura.despachador import DespachadorProveedores
from dominio.modelo import Proveedor
import pulsar
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsumidorProveedores:
    def __init__(self, topico_comandos, topico_eventos, db_session):
        self.conexion = ConexionPulsar()
        self.topico_comandos = topico_comandos
        self.topico_eventos = topico_eventos
        self.despachador_eventos = DespachadorProveedores(topico_eventos=topico_eventos)
        self.repositorio = RepositorioProveedores(db_session=db_session)

    def procesar_comando(self, mensaje):
        """
        Procesa el comando recibido y publica un evento.
        """
        data = json.loads(mensaje)
        if data.get("comando") == "RegistrarProveedor":
            proveedor_data = data.get("data")

            # Remove correlation_id from the data before creating the Proveedor instance
            proveedor_data_without_correlation_id = {key: value for key, value in proveedor_data.items() if key != "correlation_id"}

            proveedor = Proveedor(**proveedor_data_without_correlation_id)

            # Guardar en la base de datos
            self.repositorio.guardar(proveedor)

            # Publicar evento en la cola de eventos
            evento = {
                "evento": "ProveedorRegistrado",
                "data": {
                    "id": proveedor.id,
                    "nombre": proveedor.nombre,
                    "email": proveedor.email,
                    "numero_contacto": proveedor.numero_contacto,
                    "pais": proveedor.pais,
                    "caracteristicas": proveedor.caracteristicas,
                    "condiciones_comerciales_tributarias": proveedor.condiciones_comerciales_tributarias,
                    "fecha_registro": proveedor.fecha_registro.isoformat(),
                    "correlation_id": proveedor_data.get("correlation_id"),  # Include correlation_id in the event
                },
            }
            self.despachador_eventos.publicar_evento(evento)
            print(f"Evento publicado: {evento}")

    def escuchar(self):
        """
        Escucha los comandos en la cola de comandos y los procesa.
        """
        consumidor = self.conexion.cliente.subscribe(
            self.topico_comandos, subscription_name="gestor_proveedores_sub",
            consumer_type=pulsar.ConsumerType.Shared
        )
        while True:
            mensaje = consumidor.receive()
            try:
                logger.info(f"Comando recibido: {mensaje.data().decode('utf-8')}")
                self.procesar_comando(mensaje.data().decode("utf-8"))
                consumidor.acknowledge(mensaje)
            except Exception as e:
                logger.info(f"Error procesando mensaje: {str(e)}")
                consumidor.negative_acknowledge(mensaje)

    def esperar_evento(self, tipo_evento, correlation_id, timeout=20):
        """
        Espera un evento específico en la cola de eventos dentro de un tiempo límite,
        filtrando por tipo de evento y correlation_id.
        """
        logger.info(f"Esperando evento '{tipo_evento}' con correlation_id '{correlation_id}' durante {timeout} segundos.")
        consumidor_eventos = self.conexion.cliente.subscribe(
            self.topico_eventos, subscription_name="gestor_proveedores_eventos_sub",
            consumer_type=pulsar.ConsumerType.Shared
        )
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                consumidor_eventos.seek(0)
                mensaje = consumidor_eventos.receive(timeout_millis=1000)
                logger.info(f"Mensaje recibido: {mensaje.data().decode('utf-8')}")
                evento = json.loads(mensaje.data().decode("utf-8"))
                logger.info(f"Evento procesado: {evento}")
                logger.info(f"Correlation ID in event: {evento['data'].get('correlation_id')}, Expected: {correlation_id}")
                # Check if the event matches the type and correlation_id
                if evento.get("evento") == tipo_evento and evento["data"].get("correlation_id") == correlation_id:
                    consumidor_eventos.acknowledge(mensaje)
                    return evento
                consumidor_eventos.acknowledge(mensaje)
            except pulsar.Timeout:
                logger.debug("No message received within the current timeout window.")
            except Exception as e:
                logger.error(f"Error procesando evento: {str(e)}")
                consumidor_eventos.negative_acknowledge(mensaje)

        logger.warning(f"Timeout esperando evento '{tipo_evento}' con correlation_id '{correlation_id}'.")
        return None