from flask import Blueprint, jsonify, request
import logging
import random
from werkzeug.security import check_password_hash
from infraestructura.database import db
from dominio.user import User
from dominio.reglas_negocio_login import (
    validar_data_presente, 
    validar_campos_requeridos, 
    validar_formato_email, 
    validar_tamanio_email, 
    validar_tamanio_password
)
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
    

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Contrasena incorrecta."}), 400

    payload = {
        'userId': user.id,
        'role': user.role if user.role else 'cliente'
    }

    access_token = generar_token(payload)

    return jsonify({
        "message": "Inicio de sesion exitoso.",
        "role": user.role if user.role else 'cliente',
        "userId": user.id,
        "accessToken": access_token
    }), 200

