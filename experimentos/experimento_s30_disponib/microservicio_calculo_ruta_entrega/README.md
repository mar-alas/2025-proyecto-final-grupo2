# Códigos de utilidad

## enviar calculo de ruta
```bash
curl -X POST http://localhost:5000/calcular-ruta -H "Content-Type: application/json" -d '{"ruta_sin_calcular": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]}'
```

## correr pulsar de forma independiente

```bash
docker run -d --rm --name pulsar-container --network=network_experiment -p 6650:6650 -p 8080:8080 apachepulsar/pulsar:latest bin/pulsar standalone
```

## correr contenedor postgres:

```bash
docker run --rm --name rutas-db-container --network=network_experiment -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=rutas-db -p 5432:5432 -d postgres
```

## ver resultados en tabla de postgres
```bash
docker exec rutas-db-container psql -U admin -d rutas-db -c "SELECT * FROM rutas_calculadas;"
```


## ver topicos pulsar

curl -X GET 'http://localhost:8080/admin/v2/persistent/public/default'

## ver subscripciones topico

curl -X GET 'http://localhost:8080/admin/v2/persistent/public/default/rutas/subscriptions'

## borrar topico

curl -X DELETE 'http://localhost:8080/admin/v2/persistent/public/default/rutas'

## ver mensaje con id

curl -X GET 'http://localhost:8080/admin/v2/persistent/public/default/rutas/subscription/mysub/position/1'

## ver ultimo mensaje

curl -X GET 'http://localhost:8080/admin/v2/persistent/public/default/rutas/lastMessageId'


