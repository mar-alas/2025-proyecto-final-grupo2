import unittest
from unittest.mock import MagicMock, patch
# from ventas_servicio.gestor_ventas.repositorios.reporte_ventas_historico import RepositorioReporteVentasHistorico
from infraestructura.repositorio import RepositorioReporteVentasHistorico

class TestRepositorioReporteVentasHistorico(unittest.TestCase):

    @patch('infraestructura.repositorio.Session')
    def test_obtener_reporte_ventas_historico_retorna_datos_correctos(self, mock_session):
        # Simular filas que retornaría la base de datos
        mock_result = MagicMock()
        mock_result.fetchall.return_value = [
            # Simula valores del query, considerando que `mes` viene con espacios
            MagicMock(mes='January ', total_ventas=1000),
            MagicMock(mes='February ', total_ventas=2000),
        ]

        # Simula db_session.execute() para que retorne nuestro mock_result
        mock_db_session = MagicMock()
        mock_db_session.execute.return_value = mock_result
        mock_session.return_value = mock_db_session

        # Instancia del repositorio con el session mockeado
        repo = RepositorioReporteVentasHistorico(db_session=mock_db_session)

        # Mock del método fallback para evitar random en los tests
        repo.generar_reporte_historico_ventas_fallback = MagicMock(return_value=(50000, {mes: 0 for mes in [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]}))

        total, datos_ordenados, total_fallback, datos_fallback = repo.obtener_reporte_ventas_historico()

        self.assertEqual(total, 3000)
        self.assertEqual(datos_ordenados["january"], 1000)
        self.assertEqual(datos_ordenados["february"], 2000)
        self.assertEqual(total_fallback, 50000)
        self.assertEqual(datos_fallback["january"], 0)

    def test_generar_reporte_historico_ventas_fallback_devuelve_datos(self):
        repo = RepositorioReporteVentasHistorico()
        total, datos = repo.generar_reporte_historico_ventas_fallback()
        self.assertEqual(len(datos), 12)
        self.assertTrue(all(mes in datos for mes in [
            "january", "february", "march", "april", "may", "june",
            "july", "august", "september", "october", "november", "december"
        ]))
        self.assertGreater(total, 0)

if __name__ == '__main__':
    unittest.main()
