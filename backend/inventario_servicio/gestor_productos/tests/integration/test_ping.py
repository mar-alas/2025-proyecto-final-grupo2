from aplicacion import create_app

def test_ping():
    app = create_app()
    client = app.test_client()

    response = client.get('/api/v1/inventario/gestor_productos/ping')
    
    assert response.status_code == 200
    assert response.json == {"message": "pong"}