import unittest
from unittest.mock import patch
from optimizador_rutas.optimizador import Optimizador

class TestOptimizador(unittest.TestCase):

    @patch('optimizador_rutas.optimizador.calcular_mejor_ruta')
    def test_optimizar_ruta(self, mock_calcular_mejor_ruta):
        # Arrange
        mock_calcular_mejor_ruta.return_value = ["cliente_a", "cliente_b", "cliente_c"]
        punto_inicio = "bodega_a"
        destinos = ["cliente_a", "cliente_b", "cliente_c"]
        optimizador = Optimizador(punto_inicio, destinos)

        # Act
        resultado = optimizador.optimizar_ruta()

        # Assert
        self.assertEqual(resultado, ["cliente_a", "cliente_b", "cliente_c"])
        mock_calcular_mejor_ruta.assert_called_once_with(punto_inicio, destinos)

if __name__ == '__main__':
    unittest.main()