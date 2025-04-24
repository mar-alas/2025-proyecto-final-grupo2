import pytest
from infraestructura.modelos import Stock

def test_stock_model_attributes():
    # Crear una instancia de Stock
    stock = Stock(producto_id=123, inventario=50)

    # Verificar que los atributos están correctamente asignados
    assert stock.producto_id == 123
    assert stock.inventario == 50
    assert stock.id is None  # Porque aún no ha sido asignado por la BD
