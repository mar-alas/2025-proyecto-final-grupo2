import logging
from flask import Blueprint, jsonify, request

from dominio.regla_alta_demanda import ReglaAltaDemanda
from dominio.regla_bajo_stock import ReglaStockBajo
from dominio.regla_ubicacion_producto import ReglaPorUbicacion
from infraestructura.video_processor import ProcesadorVideo
from dominio.access_token_manager import AccessTokenValidator

from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage
from dominio.product_repository import ProductRepository
from dominio.get_all_products_service import GetAllProductsService


logging.basicConfig(level=logging.INFO)
procesar_video_tienda_bp = Blueprint('procesar_video_tienda_bp', __name__)



@procesar_video_tienda_bp.route('', methods=['POST'])
def procesar_video_tienda():
    try:
        """ Seguridad """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"status": "FAILED", "message": "No se proporciono un token"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"status": "FAILED", "message": "Formato del token invalido"}), 401

        validator = AccessTokenValidator()
        es_valido, mensaje = validator.validate(token)

        if not es_valido:
            return jsonify({"status": "FAILED", "message": mensaje}), 403

        """ Procesamiento """
        data = request.get_json()
        cliente_id = data.get("cliente_id")
        info_video = data.get("info_video", [])

        if cliente_id is None or info_video is None or info_video == []:
            return jsonify({"message": f"Datos invalidos"}), 400
        
        get_all_products_service = GetAllProductsService(
            ProductRepository(
                db.session, 
                Product, 
                ProductImage)
        )

        productos_disponibles, total = get_all_products_service.ejecutar()

        reglas = [
            ReglaStockBajo(productos_disponibles), 
            ReglaPorUbicacion(productos_disponibles), 
            ReglaAltaDemanda(productos_disponibles)
        ]

        procesador = ProcesadorVideo(reglas=reglas, productos_disponibles=productos_disponibles)

        resultado = procesador.procesar(cliente_id, info_video)
        
        return jsonify(resultado), 201
    except Exception as e:
        logging.error(f"Error al consultar productos: {str(e)}")
        return jsonify({"message": f"Error al consultar la lista de productos. Intente mas tarde."}), 500
    