# Experimento Scrum 30 Corrección rápida de errores en cálculo de ruta 

## Como correr el experimento en local

En este experimento se probaron los microservicios de: 1) calculo de rutas y 2) monitoreo y validación de rutas. Para correr el experimento primero levantar los contenedores con el comando:

```bash
docker-compose up
```

Este comando va a levantar los dos microservicios anteriormente mencionados mas un contenedor de postgres y un contenedor de Apache Pulsar. Se debe esperar a que los 4 contenedores estén en verde.

Una vez los contendedores estén corriendo el experimento se puede correr corriendo el siguiente script en la raiz del proyecto.

```bash
python3 correr_experimento.py
```
Los resultados del experimento se guardan en el archivo "rutas_calculadas.xlsx" en la raiz del proyecto despues de correr este script.

## Como correr el experimento para cloud

Cree su entorno virtual
```bash
python3 -m venv venv
```

Active el entorno virtual
```bash
source venv/bin/activate
```

Instale las dependencias necesarias
```bash
pip install -r requirements.txt
```

Ejecute:
```bash

```

## Descripción del experimento

El experimento consiste en simular el comportamiento del cálculo de rutas. En este caso lo simulamos como un proceso que ordena lista de numeros enteros de forma ascendente.

Cuando se realiza el calculo se emite un evento e pulsar con los datos de la ruta creada.

El algoritmo falla con una probabilidad del 50% y en dichos casos el monitor revisa y recalcula los resultados.

Este experimento se corre n veces según lo especificado en el script del experimento. 

## Configuraciones GCP

### Crear cluster en GKE
```
sudo gcloud container clusters create experimento-scrum30-v1-cluster \
  --num-nodes=2 \
  --zone=us-central1-a
```

### Conectarme al cluster
```
sudo gcloud container clusters get-credentials experimento-scrum30-v1-cluster --zone us-central1-a
```

### Desplegar los contenedores.

#### Base de datos
```
sudo kubectl apply -f rutas-db-container-deployment.yaml
sudo kubectl apply -f rutas-db-container-service.yaml
```

#### Pulsar
```
sudo kubectl apply -f pulsar-container-deployment.yaml
sudo kubectl apply -f pulsar-container-service.yaml
```

#### microservicio calculo ruta entrega

##### Build
```
sudo docker build -t microservicio_calculo_ruta_entrega:latest .
```

##### Upload
sudo docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/microservicio_calculo_ruta_entrega:latest .

##### Push
sudo docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/microservicio_calculo_ruta_entrega:latest


```
sudo kubectl apply -f microservicio-calculo-ruta-entrega-container-deployment.yaml
sudo kubectl apply -f microservicio_monitor_calculo_ruta_entrega_container-service.yaml
```

#### Componente MONITOR calculo ruta entrega

##### Build
```
sudo docker build -t microservicio-monitor-calculo-ruta-entrega:latest .
```

##### Upload
sudo docker buildx build --platform linux/amd64 -t us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/microservicio-monitor-calculo-ruta-entrega:latest .

##### Push
sudo docker push us-central1-docker.pkg.dev/appnomonoliticas-452202/repositorio-imagenes-docker/microservicio-monitor-calculo-ruta-entrega:latest


```
sudo kubectl apply -f microservicio-monitor-calculo-ruta-entrega-container-deployment.yaml
sudo kubectl apply -f microservicio_monitor_calculo_ruta_entrega_container-service.yaml
```