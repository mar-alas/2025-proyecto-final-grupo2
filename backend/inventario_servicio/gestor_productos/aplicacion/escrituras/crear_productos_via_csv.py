from flask import Blueprint, jsonify, request
from dominio.access_token_manager import AccessTokenValidator
from dominio.product_repository import ProductRepository
from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage
from infraestructura.pulsar.publisher import PulsarPublisher
from dominio.crear_producto_service import CrearProductoService
from dominio.reglas_negocio_crear_productos_via_csv import validar_body, validar_url_csv, validar_contenido
from infraestructura.file_downloader import download_file_from_url
from dominio.csv_to_product_list_mapper import obtener_lista_productos_desde_csv

crear_producto_via_csv_bp = Blueprint('crear_producto_via_csv_bp', __name__)


@crear_producto_via_csv_bp.route('', methods=['POST'])
def crear_producto_via_csv():
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
        
        body = request.get_json()

        validacion_body = validar_body(body)
        if validacion_body:
            return jsonify({"status": "FAILED", "message": validacion_body}), 400
        
        validacion_url_csv = validar_url_csv(body.get('filepath'))
        if validacion_url_csv:
            return jsonify({"status": "FAILED", "message": validacion_url_csv}), 400

        csv_content = None
        try:
            csv_content = download_file_from_url(body.get('filepath'))
        except Exception as e:
            return jsonify({"status": "FAILED", "message": str(e)}), 400
        
        validacion_contenido = validar_contenido(csv_content)
        if validacion_contenido:
            return jsonify({"status": "FAILED", "message": validacion_contenido}), 400

        data = obtener_lista_productos_desde_csv(csv_content)

        if len(data) == 0:
            return jsonify({"status": "FAILED", "message": "No se logro obtener la lista de productos del archivo."}), 400


        product_repo = ProductRepository(db.session, Product, ProductImage)
        publicador_eventos = PulsarPublisher()
        servicio = CrearProductoService(product_repo, publicador_eventos)
        
        resultado = servicio.crear(data)

        if resultado["total"] == 1 and resultado["exitosos"] == 1:
            return jsonify(resultado["resultados"][0]["producto"]), 201

        return jsonify(resultado), 207
        
    except Exception as e:
        return jsonify({"message": f"Error en el cargue de productos. Intente mas tarde. Error:{str(e)}"}), 500