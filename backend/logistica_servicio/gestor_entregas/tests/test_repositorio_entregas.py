import unittest
import datetime
from infraestructura.repositorio_entregas import RepositorioEntrega, Session, RepositorioDetalleEntrega
from infraestructura.modelos import Entrega, DetalleEntrega, Base

class TestRepositorioEntrega(unittest.TestCase):
    def setUp(self):
        self.repositorio_entrega = RepositorioEntrega()
        # Add a testing entrgea object to the database
        self.test_entrega = {
            "pedido_id": 101,
            "cliente_id": 1,
            "fecha_entrega": datetime.date(2025, 5, 5),
            "hora_entrega": datetime.time(14, 0),
            "estado": "pendiente",
            "direccion_entrega": "Calle 123",
            "coordenadas_origen": "4.7110,-74.0721",
            "coordenadas_destino": "4.6097,-74.0817",
            "cantidad": 2,
            "valor_total": 50000.0
        }
        with Session() as session:
            entrega = Entrega(**self.test_entrega)
            session.add(entrega)
            session.commit()
            self.test_entrega_id = entrega.id

    def tearDown(self):
        # clean up the database
        with Session() as session:
            session.query(Entrega).delete()
            session.commit()

    def test_registrar_entrega_success(self):
        # Define the entrega data
        entrega_data = {
            "pedido_id": 101,
            "cliente_id": 1,
            "fecha_entrega": datetime.date(2025, 5, 5),
            "hora_entrega": datetime.time(14, 0),
            "estado": "pendiente",
            "direccion_entrega": "Calle 123",
            "coordenadas_origen": "4.7110,-74.0721",
            "coordenadas_destino": "4.6097,-74.0817",
            "cantidad": 2,
            "valor_total": 50000.0
        }
        # Call the method
        entrega_id = self.repositorio_entrega.registrar_entrega(entrega_data)

        # Assertions
        self.assertIsNotNone(entrega_id)
        self.assertTrue(isinstance(entrega_id, int))

        # remove the added entrega
        with Session() as session:
            entrega = session.query(Entrega).filter_by(id=entrega_id).first()
            if entrega:
                session.delete(entrega)
                session.commit()

    def test_actualizar_estado_entrega_success(self):
        self.repositorio_entrega.actualizar_estado_entrega(self.test_entrega_id, "entregado")
        with Session() as session:
            entrega = session.query(Entrega).filter_by(id=self.test_entrega_id).first()
            self.assertEqual(entrega.estado, "entregado")
    
    def test_actualizar_estado_entrega_not_found(self):
        # Call the method and assert exception
        with self.assertRaises(ValueError):
            self.repositorio_entrega.actualizar_estado_entrega(9999, "entregado")

    def test_obtener_entregas_success(self):
        # Call the method
        entregas = self.repositorio_entrega.obtener_entregas()

        # Assertions
        self.assertEqual(len(entregas), 1)
        self.assertEqual(entregas[0]["id"], self.test_entrega_id)

    def test_obtener_entrega_por_id_success(self):
        # Call the method
        entrega = self.repositorio_entrega.obtener_entrega_por_id(self.test_entrega_id)

        # Assertions
        self.assertEqual(entrega["id"], self.test_entrega_id)
        
class TestRepositorioDetalleEntrega(unittest.TestCase):
    def setUp(self):
        self.repositorio_detalle_entrega = RepositorioDetalleEntrega()
        # Add a testing detalle entrega object to the database
        self.test_detalle_entrega = {
            "entrega_id": 1,
            "camion_id": 1
        }
        with Session() as session:
            detalle_entrega = DetalleEntrega(**self.test_detalle_entrega)
            session.add(detalle_entrega)
            session.commit()
            self.test_detalle_entrega_id = detalle_entrega.id

    def tearDown(self):
        # clean up the database
        with Session() as session:
            session.query(DetalleEntrega).delete()
            session.commit()
    
    def test_registrar_detalle_entrega_success(self):
        # Define the detalle entrega data
        detalle_data = {
            "entrega_id": 1,
            "camion_id": 1
        }
        # Call the method
        detalle_id = self.repositorio_detalle_entrega.registrar_detalle_entrega(detalle_data)

        # Assertions
        self.assertIsNotNone(detalle_id)
        self.assertTrue(isinstance(detalle_id, int))

        # remove the added detalle entrega
        with Session() as session:
            detalle = session.query(DetalleEntrega).filter_by(id=detalle_id).first()
            if detalle:
                session.delete(detalle)
                session.commit()

    def test_obtener_detalle_entrega_success(self):
        # Call the method
        detalle_entrega = self.repositorio_detalle_entrega.obtener_detalles_por_entrega(self.test_detalle_entrega_id)

        # Assertions
        self.assertEqual(detalle_entrega[0]["id"], self.test_detalle_entrega_id)

if __name__ == "__main__":
    unittest.main()