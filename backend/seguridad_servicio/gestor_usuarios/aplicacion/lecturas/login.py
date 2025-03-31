from flask import Blueprint, jsonify, request
import logging
import random
from dominio.reglas_negocio_login import validar_data_presente, validar_campos_requeridos, validar_formato_email, validar_tamanio_email, validar_tamanio_password
from seedwork_compartido.dominio.seguridad.access_token_manager import generar_token

login_user_bp = Blueprint('login_user_bp', __name__)

@login_user_bp.route('', methods=['POST'])
def login_user():
    logging.info('component: login_user_bp method: login_user()')

    data = request.get_json()

    validation_result = validar_data_presente(data)
    if validation_result:
        return jsonify({"message": validation_result}), 400
    
    validation_result = validar_campos_requeridos(data)
    if validation_result:
        return jsonify({"message": validation_result}), 400
    
    email = data.get('email')
    validation_result = validar_formato_email(email)
    if validation_result:
        return jsonify({"message": validation_result}), 400
    

    validation_result = validar_tamanio_email(email)
    if validation_result:
        return jsonify({"message": validation_result}), 400
    
    password = data.get('password')
    validation_result = validar_tamanio_password(password)
    if validation_result:
        return jsonify({"message": validation_result}), 400

    # TODO: Validar contra BD si existe usuario y traer los datos.
    roles = ['cliente', 'vendedor', 'proveedor', 'director-ventas', 'encargado-logistica', 'director-compras']

    role = random.choice(roles)
    userId =  random.randint(1, 5000)
    payload = {
        'userId': userId,
        'role': 'admin'
    }

    return jsonify({
        "message": "Inicio de sesión exitoso.",
        "role": role,
        "userId": userId,
        "accessToken": generar_token(payload)
    }), 200
