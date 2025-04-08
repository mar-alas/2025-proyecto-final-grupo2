import json
import pulsar
import _pulsar
from seedwork_compartido.infraestructura.broker_utils import ConexionPulsar
from infraestructura.repositorio import RepositorioStock
import logging

class ConsumidorStock:
    def __init__(self, topico_producto, topico_pedido):
        self.conexion = ConexionPulsar()
        self.topico_producto = topico_producto
        self.topico_pedido = topico_pedido
        self.repositorio = RepositorioStock()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def procesar_registro_producto(self, mensaje):
        try:
            self.logger.info(f"Procesando mensaje de producto: {mensaje}")
            data = json.loads(mensaje)
            producto_id = data.get("producto_id")
            inventario_inicial = data.get("inventario_inicial", 0)
            if producto_id:
                self.repositorio.actualizar_inventario_inicial(producto_id, inventario_inicial)
                self.logger.info(f"Inventario actualizado para producto {producto_id} con cantidad {inventario_inicial}")
            else:
                self.logger.warning("Mensaje de producto no contiene 'producto_id'")
        except Exception as e:
            self.logger.error(f"Error procesando mensaje de producto: {e}")

    def procesar_registro_pedido(self, mensaje):
        try:
            self.logger.info(f"Procesando mensaje de pedido: {mensaje}")
            data = json.loads(mensaje)
            producto_id = data.get("producto_id")
            cantidad = data.get("cantidad", 0)
            if producto_id and cantidad:
                self.repositorio.actualizar_inventario(producto_id, -cantidad)
                self.logger.info(f"Inventario actualizado para producto {producto_id} con decremento de {cantidad}")
            else:
                self.logger.warning("Mensaje de pedido no contiene 'producto_id' o 'cantidad'")
        except Exception as e:
            self.logger.error(f"Error procesando mensaje de pedido: {e}")

    def escuchar(self, max_iterations=None):
        self.logger.info("Iniciando escucha de tópicos")
        consumidor_producto = self.conexion.cliente.subscribe(
            self.topico_producto,
            subscription_name="gestor_stock_producto_sub",
            consumer_type=_pulsar.ConsumerType.Shared
        )
        consumidor_pedido = self.conexion.cliente.subscribe(
            self.topico_pedido,
            subscription_name="gestor_stock_pedido_sub",
            consumer_type=_pulsar.ConsumerType.Shared
        )

        iteration = 0
        while True:
            if max_iterations is not None and iteration >= max_iterations:
                break
            iteration += 1

            try:
                try:
                    mensaje_producto = consumidor_producto.receive(timeout_millis=100)
                    self.logger.info("Mensaje recibido en tópico de producto")
                    self.procesar_registro_producto(mensaje_producto.data().decode("utf-8"))
                    consumidor_producto.acknowledge(mensaje_producto)
                except _pulsar.Timeout:
                    pass  # No hay mensajes en el tópico de producto, continuar escuchando

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
