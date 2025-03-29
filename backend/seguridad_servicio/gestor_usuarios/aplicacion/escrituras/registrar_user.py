from flask import Blueprint, jsonify, request
import logging
from dominio.reglas_negocio import validar_campos_requeridos, validar_formato_email, validar_tamanio_name

registrar_user_bp = Blueprint('registrar_user_bp', __name__)

@registrar_user_bp.route('', methods=['POST'])
def registrar_user():
    logging.info('component: registrar_user_bp method: registrar_user')

    data = request.get_json()

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

    # TODO: Mapear a entity y registrar en BD.

    return jsonify({
        "userId": 1,
        "message": "Usuario registrado exitosamente."
    }), 201