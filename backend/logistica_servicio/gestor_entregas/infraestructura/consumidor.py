from datetime import datetime, time, timedelta
import json
import random
import _pulsar
from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
from infraestructura.repositorio_entregas import RepositorioEntrega
from infraestructura.logistica_entregas import LogisticaEntregas
import logging
import requests
import os
from time import sleep

USUARIOS_HOSTNAME = os.getenv('USUARIOS_HOST', default="localhost")
USUARIOS_PORT = os.getenv('USUARIOS_PORT', default="3011")
PRODUCTOS_HOSTNAME = os.getenv('PRODUCTOS_HOST', default="localhost")
PRODUCTOS_PORT = os.getenv('PRODUCTOS_PORT', default="3001")

class ConsumidorLogistica:
    def __init__(self, topico_pedido):
        self.conexion = ConexionPulsar()
        self.topico_pedido = topico_pedido
        self.repositorio = RepositorioEntrega()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def procesar_registro_pedido(self, mensaje):
        try:
            self.logger.info(f"Procesando mensaje de pedido: {mensaje}")
            data = json.loads(mensaje)
            token = data.get("token")
            cliente_data = self.get_client_data(data.get("cliente_id"), token)
            fecha_entrega, cantidad_productos = self.get_delivery_date(data.get("productos"), data.get("fecha_creacion"), token)
            fecha_entrega = str(fecha_entrega)  # Convert fecha_entrega to string if needed
            entrega_data = {
                "pedido_id": data.get("pedido_id"),
                "cliente_id": data.get("cliente_id"),
                "fecha_entrega": fecha_entrega,  # Use a string in ISO format or a `datetime.date` object
                "hora_entrega": f"{random.randint(8, 17)}:00:00",  # Use a string in HH:MM:SS format or a `datetime.time` object
                "estado": data.get("estado"),
                "direccion_entrega": cliente_data.get("address"),
                "coordenadas_origen": "4.7110,-74.0721",
                "coordenadas_destino": cliente_data.get("geographic_coordinates"),
                "cantidad": cantidad_productos,
                "valor_total": data.get("total")
            }
            entrega_id = self.repositorio.registrar_entrega(entrega_data)
            logistica_entregas = LogisticaEntregas()
            detalle_id, camion_id = logistica_entregas.asignar_camion_a_entrega(entrega_id)
            self.logger.info(f"Entrega registrada con ID: {entrega_id}")
            self.logger.info(f"Detalle de entrega registrado con ID: {detalle_id}")
            logistica_entregas.actualizar_entregas_programadas(
                entrega_id=entrega_id,
                fecha=fecha_entrega,
                camion_id=camion_id,
                destino_coordenadas=cliente_data.get("geographic_coordinates"),
                destino_direccion=cliente_data.get("address"),
                origen="4.7110,-74.0721"
            )
            # llamar al calculo de ruta
        except Exception as e:
            self.logger.error(f"Error procesando mensaje de pedido: {e}")

    def get_client_data(self, cliente_id, token):
        url = f'http://{USUARIOS_HOSTNAME}:{USUARIOS_PORT}/api/v1/seguridad/gestor_usuarios/r/clientes'
        response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        clientes = response.json()

        for cliente in clientes["clientes"]:
            if cliente["id"] == cliente_id:
                return {
                    "address": cliente.get("address"),
                    "geographic_coordinates": cliente.get("geographic_coordinates")
                }
        self.logger.error(f"Error al consultar los clientes: cliente_id no existe")

    def get_delivery_date(self, entrega_productos, fecha_pedido, token):
        # request to get product data
        # for now, we will just return a dummy data
        url = f'http://{PRODUCTOS_HOSTNAME}:{PRODUCTOS_PORT}/api/v2/inventario/gestor_productos/productos'
        response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        productos = response.json()
        cantidad_productos = 0
        max_delivery_time = 0
        for product in entrega_productos:
            product_data = next((p for p in productos["products"] if int(p["id"]) == int(product)), None)
            cantidad_productos += entrega_productos[product]['cantidad']
            if product_data:
                try:
                    delivery_time = product_data.get("tiempo_entrega", "2")
                    delivery_time = int(delivery_time.split(' ')[0])  # Convert to integer
                except (ValueError, AttributeError):
                    delivery_time = random.randint(1, 5)  # Random value between 1 and 5 if conversion fails
                max_delivery_time = max(max_delivery_time, delivery_time)
        # Calculate delivery date
        fecha_pedido_dt = datetime.strptime(fecha_pedido, "%Y-%m-%d %H:%M:%S.%f")  # Assuming fecha_pedido is in "YYYY-MM-DD" format
        delivery_date = fecha_pedido_dt + timedelta(days=max_delivery_time)
        return delivery_date, cantidad_productos

    def obtener_mejor_ruta(self, origen, destinos):
        pass

    def escuchar(self, max_iterations=None):
        self.logger.info("Iniciando escucha de tópicos")
        max_retries = 5
        retry_delay = 25  # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                self.conexion.cliente.create_producer(self.topico_pedido).close()
                consumidor_pedido = self.conexion.cliente.subscribe(
                    self.topico_pedido,
                    subscription_name="logistica_pedido_sub",
                    consumer_type=_pulsar.ConsumerType.Shared
                )
                break  # Exit loop if subscription is successful
            except _pulsar.Timeout as e:
                self.logger.warning(f"Intento {attempt + 1} de {max_retries} fallido: {e}")
                if attempt < max_retries - 1:
                    sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    self.logger.error("No se pudo suscribir al tópico después de varios intentos")
                    raise

        iteration = 0
        while True:
            if max_iterations is not None and iteration >= max_iterations:
                break
            iteration += 1
            try:
                mensaje_pedido = consumidor_pedido.receive(timeout_millis=100)
                self.logger.info("Mensaje recibido en tópico de pedido")
                self.procesar_registro_pedido(mensaje_pedido.data().decode("utf-8"))
                consumidor_pedido.acknowledge(mensaje_pedido)
            except _pulsar.Timeout:
                pass  # No hay mensajes en el tópico de pedido, continuar escuchando
            except Exception as e:
                self.logger.error(f"Error en el proceso de escucha: {type(e).__name__}: {e}")
                break
        self.conexion.cliente.close()
        self.logger.info("Escucha de tópicos finalizada")
