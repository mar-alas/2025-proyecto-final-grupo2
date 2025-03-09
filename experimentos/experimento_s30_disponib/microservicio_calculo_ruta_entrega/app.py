from datetime import datetime
from flask import Flask, request, jsonify
import random
from pulsar import Client
from models import Session, Ruta,RutaSchema
import json
import logging

# TODO: Convertir BASE_PULSAR_URL a env var.
BASE_PULSAR_URL = "pulsar://pulsar-container.default.svc.cluster.local:6650"
pulsar_client = Client(BASE_PULSAR_URL)

ruta_schema = RutaSchema()

def publish_message(ruta_json:str):

    producer = pulsar_client.create_producer('persistent://public/default/rutas')
    producer.send(ruta_json.encode('utf-8'))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': "UP"}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': "Pong"}), 200

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


@app.route('/rutas', methods=['DELETE'])
def delete_routes():
    logging.info("Called API: delete_routes() Path: [/rutas] Method: DELETE")
    try:
        session = Session()
        try:
            session.query(Ruta).delete()
            session.commit()
        except Exception as e:
            logging.warning("Error al eliminar los registros de la tabla Ruta. Se hara rollback. Mensaje: "+str(e))
            session.rollback()
        finally:
            logging.info("Cerrando sesion de la conexion con la BD.")
            session.close()

        return jsonify({
            "message": "Todos los registros de la tabla [Ruta] fueron eliminadas.",
            "sucess": True
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/rutas', methods=['GET'])
def get_all_routes():
    logging.info("Called API: get_all_routes() Path: [/rutas] Method: GET")
    try:
        session = Session()
        try:
            rutas = session.query(Ruta).all()
            ruta_schema = RutaSchema(many=True)
            session.close()
            logging.info(f"Se encontraron {len(rutas)} registros de rutas en la base de datos.")
            return jsonify({
                "message": "Todos los registros de la tabla [Ruta] fueron consultados.",
                "sucess": True,
                "data": ruta_schema.dump(rutas)
            }), 200
        except Exception as e:
            logging.warning("Error al consultar todos los registros de la tabla Ruta. Mensaje: "+str(e))
            return jsonify({
                'error': str(e),
                'success': False,
                "data": None
            }), 500
        finally:
            logging.info("Cerrando sesion de la conexion con la BD.")
            session.close()
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
