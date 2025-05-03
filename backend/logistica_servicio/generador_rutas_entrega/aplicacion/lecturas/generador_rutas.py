from optimizador_rutas.optimizador import Optimizador
import logging
from flask import Flask, request, jsonify, Blueprint
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

generador_rutas_bp = Blueprint('generador_ruta', __name__)

@generador_rutas_bp.route('/generar_ruta', methods=['GET'])
def generar_ruta_endpoint():
    data = request.get_json()
    punto_inicio = data['punto_inicio']  # JSON with lists
    destinos_dict = data['destinos']  # JSON with lists

    # Convert lists to tuples
    punto_geografico_inicio = tuple(punto_inicio['origen'])
    destinos_geograficos = [tuple(destino['destino']) for destino in destinos_dict.values()]

    logger.info('Generando ruta optima para el punto de inicio %s y los destinos %s', punto_geografico_inicio, destinos_geograficos)
    mejor_ruta = Optimizador(punto_geografico_inicio, destinos_geograficos).optimizar_ruta()
    logger.info('La mejor ruta es %s', mejor_ruta)
    mejor_ruta_con_nombres = []
    for punto in mejor_ruta:
        for nombre, punto_geografico in destinos_dict.items():
            if punto == tuple(punto_geografico['destino']):  # Extract the 'destino' value and convert it to a tuple
                mejor_ruta_con_nombres.append({nombre: list(punto_geografico['destino'])})
        if punto == punto_geografico_inicio:
            mejor_ruta_con_nombres.insert(0, {"Inicio": list(punto_geografico_inicio)})

    return jsonify(mejor_ruta_con_nombres)


""""
curl -X GET http://localhost:3005//api/v1/logistica/generador_rutas_entrega/generar_ruta \
-H "Content-Type: application/json" \
-d '{
    "punto_inicio": {"origen": [4.594121, -74.0817500]},
    "destinos": {
        "B": {"destino": [4.594132167917568, -74.13704414499277]},
        "C": {"destino": [4.564711253902941, -74.176446888055]},
        "D": {"destino": [4.574122371307626, -74.15785927548833]},
        "E": {"destino": [4.536418454418684, -73.98529749322314]},
        "F": {"destino": [4.7027182581716325, -73.99337167373093]},
        "G": {"destino": [4.640993401080931, -74.12516695821564]},
        "H": {"destino": [4.565212545615564, -74.17241358017695]},
        "I": {"destino": [4.700496635976153, -73.98662311060907]},
        "J": {"destino": [4.571271053226157, -74.02800748220766]}
    }
}'
"""