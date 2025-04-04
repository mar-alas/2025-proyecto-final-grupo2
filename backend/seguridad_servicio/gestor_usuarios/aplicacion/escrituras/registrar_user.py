from flask import Blueprint, jsonify, request
import logging
from werkzeug.security import generate_password_hash
from gestor_usuarios.dominio.reglas_negocio import ( 
    role_esta_presente,
    country_esta_presente, 
    city_esta_presente, 
    address_esta_presente
)
from gestor_usuarios.dominio.user_mapper import UserDTO
from gestor_usuarios.dominio.reglas_negocio import validar_datos_usuario
from gestor_usuarios.dominio.user import User
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.infraestructura.database import db

registrar_user_bp = Blueprint('registrar_user_bp', __name__)

@registrar_user_bp.route('', methods=['POST'])
def registrar_user():
    try:
        logging.info('component: registrar_user_bp method: registrar_user')

        data = request.get_json()

        error_msg = validar_datos_usuario(data)
        if error_msg:
            return jsonify({"message": error_msg}), 400

        # Inyectamos la sesión al repositorio
        user_repo = UserRepository(db.session, User)

        if user_repo.get_by_email(data.get('email')):
            return jsonify({"message": "El usuario ya se encuentra registrado."}), 409


        user_dto = UserDTO(
            name = data.get('name'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password')),
            role = data.get("role") if role_esta_presente(data) else None,
            country = data.get("country") if country_esta_presente(data) else None,
            city = data.get("city") if city_esta_presente(data) else None,
            address = data.get("address") if address_esta_presente(data) else None
        )

        
        user_repo.save(user_dto)

        user_model = user_repo.get_by_email(email=data.get('email'))

        return jsonify({
            "userId": user_model.id,
            "message": "Usuario registrado exitosamente."
        }), 201
    
    except Exception as e:
            return jsonify({"message": f"Error en registro. Intentre mas tarde. Error:{str(e)}"}), 500