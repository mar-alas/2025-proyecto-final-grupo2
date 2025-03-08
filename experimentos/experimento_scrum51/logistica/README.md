Este experimento implementa una arquitectura de microservicios con cola de comandos y de eventos para gestionar solicitudes de entrega y optimizar rutas de entrega. Consta de dos componentes principales: el Servicio de Gestión de Entregas y el Servicio de Optimización de Rutas.

## Estructura del Proyecto

```
├── README.md
├── api_logistica
│   ├── Dockerfile
│   ├── api.py
│   └── requirements.txt
├── docker-compose.yml
├── gestor_entregas
│   ├── Dockerfile
│   ├── __init__.py
│   ├── generador_rutas.py
│   ├── optimizador_rutas
│   │   ├── __init__.py
│   │   ├── algoritmo
│   │   │   └── algoritmo_calculo_ruta.py
│   │   └── optimizador.py
│   └── requirements.txt
├── requirements.txt
└── test_request.sh
```

## Componentes

### Servicio de Gestión de Entregas

- **API**: Maneja las solicitudes entrantes para la gestión de entregas, se encarga de poner la solicitud en una cola de comandos, y espera la respuesta de la cola de eventos.
- **Cola de Comandos**: Gestiona la cola para procesar solicitudes de entrega.
- **Cola de Eventos**: Maneja eventos relacionados con actualizaciones del estado de las entregas.
- **Generador de Rutas**: Se suscribe al topico de la lista de comandos para llamar al optimizador de rutas, y envia el evento a la cola de eventos una vez se calcula la ruta. Aca se generan ubicaciones aleatoreas en un rango de 10km de una ubicacion inicial en Bogota

### Servicio de Optimización de Rutas

- **Optimizador**: Implementa la lógica para optimizar las rutas de entrega.
- **Algoritmo de Rutas**: Contiene el algoritmo utilizado para calcular la mejor ruta basada en los puntos proporcionados.

## Instrucciones de Configuración

1. Inicia los servicios usando Docker Compose:
   ```
   docker-compose up
   ```

2. Para probar la escalabilidad del calculo de rutas se usa el siguiente comando:
   ```
   docker-compose up --scale gestor_entregas=2
   ```

## Uso
### Ejemplo de Uso

1. Envía una solicitud a la API del Servicio de Gestión de Entregas para iniciar una solicitud de entrega:

   ```sh
   curl -X POST http://127.0.0.1:5001/api/entregas \
     -H "Content-Type: application/json" \
     -d '{
       "punto_inicio": "bodega_a",
       "destinos": ["cliente_a", "cliente_b", "cliente_c"]
     }'
   ```

2. Actualmente, no se dispone de una base de datos con las coordenadas de los clientes y las bodegas, por lo que estas se generan automáticamente.

3. El resultado de la solicitud muestra las coordenadas del punto de inicio y cada destino en el orden de la ruta óptima:

   ```json
   {
     "ruta_optima": [
       ["bodega_a", [4.5963447980258145, -74.140915780082]],
       ["cliente_c", [4.576081264259333, -74.06995657058636]],
       ["cliente_b", [4.65139365472069, -74.07229591781795]],
       ["cliente_a", [4.541978566073393, -73.98980769501749]]
     ]
   }
   ```

## Arquitectura

Este proyecto sigue una arquitectura de microservicios, utilizando colas de comandos y eventos para facilitar la comunicación entre servicios. Cada servicio es responsable de una funcionalidad específica, promoviendo la separación de preocupaciones y la escalabilidad.




### Crear el cluster
```
sudo gcloud container clusters create experimento-scrum51-v1-cluster \
  --num-nodes=2 \
  --zone=us-central1-a
```

### Conectarme al cluster
```
sudo gcloud container clusters get-credentials experimento-scrum51-v1-cluster --zone us-central1-a
```

## Desplegar los contenedores.
### pulsar
```
sudo kubectl apply -f pulsar-deployment.yaml
sudo kubectl apply -f pulsar-service.yaml
```

### api logistica
```
sudo kubectl apply -f api-logistica-deployment.yaml
sudo kubectl apply -f api_logistica-service.yaml
```

### gestor entregas
```
sudo kubectl apply -f gestor-entregas-deployment.yaml
sudo kubectl apply -f gestor_entregas-service.yaml
```

## Ver los pods corriendo
```
sudo kubectl get pods
```

## Ver los services corriendo
```
sudo kubectl get services
```

## ver logs de pods
```
sudo kubectl logs -f nombre-del-pod
```


## Cargue de imagenes Docker (se hace una vez pro proyecto)
sudo gcloud services enable artifactregistry.googleapis.com

sudo gcloud artifacts repositories create repositorio-imagenes-docker \
    --repository-format=docker \
    --location=us-central1 \
    --description="Repositorio de imágenes Docker"

## Construir imagen (win)
sudo docker build -t api-logistica:latest .

## construior la imagen (Mac)
sudo docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/api-logistica:latest .

sudo docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/gestor-entregas:latest .



## Validar si creó la imagen
sudo docker images | grep api-logistica
sudo docker images | grep gestor-entregas

## Etiquetar la imagen 
sudo docker tag api-logistica:latest gcr.io/appnomonoliticas-452202/api-logistica:latest

sudo docker tag api-logistica:latest us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/api-logistica:latest

sudo docker tag gestor-entregas:latest us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/gestor-entregas:latest

## Autenticación en el registro de contenedores.
gcloud auth configure-docker us-central1-docker.pkg.dev

## Subir imagen (win)
sudo docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/api-logistica:latest

## subir la imagen (Mac)
sudo docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/api-logistica:latest

sudo docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/gestor-entregas:latest


## -------------------------------

### debo crear una cuenta de servicio para leer las imagenes
sudo gcloud iam service-accounts create k8s-container-pull \
    --display-name "Kubernetes Image Pull Service Account"

### Darle permisos a la cuneta
sudo gcloud projects add-iam-policy-binding appnomonoliticas-452202 \
    --member=serviceAccount:k8s-container-pull@appnomonoliticas-452202.iam.gserviceaccount.com \
    --role=roles/artifactregistry.reader

### Generar la key
sudo gcloud iam service-accounts keys create keyfile.json \
    --iam-account=k8s-container-pull@appnomonoliticas-452202.iam.gserviceaccount.com


## crear secreto para qeu GKE acceso a las imagenes
Nota: el archivo keyfile.json debe tener todos los permisos. 
```
sudo kubectl create secret docker-registry gcr-secret \
    --docker-server=us-central1-docker.pkg.dev \
    --docker-username=_json_key \
    --docker-password="$(cat keyfile.json)" \
    --docker-email=k8s-container-pull@appnomonoliticas-452202.iam.gserviceaccount.com
```


# creacion del ingress

## Habilitar Ingress en GCP
sudo gcloud services enable container.googleapis.com

sudo gcloud services enable compute.googleapis.com