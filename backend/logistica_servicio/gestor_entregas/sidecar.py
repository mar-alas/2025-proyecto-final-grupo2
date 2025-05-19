import json
import time
import requests
import os
from flask import Flask, request, jsonify
import threading
import logging
import random
from infraestructura.repositorio_entrega_camion import RepositorioEntregasProgramadas

GENERADOR_RUTAS_HOSTNAME = os.getenv('GENERADOR_RUTAS_HOSTNAME', default="localhost")
GENERADOR_RUTAS_PORT = os.getenv('GENERADOR_RUTAS_PORT', default="3005")

MAIN_COMPONENT_URL = f"http://{GENERADOR_RUTAS_HOSTNAME}:{GENERADOR_RUTAS_PORT}/api/v1/logistica/generador_rutas_entrega"

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
recalculation_count = 0

def validate_route(ruta_data):
    # Dummy validator: returns True 99% of the time, False 1% of the time
    return random.random() < 0.99

def recalculate_route(entrada):
    response = requests.post(f"{MAIN_COMPONENT_URL}/generar_ruta", json=entrada)
    respopnse_data = response.json()
    ruta_json = json.dumps(respopnse_data)
    return ruta_json

def update_route_in_db(entrega_id, new_ruta):
    # Update the entrega using the repository's actualizar_entrega_programada method
    repo = RepositorioEntregasProgramadas()
    repo.actualizar_entrega_programada(entrega_id, {"ruta_calculada": str(new_ruta)})
    logging.info(f"Ruta programada de la entrega_id {entrega_id} se actualizo en la BD con la ruta {new_ruta}")

def process_entrega(entrega_id, informacion_ruta, ruta_calculada):
    global recalculation_count
    ruta_data = {
        "entrada": informacion_ruta,
        "ruta": ruta_calculada
    }
    if not validate_route(ruta_data):
        logging.info(f"La ruta con la entrega {entrega_id} no es la optima. Recalculando...")
        recalculation_count += 1
        new_ruta = recalculate_route(informacion_ruta)
        update_route_in_db(entrega_id, {"ruta_calculada": new_ruta})
        logging.info(f"La ruta de la {entrega_id} se recalculo y se actualizo en la BD.")
    else:
        logging.info(f"La ruta de la entrega_id {entrega_id} es la optima.")

@app.route('/api/v1/logistica/generador_rutas_entrega/sidecar/validate_entrega', methods=['POST'])
def validate_entrega():
    data = request.get_json()
    entrega_id = data.get("entrega_id")
    informacion_ruta = data.get("informacion_ruta")
    ruta_calculada = data.get("ruta_calculada")

    # Respond immediately
    threading.Thread(target=process_entrega, args=(entrega_id, informacion_ruta, ruta_calculada)).start()
    return jsonify({"status": "received"}), 200

@app.route('/api/v1/logistica/generador_rutas_entrega/sidecar/recalculation_count', methods=['GET'])
def get_recalculation_count():
    return jsonify({"recalculation_count": recalculation_count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
