import pytest
from dominio.event_publisher import EventPublisher


def test_event_publisher_es_abstracta():
    with pytest.raises(TypeError) as exc_info:
        EventPublisher()
    assert "Can't instantiate abstract class" in str(exc_info.value)


class EventPublisherDummy(EventPublisher):
    def __init__(self):
        self.mensajes_publicados = []

    def publicar_mensaje(self, topico: str, mensaje: dict) -> None:
        self.mensajes_publicados.append((topico, mensaje))


def test_event_publisher_subclase_implementa_correctamente():
    dummy = EventPublisherDummy()
    dummy.publicar_mensaje("mi-topico", {"key": "value"})

    assert len(dummy.mensajes_publicados) == 1
    topico, mensaje = dummy.mensajes_publicados[0]
    assert topico == "mi-topico"
    assert mensaje == {"key": "value"}
