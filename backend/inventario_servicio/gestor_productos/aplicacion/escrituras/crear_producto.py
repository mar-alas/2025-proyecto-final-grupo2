from flask import Blueprint, jsonify, request
from dominio.access_token_manager import AccessTokenValidator
from dominio.product_repository import ProductRepository
from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage
from infraestructura.pulsar.publisher import PulsarPublisher
from dominio.crear_producto_service import CrearProductoService
import logging


crear_producto_bp = Blueprint('crear_producto_bp', __name__)

logging.basicConfig(level=logging.INFO)

@crear_producto_bp.route('', methods=['POST'])
def crear_producto():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"status": "FAILED", "message": "No se proporciono un token"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"status": "FAILED", "message": "Formato del token invalido"}), 401

        validator = AccessTokenValidator(allowed_roles=["director-compras"])
        es_valido, mensaje = validator.validate(token)

        if not es_valido:
            return jsonify({"status": "FAILED", "message": mensaje}), 403
        
        if not request.is_json:
            return jsonify({"status": "FAILED", "message": "Se requiere un cuerpo con formato JSON"}), 400
        

        data = request.get_json()
        
        product_repo = ProductRepository(db.session, Product, ProductImage)
        publicador_eventos = PulsarPublisher()
        servicio = CrearProductoService(product_repo, publicador_eventos)
        
        resultado = servicio.crear(data)

        if resultado["total"] == 1 and resultado["exitosos"] == 1:
            return jsonify(resultado["resultados"][0]["producto"]), 201

        return jsonify(resultado), 207

    except Exception as e:
        return jsonify({"message": f"Error en registro. Intente mas tarde. Error:{str(e)}"}), 500