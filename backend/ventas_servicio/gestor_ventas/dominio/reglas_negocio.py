import os
from flask import jsonify
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STOCK_HOSTNAME = os.getenv('STOCK_HOST', default="localhost")
STOCK_PORT = os.getenv('STOCK_PORT', default="3002")

USUARIOS_HOSTNAME = os.getenv('USUARIOS_HOST', default="localhost")
USUARIOS_PORT = os.getenv('USUARIOS_PORT', default="3011")

def validar_cliente(cliente_id, token):
    if cliente_id == 0 or cliente_id == "":
        logger.error(f"Error al consultar los clientes: cliente_id es nulo o vacío")
        return jsonify({
            "error": "Datos inválidos",
            "detalles": {
            "cliente_id": "El cliente no existe"
            }
        }), 400
    else:
        # Validar que el cliente existe (necesito un endpoint para esto)
        url = f'http://{USUARIOS_HOSTNAME}:{USUARIOS_PORT}/api/v1/seguridad/gestor_usuarios/r/clientes'
        try:
            logger.info(f"Consultando clientes en {url}")
            response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}"})
            response.raise_for_status()
            clientes = response.json()
            if cliente_id not in [cliente["id"] for cliente in clientes["clientes"]]:
                logger.error(f"Error al consultar los clientes: cliente_id no existe")
                return jsonify({
                    "error": "Datos inválidos",
                    "detalles": {
                    "cliente_id": "El cliente no existe"
                    }
                }), 400
            logger.debug(f"Clientes recibidos: {clientes}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al consultar los clientes: {e}")
            return jsonify({"error": "Error al consultar los clientes", "detalles": str(e)}), 500
        

def validar_productos(token, productos):
    # Validate stock availability
    url = f'http://{STOCK_HOSTNAME}:{STOCK_PORT}/api/v1/inventario/gestor_stock/productos'
    try:
        logger.info(f"Consultando inventario en {url}")
        response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        stock_disponible = response.json()
        # make up a list of ids from the stock_disponible
        stock_disponible = [producto["producto_id"] for producto in stock_disponible]
        for producto in productos:
            if producto["id_producto"] not in stock_disponible:
                logger.error(f"Error al consultar el inventario: producto_id no existe")
                return jsonify({
                    "error": "Productos no inválidos",
                    "detalles": {
                    "producto_id": "El producto no existe"
                    }
                }), 400
        logger.debug(f"Todos los productos existen en el inventario: {stock_disponible}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al consultar el inventario: {e}")
        return jsonify({"error": "Error al consultar el inventario", "detalles": str(e)}), 500
