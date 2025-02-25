# Experimento Scrum 30 Corrección rápida de errores en cálculo de ruta 

## Como correr el experimento

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

## Descripción del experimento

El experimento consiste en simular el comportamiento del cálculo de rutas. En este caso lo simulamos como un proceso que ordena lista de numeros enteros de forma ascendente.

Cuando se realiza el calculo se emite un evento e pulsar con los datos de la ruta creada.

El algoritmo falla con una probabilidad del 50% y en dichos casos el monitor revisa y recalcula los resultados.

Este experimento se corre n veces según lo especificado en el script del experimento. 

