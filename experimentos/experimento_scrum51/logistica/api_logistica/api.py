from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.INFO)
import pulsar
import os
import json

app = Flask(__name__)

@app.before_request
def log_request_info():
    logging.info('Request Headers: %s', request.headers)
    logging.info('Request Body: %s', request.get_data())

@app.route('/api/entregas', methods=['POST'])
def receive_request():
    logging.info('Request received')
    data = request.json
    punto_inicio = data.get('punto_inicio')
    destinos = data.get('destinos')

    if not punto_inicio or not destinos:
        return jsonify({'error': 'Invalid input'}), 400

    logging.info('Enviar el comando al topico de comandos')
    client = pulsar.Client(os.environ['PULSAR_SERVICE_URL'])
    producer = client.create_producer(os.environ['TOPIC_COMANDOS'])
    message = json.dumps({'punto_inicio': punto_inicio, 'destinos': destinos}).encode('utf-8')
    producer.send(message)
    mejor_ruta = None
    subscription_name = f'my-subscription'
    consumer = client.subscribe(
        os.environ['TOPIC_EVENTOS'],
        subscription_name=subscription_name,
        consumer_type=pulsar.ConsumerType.Shared
    )
    while True:
        mensaje = consumer.receive()
        mejor_ruta = json.loads(mensaje.data().decode('utf-8'))
        consumer.acknowledge(mensaje)
        break
    consumer.close()
    return jsonify({'ruta_optima': mejor_ruta}), 200

if __name__ == '__main__':
    app.run(debug=True)