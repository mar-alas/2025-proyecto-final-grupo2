import unittest
from dominio.optimizaciones import optimizar_ruta

class Visita:
    def __init__(self, nombre, distancia):
        self.nombre = nombre
        self.distancia = distancia

class TestOptimizarRuta(unittest.TestCase):
    def test_optimizar_ruta(self):
        # Arrange
        visitas = [
            Visita("cliente_a", 10),
            Visita("cliente_b", 5),
            Visita("cliente_c", 15)
        ]

        # Act
        resultado = optimizar_ruta(visitas)

        # Assert
        self.assertEqual([v.nombre for v in resultado], ["cliente_b", "cliente_a", "cliente_c"])

if __name__ == "__main__":
    unittest.main()