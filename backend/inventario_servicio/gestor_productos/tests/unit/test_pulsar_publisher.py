import pytest
from unittest.mock import patch, MagicMock
from infraestructura.pulsar.publisher import PulsarPublisher


@patch("infraestructura.pulsar.publisher.pulsar.Client")
def test_publicar_mensaje_exitosamente(mock_pulsar_client):
    # Arrange
    mock_producer = MagicMock()
    mock_client_instance = MagicMock()
    mock_client_instance.create_producer.return_value = mock_producer
    mock_pulsar_client.return_value = mock_client_instance

    publisher = PulsarPublisher()
    topico = "productos"
    mensaje = {"evento": "ProductoRegistrado", "producto": {"nombre": "Producto Test"}}

    # Act
    publisher.publicar_mensaje(topico, mensaje)

    # Assert
    mock_client_instance.create_producer.assert_called_once_with(topico)
    mock_producer.send.assert_called_once_with(b'{"evento": "ProductoRegistrado", "producto": {"nombre": "Producto Test"}}')
    # mock_client_instance.close.assert_called_once()


@patch("infraestructura.pulsar.publisher.pulsar.Client")
def test_publicar_mensaje_con_error_no_cierra_cliente(mock_pulsar_client, caplog):
    # Arrange
    mock_client_instance = MagicMock()
    mock_client_instance.create_producer.side_effect = Exception("Fallo de conexión")
    mock_pulsar_client.return_value = mock_client_instance

    publisher = PulsarPublisher()
    topico = "productos"
    mensaje = {"evento": "ProductoRegistrado"}

    # Act
    with caplog.at_level("INFO"):
        publisher.publicar_mensaje(topico, mensaje)

    # Assert
    assert any("Error enviando mensaje a productos: Fallo de conexión" in msg for msg in caplog.messages)
    mock_client_instance.close.assert_not_called()
