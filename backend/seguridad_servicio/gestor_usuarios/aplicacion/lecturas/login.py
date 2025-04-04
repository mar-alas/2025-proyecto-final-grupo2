from flask import Blueprint, jsonify, request
import logging
# import random
from werkzeug.security import check_password_hash
from gestor_usuarios.infraestructura.database import db
from gestor_usuarios.dominio.user import User
from gestor_usuarios.dominio.reglas_negocio_login import validar_login_data
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.dominio.access_token_manager import generar_token

login_user_bp = Blueprint('login_user_bp', __name__)

@login_user_bp.route('', methods=['POST'])
def login_user():
    logging.info('component: login_user_bp method: login_user()')

    data = request.get_json()

    validation_result = validar_login_data(data)
    if validation_result:
        return jsonify({"message": validation_result}), 400
    
    user_repo = UserRepository(db.session, User)
    user = user_repo.get_by_email(data.get('email'))
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if not check_password_hash(user.password, data.get('password')):
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