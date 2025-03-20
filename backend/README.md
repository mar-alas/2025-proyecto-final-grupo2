## Backend Execution

To start the backend, run:
```sh
docker-compose up
```

## Running Tests

Set the `PYTHONPATH` environment variable:
```sh
export PYTHONPATH=$PWD/seedwork_compartido:$PWD/inventario_servicio/gestor_productos:$PWD/compras_servicio/gestor_compras
```

Run the tests:
```sh
python -m unittest discover -s compras_servicio/gestor_compras
python -m unittest discover -s inventario_servicio/gestor_productos
```

## Testing Endpoints

Ping the endpoints to check if they are working:

### Compras
```sh
curl http://127.0.0.1:3000/api/v1/compras/gestor_compras/ping
```
Response:
```json
{
    "message": "pong"
}
```

### Inventario
```sh
curl http://127.0.0.1:3001/api/v1/inventario/gestor_productos/ping
curl http://127.0.0.1:3002/api/v1/inventario/gestor_stock/ping
curl http://127.0.0.1:3003/api/v1/inventario/gestor_proveedores/ping
```

### Logistica
```sh
curl http://127.0.0.1:3004/api/v1/logistica/generador_reportes/ping
curl http://127.0.0.1:3005/api/v1/logistica/generador_rutas_entrega/ping
curl http://127.0.0.1:3006/api/v1/logistica/gestor_entregas/ping
```

### Ventas
```sh
curl http://127.0.0.1:3007/api/v1/ventas/generador_reportes/ping
curl http://127.0.0.1:3008/api/v1/ventas/gestor_ventas/ping
curl http://127.0.0.1:3009/api/v1/ventas/procesador_pedidos/ping
curl http://127.0.0.1:3010/api/v1/ventas/procesador_video/ping
```

### Seguridad
```sh
curl http://127.0.0.1:3011/api/v1/seguridad/gestor_usuarios/ping
```