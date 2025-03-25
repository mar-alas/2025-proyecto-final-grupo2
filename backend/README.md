## Ejecucion del Backend

Para iniciar todos los componentes del backen en local
```sh
docker-compose up
```


Detener los componentes del backend en local
```sh
docker-compose down -v
```

Construir de nuevo los componentes del backend en local
```sh
docker-compose up --build
```


## Correr Pruebas

Establecer la variable de ambiente `PYTHONPATH`:
```sh
export PYTHONPATH=$PWD/seedwork_compartido:$PWD/inventario_servicio/gestor_productos:$PWD/compras_servicio/gestor_compras
```

Correr las pruebas:
```sh
python -m unittest discover -s compras_servicio/gestor_compras
python -m unittest discover -s inventario_servicio/gestor_productos
```

## Probar los Endpoints

Realizar un ping a cada componente

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

## Conectarse al proyecto GCP y cluster

Ubiquese en la terminal en la ruta: _scripts/gke/_

### 1. Conectese al proyecto GCP.

Ejecute:
```bash
bash conectarse_a_proyecto_gcp.sh
```
y seleccione el proyecto: proyecto-final-2-454403

### 2. Crear el cluster (si no existe)
```bash
bash crear_cluster_produccion.sh
```

### Conectarme al cluster
```bash
bash conectarse_al_cluster.sh
```

### Generar k8s
```bash
bash generar_archivos_k8s.sh
```

### 3. Construir imagenes docker

Pre-requisito: Debe existir el repositorio de artifact registry
Si no esiste, creeelo:

```bash
bash crear_repositorio_imagenes_en_gcp.sh
```

Generar imagenes:
```bash
bash construir_todas_las_imagenes.sh
```

Subir imagenes a GCP:
```bash
bash subir_imagenes_a_gcp.sh
```

### 3. Desplegar contenedores en Kubernetes
Subir imagenes a GCP:
```bash
bash desplegar_imagenes_en_gke.sh
```