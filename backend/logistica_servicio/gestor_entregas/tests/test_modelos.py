import unittest
from datetime import date, time
from infraestructura.modelos import Entrega, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestEntregaModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up an in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback any changes and close the session
        self.session.rollback()
        self.session.close()

    def test_create_entrega(self):
        # Create a new Entrega instance
        entrega = Entrega(
            pedido_id=1,
            cliente_id=1,
            fecha_entrega=date(2023, 10, 1),
            hora_entrega=time(14, 30),
            estado="Pendiente",
            direccion_entrega="123 Main St",
            coordenadas_origen="10.1234,-75.1234",
            coordenadas_destino="10.5678,-75.5678",
            cantidad=5,
            valor_total=100.0
        )

        # Add and commit the instance to the database
        self.session.add(entrega)
        self.session.commit()

        # Query the database to verify the instance was added
        result = self.session.query(Entrega).filter_by(id=entrega.id).first()

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.pedido_id, 1)
        self.assertEqual(result.cliente_id, 1)
        self.assertEqual(result.fecha_entrega, date(2023, 10, 1))
        self.assertEqual(result.hora_entrega, time(14, 30))
        self.assertEqual(result.estado, "Pendiente")
        self.assertEqual(result.direccion_entrega, "123 Main St")
        self.assertEqual(result.coordenadas_origen, "10.1234,-75.1234")
        self.assertEqual(result.coordenadas_destino, "10.5678,-75.5678")
        self.assertEqual(result.cantidad, 5)
        self.assertEqual(result.valor_total, 100.0)

    def test_update_entrega(self):
        # Create and add a new Entrega instance
        entrega = Entrega(
            pedido_id=2,
            cliente_id=2,
            fecha_entrega=date(2023, 10, 2),
            hora_entrega=time(15, 0),
            estado="Pendiente",
            direccion_entrega="456 Another St",
            coordenadas_origen="11.1234,-76.1234",
            coordenadas_destino="11.5678,-76.5678",
            cantidad=10,
            valor_total=200.0
        )
        self.session.add(entrega)
        self.session.commit()

        # Update the instance
        entrega.estado = "Entregado"
        self.session.commit()

        # Query the database to verify the update
        result = self.session.query(Entrega).filter_by(id=entrega.id).first()

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.estado, "Entregado")

    def test_delete_entrega(self):
        # Create and add a new Entrega instance
        entrega = Entrega(
            pedido_id=3,
            cliente_id=3,
            fecha_entrega=date(2023, 10, 3),
            hora_entrega=time(16, 0),
            estado="Pendiente",
            direccion_entrega="789 Another St",
            coordenadas_origen="12.1234,-77.1234",
            coordenadas_destino="12.5678,-77.5678",
            cantidad=15,
            valor_total=300.0
        )
        self.session.add(entrega)
        self.session.commit()

        # Delete the instance
        self.session.delete(entrega)
        self.session.commit()

        # Query the database to verify the instance was deleted
        result = self.session.query(Entrega).filter_by(id=entrega.id).first()

        # Assertions
        self.assertIsNone(result)