from dominio.get_all_products_service import GetAllProductsService
from unittest.mock import Mock
import pytest

def test_servicio_obtener_productos_exitoso():
    productos_falsos = [
        {"id": 1, "nombre": "Producto 1"},
        {"id": 2, "nombre": "Producto 2"},
    ]

    mock_repo = Mock()
    mock_repo.obtener_todos.return_value = productos_falsos

    servicio = GetAllProductsService(mock_repo)
    resultado = servicio.ejecutar()

    assert resultado == productos_falsos
    mock_repo.obtener_todos.assert_called_once()


def test_servicio_obtener_productos_error():
    mock_repo = Mock()
    mock_repo.obtener_todos.side_effect = Exception("Falla intencional")

    servicio = GetAllProductsService(mock_repo)

    with pytest.raises(RuntimeError) as excinfo:
        servicio.ejecutar()

    assert "Error al consultar productos" in str(excinfo.value)
