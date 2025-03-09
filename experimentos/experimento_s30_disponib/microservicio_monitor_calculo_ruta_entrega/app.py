from datetime import datetime
import pulsar
from models import Session, Ruta,RutaSchema
import json
import time

# Connect to Pulsar
# TODO: Poner como variable de entorno.
BASE_PULSAR_URL = "pulsar://pulsar-container.default.svc.cluster.local:6650"
client = pulsar.Client(BASE_PULSAR_URL)

# Create a consumer
consumer = client.subscribe('persistent://public/default/rutas', subscription_name='mysub4')

#Data base session
session = Session()

# check and correct route
def check_and_correct_route(ruta_x_revisar:dict):
    #wait 1 second
    #time.sleep(1)

    # Sort the numbers
    ruta_x_revisar=Ruta(**ruta_x_revisar)
    ruta_sin_calcular=ruta_x_revisar.dar_ruta_sin_calcular()
    ruta_calculada=ruta_x_revisar.dar_ruta_calculada()
    ruta_revision = sorted(ruta_sin_calcular)
    
    if ruta_revision != ruta_calculada:
        ruta_x_corregir= session.query(Ruta).filter(Ruta.id==ruta_x_revisar.id).first()
        ruta_x_corregir.ruta_calculada = str(ruta_revision)
        ruta_x_corregir.calculo_correcto = True
        ruta_x_corregir.fecha_actualizacion = datetime.now()
        ruta_x_corregir.tuvo_correccion = True
        session.commit()
        print(f'la ruta con id {ruta_x_revisar.id} fue corregida')
    print(f'la ruta con id {ruta_x_revisar.id} fue revisada')
    
# Receive messages
try:
    while True:
        msg = consumer.receive()
        ruta_json_str = msg.data().decode('utf-8')
        #ruta_json_str='{"fecha_creacion": "2025-02-25T15:47:37.344435", "ruta_calculada": "[1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]", "fecha_actualizacion": "2025-02-25T15:47:37.344441", "calculo_correcto": true, "id": 29, "ruta_sin_calcular": "[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]"}'
        print(f"Received message: {ruta_json_str}")
        print(f"tipo: {type(ruta_json_str)}")
        consumer.acknowledge(msg)

        ruta_dict=json.loads(ruta_json_str)

        check_and_correct_route(ruta_dict)
    
except KeyboardInterrupt:
    print("Stopping consumer...")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the client
    client.close()
    session.close()