import unittest
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas, RepositorioEntregaProgramadasDetalle, Session
import datetime
from infraestructura.modelos import EntregasProgramadas, EntregaProgramadaDetalle

class TestRepositorioEntregasProgramadas(unittest.TestCase):
    def setUp(self):
        self.repositorio_entregas = RepositorioEntregasProgramadas()
        # Add a testing entrega programada object to the database
        self.test_entrega = {
            "fecha_programada": datetime.date(2023, 10, 1),
            "camion_id": 1,
            "ruta_calculada": "Ruta Test"
        }
        with Session() as session:
            entrega = EntregasProgramadas(**self.test_entrega)
            session.add(entrega)
            session.commit()
            self.test_entrega_id = entrega.id
            self.test_entrega_obj = entrega
    
    def tearDown(self):
        # clean up the database
        with Session() as session:
            session.query(EntregasProgramadas).delete()
            session.commit()

    
    def test_agregar_entrega_programada_success(self):
        # Define the entrega programada data
        entrega_data = EntregasProgramadas(
            fecha_programada=datetime.date(2023, 10, 1),
            camion_id=1,
            ruta_calculada="Nueva Ruta Test"
        )
        # Call the method
        entrega_id = self.repositorio_entregas.agregar_entrega_programada(entrega_data)

        # Assertions
        self.assertIsNotNone(entrega_id)
        self.assertTrue(isinstance(entrega_id, int))

        # remove the added entrega programada
        with Session() as session:
            entrega = session.query(EntregasProgramadas).filter_by(id=entrega_id).first()
            if entrega:
                session.delete(entrega)
                session.commit()

    def test_obtener_entrega_programada_por_id_success(self):
        # Call the method
        entrega = self.repositorio_entregas.obtener_entrega_programada_por_id(self.test_entrega_id)

        # Assertions
        self.assertIsNotNone(entrega)
        self.assertEqual(entrega.id, self.test_entrega_id)
    
    def test_obtener_entregas_programadas_por_fecha_camion_success(self):
        # Call the method
        entregas = self.repositorio_entregas.obtener_entregas_programadas_por_fecha_camion("2023-10-01", 1)

        # Assertions
        self.assertIsNotNone(entregas)
        self.assertEqual(len(entregas), 1)
        self.assertEqual(entregas[0].id, self.test_entrega_id)
    
    def test_actualizar_entrega_programada_success(self):
        # Define the new data
        nuevos_datos = {
            "fecha_programada": datetime.date(2023, 10, 3),
            "camion_id": 3,
            "ruta_calculada": "ruta actualizada"
        }
        # Call the method
        entrega_actualizada = self.repositorio_entregas.actualizar_entrega_programada(self.test_entrega_id, nuevos_datos)

        # Assertions
        self.assertIsNotNone(entrega_actualizada)
        self.assertEqual(entrega_actualizada.fecha_programada, datetime.date(2023, 10, 3))
        self.assertEqual(entrega_actualizada.camion_id, 3)
        self.assertEqual(entrega_actualizada.ruta_calculada, "ruta actualizada")

    def test_listar_entregas_programadas_success(self):
        # Call the method
        entregas = self.repositorio_entregas.listar_entregas_programadas()

        # Assertions
        self.assertIsNotNone(entregas)
        self.assertTrue(len(entregas) > 0)
        self.assertEqual(entregas[0].id, self.test_entrega_id)


