
from optimizador_rutas.optimizador import Optimizador
import random
import logging
import pulsar
from pulsar import KeySharedPolicy
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_puntos_geograficos(ubicacion):
        # TBD obtener la ubicacion del cliente de la BD
        # obtener los puntos geograficos de la ubicacion
        # por ahora vamos a devolver una lista de puntos geograficos aleatorios
        # todos dentro de un radio de 10 km de Bogota
        logger.info('Generando puntos geograficos aleatorios para la ubicacion %s', ubicacion)
        ubicacion = (4.6097100, -74.0817500)
        return (ubicacion[0] + random.uniform(-0.1, 0.1), ubicacion[1] + random.uniform(-0.1, 0.1))


def generar_ruta():
    if 'PULSAR_SERVICE_URL' not in os.environ:
        client = pulsar.Client('pulsar://localhost:6650')
    else:
        client = pulsar.Client(os.environ['PULSAR_SERVICE_URL'])
    consumer = client.subscribe(
        topic=os.environ['TOPIC_COMANDOS'],
        subscription_name='my-subscription',
        consumer_type=pulsar.ConsumerType.Shared)
    producer = client.create_producer(os.environ['TOPIC_EVENTOS'])
    while True:
        mensaje = consumer.receive()
        data = json.loads(mensaje.data().decode('utf-8'))
        punto_inicio = data['punto_inicio']
        destinos = data['destinos']
        consumer.acknowledge(mensaje)
        punto_geografico_inicio = get_puntos_geograficos(punto_inicio)
        destinos_geograficos = [get_puntos_geograficos(destino) for destino in destinos]
        # guarde los destinos con el nombre como key y los puntos geograficos como value
        punto_inicio_dict = {punto_inicio: punto_geografico_inicio}
        destinos_dict = {destino: punto_geografico for destino, punto_geografico in zip(destinos, destinos_geograficos)}

        logger.info('Generando ruta optima para el punto de inicio %s y los destinos %s', punto_inicio, destinos)
        mejor_ruta = Optimizador(punto_geografico_inicio, destinos_geograficos).optimizar_ruta()
        logger.info('La mejor ruta es %s', mejor_ruta)
        logger.info('Puntos de inicio %s', punto_inicio_dict)
        logger.info('Destinos %s', destinos_dict)
        mejor_ruta_con_nombres = []
        for punto in mejor_ruta:
            for nombre, punto_geografico in punto_inicio_dict.items():
                if punto == punto_geografico:
                    mejor_ruta_con_nombres.append((nombre, punto_geografico))
            for nombre, punto_geografico in destinos_dict.items():
                if punto == punto_geografico:
                    mejor_ruta_con_nombres.append((nombre, punto_geografico))
        logger.info('mejor_ruta_con_nombres %s', mejor_ruta_con_nombres)
        logger.info('Puntos geograficos de la mejor ruta %s', [punto for punto in mejor_ruta])
        producer.send(json.dumps(mejor_ruta_con_nombres).encode('utf-8'))
  

if __name__ == '__main__':
    generar_ruta()

       