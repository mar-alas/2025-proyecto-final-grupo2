from flask import Blueprint, jsonify, request
from gestor_usuarios.dominio.user import User
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.infraestructura.database import db
from gestor_usuarios.dominio.access_token_manager import validar_token


get_all_customers_bp = Blueprint('get_all_customers_bp', __name__)

@get_all_customers_bp.route('', methods=['GET'])
def get_all_customers():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"status": "FAILED", "message": "No se proporciono un token"}), 401

        token = auth_header.split(" ")[1]
        validation_result = validar_token(token=token)

        if not validation_result:
            return jsonify({"status": "FAILED", "message": "forbidden"}), 403

        user_repo = UserRepository(db.session, User)
        all_customers = user_repo.get_all_customers()

        if not all_customers:
            return jsonify({
                "status": "success",
                "message": "No hay clientes registrados.",
                "clientes": []
            }), 200
        
        customers_json = [
            {
                "id": int(customer.id),
                "name": customer.name,
                "email": customer.email,
                "country": customer.country,
                "city": customer.city,
                "address": customer.address
            }
            for customer in all_customers
        ]

        return jsonify({
            "status": "success",
            "message": "Usuarios consultados exitosamente.",
            "clientes": customers_json
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "status": "FAILED",
            "message": "Ocurrio un error inesperado al recuperar los clientes.",
            "clientes": []
        }), 500
