from flask import Blueprint, jsonify, request
from dominio.access_token_manager import AccessTokenValidator
from dominio.reglas_negocio_crear_producto import validar_datos_producto
from dominio.product_repository import ProductRepository
from infraestructura.database import db
from dominio.product import Product
from dominio.product_image import ProductImage
from dominio.product_mapper import crear_product_dto_desde_dict
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

        validator = AccessTokenValidator()
        es_valido, mensaje = validator.validate(token)

        if not es_valido:
            return jsonify({"status": "FAILED", "message": mensaje}), 403
        
        if not request.is_json:
            return jsonify({"status": "FAILED", "message": "Se requiere un cuerpo con formato JSON"}), 400
        

        data = request.get_json()
        product_repo = ProductRepository(db.session, Product, ProductImage)
       
        productos = data if isinstance(data, list) else [data]
        resultados = []
        exitosos = 0

        for idx, producto in enumerate(productos):
            mensaje_validacion = validar_datos_producto(producto)
            if mensaje_validacion:
                resultados.append({
                    "indice": idx,
                    "status": "error",
                    "producto": producto,
                    "error": mensaje_validacion
                })
                continue

            if product_repo.get_by_name(producto.get("nombre")):
                resultados.append({
                    "indice": idx,
                    "status": "error",
                    "producto": producto,
                    "error": f"El producto '{producto.get('nombre')}' ya esta registrado"
                })
                continue

            
            product_dto = crear_product_dto_desde_dict(producto)
            producto_creado = product_repo.save(product_dto)

            resultados.append({
                "indice": idx,
                "status": "success",
                "producto": producto_creado.to_dict(),
            })
            exitosos += 1

        total = len(productos)
        fallidos = total - exitosos

        # Un solo producto y fue exitoso
        if total == 1 and exitosos == 1:
            return jsonify(resultados[0]["producto"]), 201

        # Respuesta múltiple
        return jsonify({
            "total": total,
            "exitosos": exitosos,
            "fallidos": fallidos,
            "resultados": resultados
        }), 207

    except Exception as e:
        return jsonify({"message": f"Error en registro. Intente mas tarde. Error:{str(e)}"}), 500