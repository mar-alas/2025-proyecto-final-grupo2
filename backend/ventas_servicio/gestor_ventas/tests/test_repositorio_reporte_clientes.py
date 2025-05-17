import unittest
from unittest.mock import MagicMock
from infraestructura.repositorio import RepositorioReporteClientes

class TestRepositorioReporteClientes(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.repositorio = RepositorioReporteClientes(db_session=self.mock_session)

    def test_obtener_clientes_con_ventas_con_filtros(self):
        # Simulamos resultados de la consulta
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            MagicMock(cliente_id=1, direccion="Calle Falsa 123", codigo=101, promedio_ventas=150.0),
            MagicMock(cliente_id=2, direccion="Carrera Real 456", codigo=202, promedio_ventas=250.5),
        ]
        self.mock_session.execute.return_value = mock_result

        clientes = self.repositorio.obtener_clientes_con_ventas(vendedor_id=1, producto_id=202)

        self.mock_session.execute.assert_called_once()
        self.assertEqual(len(clientes), 2)
        self.assertEqual(clientes[0]["nombre"], "Cliente 1")
        self.assertEqual(clientes[0]["codigo"], "#101")
        self.assertEqual(clientes[1]["promedio_ventas"], 250.5)

    def test_obtener_clientes_con_ventas_sin_resultados(self):
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        self.mock_session.execute.return_value = mock_result

        clientes = self.repositorio.obtener_clientes_con_ventas(vendedor_id=5)

        self.mock_session.execute.assert_called_once()
        self.assertEqual(clientes, [])

    def test_obtener_clientes_con_ventas_exception(self):
        self.mock_session.execute.side_effect = Exception("DB error")

        with self.assertRaises(Exception) as context:
            self.repositorio.obtener_clientes_con_ventas(producto_id=999)

        self.assertIn("DB error", str(context.exception))

if __name__ == "__main__":
    unittest.main()
