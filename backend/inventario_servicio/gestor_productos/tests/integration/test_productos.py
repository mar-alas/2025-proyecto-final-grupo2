from aplicacion import create_app

def test_obtener_productos():
    app = create_app()
    client = app.test_client()

    response = client.get('/api/v1/inventario/gestor_productos/productos')
    assert response.status_code == 200

    data = response.get_json()

    # Verificamos que se retorne una lista
    assert isinstance(data, list)
    assert len(data) == 5

    # Verificamos que los campos clave existan en el primer producto
    expected_keys = {
        "id", "nombre", "descripcion", "tiempo_entrega", "precio",
        "condiciones_almacenamiento", "fecha_vencimiento", "estado",
        "inventario_inicial", "imagenes_productos", "proveedor"
    }
    assert expected_keys.issubset(data[0].keys())
