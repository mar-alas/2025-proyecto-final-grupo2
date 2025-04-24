import unittest
from dominio.event_publisher import EventPublisher


class MockPublisher(EventPublisher):
    def __init__(self):
        self.publicados = []

    def publicar_mensaje(self, topico: str, mensaje: dict) -> None:
        self.publicados.append((topico, mensaje))


class TestEventPublisher(unittest.TestCase):
    def test_publicar_mensaje_is_called_in_concrete_subclass(self):
        publisher = MockPublisher()

        topico = "producto.creado"
        mensaje = {"producto_id": 1}

        publisher.publicar_mensaje(topico, mensaje)

        self.assertEqual(publisher.publicados, [(topico, mensaje)])

    def test_mock_is_subclass_of_event_publisher(self):
        self.assertTrue(issubclass(MockPublisher, EventPublisher))

    
    def test_event_publisher_definition(self):
        from dominio.event_publisher import EventPublisher
        assert EventPublisher is not None


class TestConcretePublisher(unittest.TestCase):
    def test_publicar_mensaje(self):
        publisher = MockPublisher()
        topico = "producto.creado"
        mensaje = {"producto_id": 1}

        publisher.publicar_mensaje(topico, mensaje)

        self.assertEqual(publisher.publicados, [(topico, mensaje)])


class TestEventPublisher(unittest.TestCase):
    def test_publicar_mensaje_no_implementado(self):
        with self.assertRaises(TypeError):
            publisher = EventPublisher()  # No se puede instanciar directamente
            publisher.publicar_mensaje("topico", {"mensaje": "prueba"})


class TestMockPublisher(unittest.TestCase):
    def test_publicar_mensaje_is_called_in_concrete_subclass(self):
        publisher = MockPublisher()

        topico = "producto.creado"
        mensaje = {"producto_id": 1}

        publisher.publicar_mensaje(topico, mensaje)

        self.assertEqual(publisher.publicados, [(topico, mensaje)])

    def test_publicar_mensaje_no_implementado(self):
        with self.assertRaises(TypeError):
            publisher = EventPublisher()
            publisher.publicar_mensaje("topico", {"mensaje": "prueba"})