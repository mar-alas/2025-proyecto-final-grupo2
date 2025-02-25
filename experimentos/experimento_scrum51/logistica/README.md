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

- Envía una solicitud a la API del Servicio de Gestión de Entregas para iniciar una solicitud de entrega.

   ```
curl -X POST http://127.0.0.1:5001/api/entregas \
  -H "Content-Type: application/json" \
  -d '{
    "punto_inicio": "bodega_a",
    "destinos": ["cliente_a", "cliente_b", "cliente_c"]
  }'
   ```

- Por ahora no se tiene la base de datos con las coordenadas de los clientes, y las bodegas, por lo tanto se generan automaticamente.
- El resultado del request muestra las coordenadas del punto de inicio y cada destino en el orden de la ruta optima:

   ```
{"ruta_optima":[["bodega_a",[4.5963447980258145,-74.140915780082]],["cliente_c",[4.576081264259333,-74.06995657058636]],["cliente_b",[4.65139365472069,-74.07229591781795]],["cliente_a",[4.541978566073393,-73.98980769501749]]]}
   ```

## Arquitectura

Este proyecto sigue una arquitectura de microservicios, utilizando colas de comandos y eventos para facilitar la comunicación entre servicios. Cada servicio es responsable de una funcionalidad específica, promoviendo la separación de preocupaciones y la escalabilidad.