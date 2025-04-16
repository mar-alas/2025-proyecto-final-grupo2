import pytest
from unittest.mock import MagicMock
from dominio.get_all_products_service import GetAllProductsService

def test_ejecutar_retorna_lista_de_productos():
    # Arrange
    productos_esperados = [{"id": 1, "nombre": "Producto A"}, {"id": 2, "nombre": "Producto B"}]

    mock_repository = MagicMock()
    mock_repository.get_all.return_value = productos_esperados

    service = GetAllProductsService(mock_repository)

    # Act
    resultado = service.ejecutar()

    # Assert
    mock_repository.get_all.assert_called_once()
    assert resultado == productos_esperados


def test_ejecutar_lanza_runtime_error_si_get_all_falla():
    # Arrange
    mock_repository = MagicMock()
    mock_repository.get_all.side_effect = Exception("Falla en base de datos")

    service = GetAllProductsService(mock_repository)

    # Act & Assert
    with pytest.raises(RuntimeError) as excinfo:
        service.ejecutar()

    assert "Error al consultar productos" in str(excinfo.value)
