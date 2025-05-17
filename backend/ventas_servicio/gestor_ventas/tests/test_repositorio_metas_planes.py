import unittest
from unittest.mock import patch
from infraestructura.repositorio import RepositorioMetasPlanes

class TestRepositorioMetasPlanes(unittest.TestCase):

    def setUp(self):
        self.repo = RepositorioMetasPlanes(db_session=None)

    @patch('infraestructura.repositorio.random.randint')
    def test_generar_hora_aleatoria(self, mock_randint):
        mock_randint.return_value = 3600  # 1 hora
        hora = self.repo.generar_hora_aleatoria(inicio="09:00", fin="19:00")
        self.assertEqual(hora, "10:00")

    @patch('infraestructura.repositorio.random.choice')
    @patch('infraestructura.repositorio.RepositorioMetasPlanes.generar_hora_aleatoria')
    def test_generar_metas_ventas(self, mock_hora, mock_choice):
        mock_choice.side_effect = ["Llamar a", "cliente potencial"] * 10
        mock_hora.return_value = "10:00"

        metas = self.repo.generar_metas_ventas(n=3)

        self.assertEqual(len(metas), 3)
        for meta in metas:
            self.assertEqual(meta["meta"], "Llamar a cliente potencial")
            self.assertEqual(meta["tiempo"], "10:00")

    @patch('infraestructura.repositorio.random.choice')
    @patch('infraestructura.repositorio.RepositorioMetasPlanes.generar_hora_aleatoria')
    def test_generar_planes_ventas(self, mock_hora, mock_choice):
        mock_choice.side_effect = ["Lanzar campaña de", "ventas digitales"] * 10
        mock_hora.return_value = "15:30"

        planes = self.repo.generar_planes_ventas(n=2)

        self.assertEqual(len(planes), 2)
        for plan in planes:
            self.assertEqual(plan["plan"], "Lanzar campaña de ventas digitales")
            self.assertEqual(plan["tiempo"], "15:30")

if __name__ == '__main__':
    unittest.main()
