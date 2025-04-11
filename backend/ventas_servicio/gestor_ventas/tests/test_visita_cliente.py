import os
os.environ['UTEST'] = "True"  # Set the UTEST variable before importing anything

import unittest
from flask import Flask
from aplicacion.escrituras.visita_cliente import visita_cliente_bp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON
import datetime
from unittest.mock import patch
import requests

# Define a mock VisitaCliente model for testing
Base = declarative_base()

class VisitaCliente(Base):
    __tablename__ = 'visitas_cliente'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer)
    vendedor_id = Column(Integer)
    fecha = Column(DateTime)
    ubicacion_productos_ccp = Column(JSON)
    ubicacion_productos_competencia = Column(JSON)

class TestVisitaCliente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database
        cls.engine = create_engine("sqlite:///ventas_servicio_test.db")
        cls.Session = sessionmaker(bind=cls.engine)

        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(visita_cliente_bp)
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

    @patch('aplicacion.escrituras.visita_cliente.validar_token')
    @patch('aplicacion.escrituras.visita_cliente.validar_cliente')
    @patch('aplicacion.escrituras.visita_cliente.validar_productos')
    def test_registrar_visita_cliente_exitoso(self, mock_validar_productos, mock_validar_cliente, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True

        # Mock the response of validar_cliente
        mock_validar_cliente.return_value = None

        # Mock the response of validar_productos
        mock_validar_productos.return_value = None

        # Test the POST /visita_cliente endpoint
        payload = {
            "cliente_id": 123456,
            "vendedor_id": 987654,
            "fecha": "2025-05-31T00:00:00.000Z",
            "ubicacion_productos_ccp": [
                {"id_producto": 1, "ubicacion": "caja"},
                {"id_producto": 2, "ubicacion": "pasillo_principal"}
            ],
            "ubicacion_productos_competencia": [
                {"id_producto": 3, "ubicacion": "neveras"}
            ]
        }
        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.post('/visita_cliente', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Visita registrada exitosamente")

    @patch('aplicacion.escrituras.visita_cliente.validar_token')
    def test_falta_token(self, mock_validar_token):
        # Mock the token validation to always return False
        mock_validar_token.return_value = False

        # Test the POST /visita_cliente endpoint without a token
        payload = {
            "cliente_id": 123456,
            "vendedor_id": 987654,
            "fecha": "2025-05-31T00:00:00.000Z",
            "ubicacion_productos_ccp": [
                {"id_producto": 1, "ubicacion": "caja"}
            ],
            "ubicacion_productos_competencia": [
                {"id_producto": 3, "ubicacion": "neveras"}
            ]
        }
        response = self.client.post('/visita_cliente', json=payload)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "No se proporcionó un token")

    @patch('aplicacion.escrituras.visita_cliente.validar_token')
    @patch('aplicacion.escrituras.visita_cliente.validar_cliente')
    def test_cliente_no_existe(self, mock_validar_cliente, mock_validar_token):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True

        # Mock the response of validar_cliente to return an error
        mock_validar_cliente.return_value = ({
            "error": "Datos inválidos",
            "detalles": {
                "cliente_id": "El cliente no existe"
            }
        }), 400

        # Test the POST /visita_cliente endpoint
        payload = {
            "cliente_id": 999999,
            "vendedor_id": 987654,
            "fecha": "2025-05-31T00:00:00.000Z",
            "ubicacion_productos_ccp": [
                {"id_producto": 1, "ubicacion": "caja"}
            ],
            "ubicacion_productos_competencia": [
                {"id_producto": 3, "ubicacion": "neveras"}
            ]
        }
        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.post('/visita_cliente', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Datos inválidos")

    @patch('aplicacion.escrituras.visita_cliente.validar_productos')
    @patch('aplicacion.escrituras.visita_cliente.validar_cliente', autospec=True)
    @patch('aplicacion.escrituras.visita_cliente.validar_token', autospec=True)
    def test_productos_no_validos(self, mock_validar_token, mock_validar_cliente, mock_validar_productos):
        # Mock the token validation to always return True
        mock_validar_token.return_value = True
        mock_validar_cliente.return_value = None
        

        # Mock the response of validar_productos to return an error
        mock_validar_productos.return_value = ({
            "error": "Productos no válidos",
            "detalles": {
            "producto_id": "El producto no existe"
            }
        }), 400

        # Test the POST /visita_cliente endpoint
        payload = {
            "cliente_id": 123456,
            "vendedor_id": 987654,
            "fecha": "2025-05-31T00:00:00.000Z",
            "ubicacion_productos_ccp": [
                {"id_producto": 999, "ubicacion": "caja"}
            ],
            "ubicacion_productos_competencia": [
                {"id_producto": 3, "ubicacion": "neveras"}
            ]
        }
        headers = {"Authorization": "Bearer mock_token"}
        response = self.client.post('/visita_cliente', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Productos no válidos")


if __name__ == '__main__':
    unittest.main()