import os
import threading
import time
os.environ['UTEST'] = "True"  # Set the UTEST variable before importing anything
import _pulsar
import unittest
from unittest.mock import MagicMock, patch
from infraestructura.consumidor import ConsumidorStock
from infraestructura.repositorio import RepositorioStock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infraestructura.modelos import Base, Stock, Producto

# Mock _pulsar.Timeout as an exception
patch('_pulsar.Timeout', new=type('MockTimeout', (Exception,), {})).start()

class TestConsumidorStock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database
        cls.engine = create_engine("sqlite:///test_stock.db")
        Base.metadata.drop_all(cls.engine)  # Drop all tables to ensure a clean slate
        Base.metadata.create_all(cls.engine)  # Recreate all tables
        cls.Session = sessionmaker(bind=cls.engine)
        cls.db_session = cls.Session()

        # Ensure the stock table is empty
        cls.db_session.query(Stock).delete()

        # Add mock data for Producto
        cls.db_session.add_all([
            Producto(
                id=1,
                nombre="Sal",
                descripcion="Sal refinada para consumo diario",
                tiempo_entrega="2 días",
                precio=50.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco",
                fecha_vencimiento="2025-12-31",
                estado="en_stock",
                inventario_inicial=500,
                imagenes_productos="sal1.jpg,sal2.jpg",
                proveedor="Proveedor Salinas S.A."
            ),
            Producto(
                id=2,
                nombre="Arroz",
                descripcion="Arroz blanco de grano largo",
                tiempo_entrega="3 días",
                precio=120.0,
                condiciones_almacenamiento="Almacenar en lugar fresco y seco",
                fecha_vencimiento="2025-12-31",
                estado="en_stock",
                inventario_inicial=300,
                imagenes_productos="arroz1.jpg,arroz2.jpg",
                proveedor="Proveedor Arrocero S.A."
            )
        ])
        cls.db_session.commit()

        # Mock Pulsar connection
        cls.mock_pulsar_client = MagicMock()
        cls.mock_pulsar_consumer_producto = MagicMock()
        cls.mock_pulsar_consumer_pedido = MagicMock()

        cls.mock_pulsar_client.subscribe.side_effect = lambda topic, subscription_name, consumer_type: (
            cls.mock_pulsar_consumer_producto if topic == "ProductoRegistrado" else cls.mock_pulsar_consumer_pedido
        )

        # Patch Pulsar connection
        cls.patcher_pulsar = patch('infraestructura.consumidor.ConexionPulsar')
        cls.mock_conexion_pulsar = cls.patcher_pulsar.start()
        cls.mock_conexion_pulsar.return_value.cliente = cls.mock_pulsar_client

        # Patch pulsar to point to _pulsar
        cls.patcher_pulsar_module = patch.dict('sys.modules', {'pulsar': _pulsar})
        cls.patcher_pulsar_module.start()

        # Patch _pulsar.ConsumerType
        cls.patcher_consumer_type = patch('_pulsar.ConsumerType')
        cls.mock_consumer_type = cls.patcher_consumer_type.start()
        cls.mock_consumer_type.Shared = 'Shared'

        # Patch _pulsar.Timeout
        cls.patcher_timeout = patch('_pulsar.Timeout', new=Exception("Mocked Timeout"))
        cls.mock_timeout = cls.patcher_timeout.start()

        # Initialize the consumer
        cls.consumidor = ConsumidorStock(
            topico_producto="ProductoRegistrado",
            topico_pedido="PedidoProcesado",
            db_session=cls.db_session
        )

    @classmethod
    def tearDownClass(cls):
        cls.db_session.close()
        Base.metadata.drop_all(cls.engine)
        cls.patcher_pulsar.stop()
        cls.patcher_consumer_type.stop()
        cls.patcher_pulsar_module.stop()
        cls.patcher_timeout.stop()

    def test_procesar_registro_producto(self):
        # Mock message for ProductoRegistrado
        mensaje_producto = '{"producto_id": 1, "inventario_inicial": 500}'
        self.consumidor.procesar_registro_producto(mensaje_producto)

        # Verify the database update
        stock = self.db_session.query(Stock).filter_by(producto_id=1).first()
        self.assertIsNotNone(stock)
        self.assertEqual(stock.inventario, 500)

    def test_procesar_registro_pedido(self):
        # Add initial stock for testing
        existing_stock = self.db_session.query(Stock).filter_by(producto_id=1).first()
        if not existing_stock:
            self.db_session.add(Stock(producto_id=1, inventario=500))
            self.db_session.commit()
        else:
            existing_stock.inventario = 500
            self.db_session.commit()

        # Mock message for PedidoProcesado
        mensaje_pedido = '{"producto_id": 1, "cantidad": 20}'
        self.consumidor.procesar_registro_pedido(mensaje_pedido)

        # Verify the database update
        stock = self.db_session.query(Stock).filter_by(producto_id=1).first()
        self.assertIsNotNone(stock)
        self.assertEqual(stock.inventario, 480)


    def test_procesar_registro_producto_sin_producto_id(self):
        # Mock message without producto_id
        mensaje_producto = '{"inventario_inicial": 500}'
        with self.assertLogs(self.consumidor.logger, level='WARNING') as log:
            self.consumidor.procesar_registro_producto(mensaje_producto)
            self.assertIn("Mensaje de producto no contiene 'producto_id'", log.output[0])

    def test_procesar_registro_pedido_sin_producto_id(self):
        # Mock message without producto_id
        mensaje_pedido = '{"cantidad": 10}'
        with self.assertLogs(self.consumidor.logger, level='WARNING') as log:
            self.consumidor.procesar_registro_pedido(mensaje_pedido)
            self.assertIn("Mensaje de pedido no contiene 'producto_id' o 'cantidad'", log.output[0])

    def test_escuchar_for_10_seconds(self):
        # Mock messages for both topics
        self.mock_pulsar_consumer_producto.receive.side_effect = [
            MagicMock(data=lambda: b'{"producto_id": 1, "inventario_inicial": 500}'),
            Exception("StopIteration")  # Stop the loop after one iteration
        ]
        self.mock_pulsar_consumer_pedido.receive.side_effect = [
            MagicMock(data=lambda: b'{"producto_id": 1, "cantidad": 10}'),
            Exception("StopIteration")  # Stop the loop after one iteration
        ]
        
        with patch.object(self.consumidor, 'logger') as mock_logger:
            with self.assertRaises(Exception):  # Expect StopIteration to break the loop
                listener_thread = threading.Thread(target=self.consumidor.escuchar)
                listener_thread.start()
                time.sleep(10)
                listener_thread.stop()

            # Verify processing of messages
            stock = self.db_session.query(Stock).filter_by(producto_id=1).first()
            self.assertIsNotNone(stock)
            self.assertEqual(stock.inventario, 490)  # 50 (initial) - 10 (pedido)

    def test_escuchar(self):
        # Mock messages for both topics
        self.mock_pulsar_consumer_producto.receive.side_effect = [
            MagicMock(data=lambda: b'{"producto_id": 1, "inventario_inicial": 500}'),
            _pulsar.Timeout,  # Simulate no more messages
        ]
        self.mock_pulsar_consumer_pedido.receive.side_effect = [
            MagicMock(data=lambda: b'{"producto_id": 1, "cantidad": 10}'),
            _pulsar.Timeout,  # Simulate no more messages
        ]

        with patch.object(self.consumidor, 'logger') as mock_logger:
            # Call escuchar with max_iterations=2 to limit the loop
            self.consumidor.escuchar(max_iterations=2)

            # Verify that the messages were processed
            stock = self.db_session.query(Stock).filter_by(producto_id=1).first()
            self.assertIsNotNone(stock)
            self.assertEqual(stock.inventario, 490)  # 500 (initial) - 10 (pedido)

            # Verify that logs were written
            mock_logger.info.assert_any_call("Mensaje recibido en tópico de producto")
            mock_logger.info.assert_any_call("Mensaje recibido en tópico de pedido")

if __name__ == '__main__':
    unittest.main()