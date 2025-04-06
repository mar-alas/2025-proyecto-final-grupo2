import os
os.environ['UTEST'] = "True"  # Set the UTEST variable before importing anything

import unittest
from flask import Flask
from aplicacion.lecturas.pedidos import pedidos_lectura
from aplicacion.escrituras.pedidos import pedidos_escritura
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime
from unittest.mock import patch

# Define a mock Pedido and Producto models for testing
Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Integer)

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer)
    vendedor_id = Column(Integer)
    estado = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)
    subtotal = Column(Integer)  # Add this line
    total = Column(Integer)
    productos = []

class TestPedidos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database
        cls.engine = create_engine("sqlite:///ventas_servicio.db")
        cls.Session = sessionmaker(bind=cls.engine)

        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(pedidos_lectura)
        cls.app.register_blueprint(pedidos_escritura)
        cls.client = cls.app.test_client()

    def setUp(self):
        # Drop and recreate all tables to ensure schema consistency
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        # Recreate the session for each test
        self.db_session = self.Session()

    def tearDown(self):
        # Close the session after each test
        self.db_session.close()
        Base.metadata.drop_all(self.engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables and dispose of the engine after all tests
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    @patch('aplicacion.escrituras.pedidos.obtener_stock_disponible')
    def test_registrar_pedido_exitoso(self, mock_obtener_stock_disponible):
        # Mock the response of obtener_stock_disponible
        mock_obtener_stock_disponible.return_value = [
            {"id": 1, "inventario_inicial": 100, "precio": 50},
            {"id": 2, "inventario_inicial": 50, "precio": 120}
        ]

        # Test the POST /pedidos endpoint
        payload = {
            "cliente_id": 123456,
            "vendedor_id": 987654,
            "productos": [
                {"id": 1, "cantidad": 10, "precio_unitario": 50},
                {"id": 2, "cantidad": 5, "precio_unitario": 120}
            ]
        }
        response = self.client.post('/pedidos', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Pedido registrado exitosamente")

    def test_obtener_todos_los_pedidos(self):
        # First, create a pedido using POST
        self.test_registrar_pedido_exitoso()

        # Then, test the GET /pedidos endpoint
        response = self.client.get('/pedidos?cliente_id=123456')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total'], 1)
        self.assertEqual(len(data['pedidos']), 1)
        self.assertEqual(data['pedidos'][0]['id'], 1)
        self.assertEqual(data['pedidos'][0]['estado'], "pendiente")

    def test_obtener_pedidos_cliente_sin_pedidos(self):
        response = self.client.get('/pedidos?cliente_id=999999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "El cliente no tiene pedidos")

    def test_falta_cliente_id(self):
        response = self.client.get('/pedidos')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "El parámetro 'cliente_id' es obligatorio")


if __name__ == '__main__':
    unittest.main()