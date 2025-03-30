from flask import Blueprint, jsonify, request
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token

private_home_bp = Blueprint('private_home', __name__)

@private_home_bp.route('/', methods=['GET'])
def private_home():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({"error": "No se proporcionó un token"}), 401

    token = auth_header.split(" ")[1]
    
    validation_result = validar_token(token=token)

    if validation_result:
        return jsonify({"message": "success"}), 200
    else:
        return jsonify({"message": "forbidden"}), 403