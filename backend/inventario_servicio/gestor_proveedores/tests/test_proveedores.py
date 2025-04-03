import os
os.environ['UTEST'] = "True"  # Set the UTEST variable before importing anything

import unittest
from flask import Flask
from aplicacion.lecturas.proveedores import proveedores_lectura
from aplicacion.escrituras.proveedores import proveedores_escritura
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from unittest.mock import MagicMock, patch

# Define a mock Proveedor model for testing
Base = declarative_base()

class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String)
    numero_contacto = Column(String)
    pais = Column(String)
    caracteristicas = Column(String)
    condiciones_comerciales_tributarias = Column(String)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)

class TestProveedoresLecturas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database
        cls.engine = create_engine("sqlite:///proveedores.db")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.db_session = cls.Session()

        # Add mock data
        cls.db_session.add_all([
            Proveedor(
                id=1,
                nombre="Proveedor 1",
                email="proveedor1@example.com",
                numero_contacto="123456789",
                pais="Colombia",
                caracteristicas="Caracteristicas 1",
                condiciones_comerciales_tributarias="Condiciones 1"
            ),
            Proveedor(
                id=2,
                nombre="Proveedor 2",
                email="proveedor2@example.com",
                numero_contacto="987654321",
                pais="Argentina",
                caracteristicas="Caracteristicas 2",
                condiciones_comerciales_tributarias="Condiciones 2"
            )
        ])
        cls.db_session.commit()

        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(proveedores_lectura)
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.db_session.close()
        Base.metadata.drop_all(cls.engine)

    def test_obtener_todos_los_proveedores(self):
        response = self.client.get('/proveedores')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['nombre'], "Proveedor 1")
        self.assertEqual(data[1]['nombre'], "Proveedor 2")

    def test_obtener_proveedor_por_id_existente(self):
        response = self.client.get('/proveedores?id=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['nombre'], "Proveedor 1")
        self.assertEqual(data['email'], "proveedor1@example.com")

    def test_obtener_proveedor_por_id_inexistente(self):
        response = self.client.get('/proveedores?id=999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Proveedor no encontrado")

class TestProveedoresEscrituras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up a testing database
        cls.engine = create_engine("sqlite:///proveedores.db")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.db_session = cls.Session()

        # Mock Pulsar components
        cls.mock_despachador = MagicMock()
        cls.mock_consumidor = MagicMock()

        # Patch the Pulsar components in the Flask blueprint
        cls.patcher_despachador = patch(
            'aplicacion.escrituras.proveedores.despachador_comandos',
            cls.mock_despachador
        )
        cls.patcher_consumidor = patch(
            'aplicacion.escrituras.proveedores.consumidor',
            cls.mock_consumidor
        )

        cls.patcher_despachador.start()
        cls.patcher_consumidor.start()
        # cls.patcher_repositorio.start()
        # cls.patcher_db_session.start()

        # Create a Flask app for testing
        cls.app = Flask(__name__)
        cls.app.register_blueprint(proveedores_escritura)
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.db_session.close()
        Base.metadata.drop_all(cls.engine)
        cls.patcher_despachador.stop()
        cls.patcher_consumidor.stop()

    def test_registrar_proveedor_exitoso(self):
        # Simulate a POST request with valid data
        data = {
            "nombre": "Proveedor 3",
            "email": "proveedor3@example.com",
            "numero_contacto": "555555555",
            "pais": "Chile",
            "caracteristicas": "Caracteristicas 3",
            "condiciones_comerciales_tributarias": "Condiciones 3"
        }

        # Mock Pulsar behavior
        self.mock_despachador.publicar_evento.return_value = None
        self.mock_consumidor.esperar_evento.return_value = {"evento": "ProveedorRegistrado"}

        response = self.client.post('/proveedores', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Proveedor registrado exitosamente")

        # Verify Pulsar interactions
        expected_data = data.copy()
        expected_data["correlation_id"] = unittest.mock.ANY  # Ignore the correlation_id value
        self.mock_despachador.publicar_evento.assert_called_once_with({
            "comando": "RegistrarProveedor",
            "data": expected_data
        })
        self.mock_consumidor.esperar_evento.assert_called_once_with(
            "ProveedorRegistrado", timeout=20, correlation_id=unittest.mock.ANY
        )

    def test_registrar_proveedor_datos_invalidos(self):
        # Simulate a POST request with invalid data (missing required fields)
        data = {
            "nombre": "Proveedor 4"
            # Missing other required fields
        }
        response = self.client.post('/proveedores', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

        # Ensure Pulsar was not called
        self.mock_despachador.publicar_evento.assert_not_called()
        self.mock_consumidor.esperar_evento.assert_not_called()

if __name__ == '__main__':
    unittest.main()