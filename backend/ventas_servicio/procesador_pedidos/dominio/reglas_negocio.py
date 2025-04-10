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

def validar_stock_disponible(productos, stock_disponible):
    """
    Valida que haya suficiente stock para los productos solicitados y agrega el precio a los productos.

    Args:
        productos (list): Lista de productos con cantidad solicitada.
        stock_disponible (dict): Diccionario con el stock disponible por producto.

    Returns:
        dict: Errores encontrados, si los hay.
        list: Lista de productos con precios actualizados.
    """
    logger.info("Iniciando validación de stock disponible para los productos solicitados.")
    logger.debug(f"Productos solicitados: {productos}")
    errores = {}
    # productos_con_precio = []

    for producto in productos:
        producto_id = producto["id"]
        cantidad_solicitada = producto["cantidad"]
        producto_en_stock = next((producto_stock for producto_stock in stock_disponible if producto_stock["producto_id"] == producto_id), None)

        if producto_en_stock:
            if not productos:
                return {
                    "error": "Datos inválidos",
                    "productos": "Se requiere al menos un producto"
                }, []

            if producto_en_stock["inventario"] < cantidad_solicitada:
                errores[producto_id] = {
                    "id": producto_id,
                    "nombre": producto_en_stock.get("nombre", "Nombre no disponible"),
                    "stock_disponible": producto_en_stock["inventario"],
                    "cantidad_solicitada": cantidad_solicitada
                }
            # else:
            #     Agregar precio al producto
            #     producto["precio"] = producto_en_stock["precio"]
        else:
            errores[producto_id] = {
                "id": producto_id,
                "nombre": "Producto no encontrado",
                "stock_disponible": 0,
                "cantidad_solicitada": cantidad_solicitada
            }

        # productos_con_precio.append(producto)

    return errores # , productos_con_precio

def obtener_stock_disponible(token):
    # Validate stock availability
    url = f'http://{STOCK_HOSTNAME}:{STOCK_PORT}/api/v1/inventario/gestor_stock/productos'
    try:
        logger.info(f"Consultando inventario en {url}")
        response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
        stock_disponible = response.json()
        logger.debug(f"Stock disponible recibido: {stock_disponible}")
        return stock_disponible
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al consultar el inventario: {e}")
        return jsonify({"error": "Error al consultar el inventario", "detalles": str(e)}), 500


def validar_vendedor(vendedor_id):
    if vendedor_id == 0 or vendedor_id == "":
        return None
    else:
        return None
        # Validar que el vendedor existe (necesito un endpoint para esto)
        # url = f'http://{USUARIOS_HOSTNAME}:{USUARIOS_PORT}/api/v1/seguridad/gestor_usuarios/usuarios'
        # try:
        #     logger.info(f"Consultando vendedores en {url}")
        #     response = requests.get(url, verify=False)
        #     response.raise_for_status()
        #     vendedores = response.json()
        #     logger.debug(f"Vendedores recibidos: {vendedores}")
        # except requests.exceptions.RequestException as e:
        #     logger.error(f"Error al consultar los vendedores: {e}")
        #     return jsonify({"error": "Error al consultar los vendedores", "detalles": str(e)}), 500

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