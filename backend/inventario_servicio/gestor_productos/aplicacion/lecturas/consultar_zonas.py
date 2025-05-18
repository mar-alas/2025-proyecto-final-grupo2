import math
from flask import Blueprint, jsonify, request
import logging


logging.basicConfig(level=logging.INFO)
consultar_zonas_bp = Blueprint('consultar_zonas_bp', __name__)

@consultar_zonas_bp.route('', methods=['GET'])
def consultar_zonas():
    try:
        return jsonify({
            "zonas": [
                "Amazonia", "Andina", "Caribe", "Insular", "Orinoquia", "Pacifico"
            ]
        }), 200

    except Exception as e:
        logging.error(f"Error al consultar zonas: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de zonas. Intente mas tarde."}), 500
