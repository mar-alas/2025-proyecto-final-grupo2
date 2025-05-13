import unittest
from infraestructura.repositorio_camion import RepositorioCamion, Session
from infraestructura.modelos import Camion

class TestRepositorioCamion(unittest.TestCase):
    def setUp(self):
        self.repositorio_camion = RepositorioCamion()
        # Add a testing camion object to the database
        self.test_camion_data = {
            "placa": "TEST123",
            "marca": "TestMarca",
            "modelo": "TestModelo",
            "capacidad_carga_toneladas": 10.0,
            "volumen_carga_metros_cubicos": 20.0
        }
        with Session() as session:
            camion = Camion(**self.test_camion_data)
            session.add(camion)
            session.commit()
            self.test_camion_id = camion.id
            self.test_camion_obj = camion

    def tearDown(self):
        # Clean up the database
        with Session() as session:
            session.query(Camion).delete()
            session.commit()

    def test_registrar_camion_success(self):
        # Define the camion data
        camion_data = {
            "placa": "NEW123",
            "marca": "NewMarca",
            "modelo": "NewModelo",
            "capacidad_carga_toneladas": 15.0,
            "volumen_carga_metros_cubicos": 25.0
        }
        # Call the method
        camion_id = self.repositorio_camion.registrar_camion(camion_data)

        # Assertions
        self.assertIsNotNone(camion_id)
        self.assertTrue(isinstance(camion_id, int))

        # Remove the added camion
        with Session() as session:
            camion = session.query(Camion).filter_by(id=camion_id).first()
            if camion:
                session.delete(camion)
                session.commit()

    def test_obtener_camiones_success(self):
        # Call the method
        camiones = self.repositorio_camion.obtener_camiones()

        # Assertions
        self.assertIsNotNone(camiones)
        self.assertTrue(len(camiones) > 0)
        self.assertEqual(camiones[2]["placa"], self.test_camion_data["placa"])

    def test_obtener_camion_por_id_success(self):
        # Call the method
        camion = self.repositorio_camion.obtener_camion_por_id(self.test_camion_id)

        # Assertions
        self.assertIsNotNone(camion)
        self.assertEqual(camion["id"], self.test_camion_id)
        self.assertEqual(camion["placa"], self.test_camion_data["placa"])

    def test_obtener_camion_por_placa_success(self):
        # Call the method
        camion = self.repositorio_camion.obtener_camion_por_placa(self.test_camion_data["placa"])

        # Assertions
        self.assertIsNotNone(camion)
        self.assertEqual(camion["placa"], self.test_camion_data["placa"])

    def test_crear_camiones_por_defecto_success(self):
        # Call the method
        self.repositorio_camion.crear_camiones_por_defecto()

        # Assertions
        with Session() as session:
            camiones = session.query(Camion).all()
            self.assertTrue(len(camiones) >= 2)  # At least the two default trucks should exist
            placas = [camion.placa for camion in camiones]
            self.assertIn("ABC123", placas)
            self.assertIn("XYZ789", placas)