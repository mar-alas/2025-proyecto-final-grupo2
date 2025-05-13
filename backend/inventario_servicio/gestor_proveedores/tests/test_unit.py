def test_hola_mundo():
    mensaje = "Hola mundo"
    assert mensaje == "Hola mundo"

import unittest

class TestHolaMundo(unittest.TestCase):
    def test_saludo(self):
        saludo = "Hola, mundo"
        self.assertEqual(saludo, "Hola, mundo")
