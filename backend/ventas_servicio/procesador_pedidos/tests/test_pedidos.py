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
import requests

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
    subtotal = Column(Integer)
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

    @patch('aplicacion.escrituras.pedidos.validar_token')
    @patch('aplicacion.escrituras.pedidos.obtener_stock_disponible')
    @patch('requests.get')  # Mock the REST request made by validar_cliente
    def test_registrar_pedido_exitoso(self, mock_requests_get, mock_obtener_stock_disponible, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True

        # Mock the response of obtener_stock_disponible
        mock_obtener_stock_disponible.return_value = [
            {"producto_id": 1, "inventario": 100, "precio": 50, "nombre": "Producto 1"},
            {"producto_id": 2, "inventario": 50, "precio": 12, "nombre": "Producto 2"}
        ]

        # Mock the REST request made by validar_cliente
        mock_requests_get.return_value = requests.Response()
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json = lambda: {
            "clientes": [{"id": 123456, "name": "Cliente Test"}]
        }

        # Test the POST /pedidos endpoint
        payload = {
            "cliente_id": 123456,
            "vendedor_id": 987654,
            "productos": [
                {"id": 1, "cantidad": 10, "precio_unitario": 50},
                {"id": 2, "cantidad": 5, "precio_unitario": 120}
            ]
        }
        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.post('/pedidos', json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Pedido registrado exitosamente")

    @patch('aplicacion.lecturas.pedidos.validar_token')
    @patch('dominio.reglas_negocio.obtener_stock_disponible')
    @patch('dominio.reglas_negocio.validar_cliente')
    def test_obtener_todos_los_pedidos(self, validar_cliente, obtener_stock_disponible, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True
        # Mock the validation functions
        validar_cliente.return_value = None
        obtener_stock_disponible.return_value = [
            {"producto_id": 1, "inventario": 100, "precio": 50, "nombre": "Producto 1"},
            {"producto_id": 2, "inventario": 50, "precio": 120, "nombre": "Producto 2"}
        ]

        # First, create a pedido using POST
        self.test_registrar_pedido_exitoso()

        # Then, test the GET /pedidos endpoint
        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.get('/pedidos?cliente_id=123456', headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total'], 1)
        self.assertEqual(len(data['pedidos']), 1)
        self.assertEqual(data['pedidos'][0]['id'], 1)
        self.assertEqual(data['pedidos'][0]['estado'], "pendiente")

    @patch('aplicacion.lecturas.pedidos.validar_token')
    def test_obtener_pedidos_cliente_sin_pedidos(self, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True

        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.get('/pedidos?cliente_id=999999', headers=headers)
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "El cliente no tiene pedidos")

    @patch('aplicacion.lecturas.pedidos.validar_token')
    def test_falta_cliente_id(self, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True

        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.get('/pedidos', headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "El parámetro 'cliente_id' es obligatorio")


if __name__ == '__main__':
    unittest.main()