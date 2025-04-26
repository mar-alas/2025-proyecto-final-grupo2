import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from infraestructura.repositorio import RutasVisitas

class TestRutasVisitas(unittest.TestCase):
    def setUp(self):
        # Mock the database session
        self.mock_session = MagicMock()
        self.rutas_visitas = RutasVisitas(db_session=self.mock_session)

    @patch("infraestructura.repositorio.datetime")
    def test_obtener_rutas_por_vendedor_y_fecha_success(self, mock_datetime):
        # Mock the datetime.strptime to avoid actual parsing
        mock_datetime.strptime.return_value = datetime(2025, 4, 21)
        mock_datetime.date.return_value = datetime(2025, 4, 21).date()

        # Mock the query result
        mock_query = self.mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = [
            MagicMock(vendedor_id=1, fecha=datetime(2025, 4, 21), cliente_id=1, nombre_cliente="Carlos Gomez", barrio="El Poblado", orden=1, tiempo_estimado="0.5", distancia="5 km")
        ]

        # Call the method
        rutas = self.rutas_visitas.obtener_rutas_por_vendedor_y_fecha(1, "2025-04-21")

        # Assertions
        self.mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        self.assertEqual(len(rutas), 1)
        self.assertEqual(rutas[0].nombre_cliente, "Carlos Gomez")

    @patch("infraestructura.repositorio.datetime")
    def test_obtener_rutas_por_vendedor_y_fecha_no_results(self, mock_datetime):
        # Mock the datetime.strptime to avoid actual parsing
        mock_datetime.strptime.return_value = datetime(2025, 4, 21)
        mock_datetime.date.return_value = datetime(2025, 4, 21).date()

        # Mock the query result
        mock_query = self.mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.all.return_value = []

        # Call the method
        rutas = self.rutas_visitas.obtener_rutas_por_vendedor_y_fecha(1, "2025-04-21")

        # Assertions
        self.mock_session.query.assert_called_once()
        mock_query.filter.assert_called_once()
        self.assertEqual(len(rutas), 0)

    @patch("infraestructura.repositorio.datetime")
    def test_obtener_rutas_por_vendedor_y_fecha_invalid_date(self, mock_datetime):
        # Mock the datetime.strptime to raise a ValueError
        mock_datetime.strptime.side_effect = ValueError("Invalid date format")

        # Call the method and assert exception
        with self.assertRaises(ValueError):
            self.rutas_visitas.obtener_rutas_por_vendedor_y_fecha(1, "invalid-date")

if __name__ == "__main__":
    unittest.main()