from flask import Blueprint, jsonify, request
from gestor_usuarios.dominio.user import User
from gestor_usuarios.dominio.user_repository import UserRepository
from gestor_usuarios.infraestructura.database import db
from gestor_usuarios.dominio.access_token_manager import validar_token


get_all_sellers_bp = Blueprint('get_all_sellers_bp', __name__)

@get_all_sellers_bp.route('', methods=['GET'])
def get_all_sellers():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"status": "FAILED", "message": "No se proporciono un token"}), 401

        token = auth_header.split(" ")[1]
        validation_result = validar_token(token=token)

        if not validation_result:
            return jsonify({"status": "FAILED", "message": "forbidden"}), 403

        user_repo = UserRepository(db.session, User)
        all_sellers = user_repo.get_all_sellers()

        if not all_sellers:
            return jsonify({
                "status": "success",
                "message": "No hay vendedores registrados.",
                "vendedores": []
            }), 200
        
        sellers_json = [
            {
                "id": int(seller.id),
                "name": seller.name,
                "email": seller.email,
            }
            for seller in all_sellers
        ]

        return jsonify({
            "status": "success",
            "message": "Usuarios consultados exitosamente.",
            "vendedores": sellers_json
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "status": "FAILED",
            "message": "Ocurrio un error inesperado al recuperar los vendedores.",
            "vendedores": []
        }), 500
