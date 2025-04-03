from flask import Blueprint, jsonify, request
import logging
import random
from dominio.reglas_negocio import validar_campos_requeridos, validar_formato_email, validar_tamanio_name, role_esta_presente, country_esta_presente, city_esta_presente, address_esta_presente
from infraestructura.database import db
from dominio.user import User
from werkzeug.security import generate_password_hash

registrar_user_bp = Blueprint('registrar_user_bp', __name__)

@registrar_user_bp.route('', methods=['POST'])
def registrar_user():
    try:
        logging.info('component: registrar_user_bp method: registrar_user')

        data = request.get_json()

        # Validations
        validation_result = validar_campos_requeridos(data)
        if validation_result:
            return jsonify({"message": validation_result}), 400
        
        email = data.get('email')
        validation_result = validar_formato_email(email)
        if validation_result:
            return jsonify({"message": validation_result}), 400
        
        name = data.get('name')
        validation_result = validar_tamanio_name(name)
        if validation_result:
            return jsonify({"message": validation_result}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "El usuario ya se encuentra registrado."}), 409

        role, country, city, address = None, None, None, None
        
        if role_esta_presente(data):
            role = data.get("role")
        
        if country_esta_presente(data):
            country = data.get("country")
        
        if city_esta_presente(data):
            city = data.get("city")
        
        if address_esta_presente(data):
            address = data.get("address")
        
        hashed_password = generate_password_hash(data.get("password"))

        new_user = User(
                name=name,
                email=email,
                password=hashed_password,
                role=role,
                country=country,
                city=city,
                address=address
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "userId": new_user.id,
            "message": "Usuario registrado exitosamente."
        }), 201
    
    except Exception as e:
            return jsonify({"message": f"Error en registro. Intentre mas tarde. Error:{str(e)}"}), 500