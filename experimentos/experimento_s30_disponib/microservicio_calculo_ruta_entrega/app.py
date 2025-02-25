from datetime import datetime
from flask import Flask, request, jsonify
import random
from pulsar import Client
from models import Session, Ruta,RutaSchema
import json

pulsar_client = Client('pulsar://pulsar-container:6650')

ruta_schema = RutaSchema()

def publish_message(ruta_json:str):

    producer = pulsar_client.create_producer('persistent://public/default/rutas')
    producer.send(ruta_json.encode('utf-8'))

app = Flask(__name__)

@app.route('/')
def index():
    return 'pong'

@app.route('/calcular-ruta', methods=['POST'])
def calcular_ruta():
    try:
        # Ejemplo data: {"ruta_sin_calcular": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]}
        data = request.get_json()
        if not data or 'ruta_sin_calcular' not in data:
            return jsonify({'error': 'No ruta_sin_calcular provided'}), 400

        ruta_sin_calcular = data['ruta_sin_calcular']
        
        # Validate input
        if not all(isinstance(x, int) for x in ruta_sin_calcular):
            return jsonify({'error': 'All elements must be integers'}), 400

        # Sort the numbers
        ruta_calculada = sorted(ruta_sin_calcular)
        
        #fail variable with probability 50%
        calculo_correcto = random.random() > 0.5
        
        if not calculo_correcto:
            #scramble the sorted list in case of failure
            random.shuffle(ruta_calculada)


        # Store operation in database
        session = Session()

        current_time= datetime.now()
        ruta = Ruta(
            ruta_sin_calcular=json.dumps(ruta_sin_calcular),
            ruta_calculada=json.dumps(ruta_calculada),
            calculo_correcto=calculo_correcto,
            fecha_creacion=current_time,
            fecha_actualizacion=current_time
        )

        

        session.add(ruta)
        session.commit()

        ruta_json = ruta_schema.dumps(ruta)
        print(f'ruta: {ruta_json}')
        
        session.close()

        publish_message(ruta_json)

        return jsonify({
            'ruta_sin_calcular': ruta_sin_calcular,
            'ruta_calculada': ruta_calculada,
            'calculo_correcto': calculo_correcto
        })

        

    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
