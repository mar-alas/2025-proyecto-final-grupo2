from infraestructura.get_all_products_repository import ProductoRepository

def test_obtener_todos_retorna_lista_con_producto():
    repo = ProductoRepository()
    productos = repo.obtener_todos()

    assert isinstance(productos, list)
    assert len(productos) > 0

    producto = productos[0]
    assert "id" in producto
    assert "nombre" in producto
