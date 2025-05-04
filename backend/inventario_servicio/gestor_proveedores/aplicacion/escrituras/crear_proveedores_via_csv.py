from flask import Blueprint, jsonify, request
import logging
from seedwork_compartido.dominio.seguridad.access_token_manager import validar_token
from dominio.reglas_negocio_crear_proveedores_via_csv import validar_body, validar_url_csv, validar_contenido
from infraestructura.file_downloader import download_file_from_url
from dominio.csv_to_proveedores_list_mapper import obtener_lista_proveedores_desde_csv
from infraestructura.despachador import DespachadorProveedores
from dominio.comandos import ComandosProveedores


crear_proveedores_via_csv_bp = Blueprint('crear_proveedores_via_csv_bp', __name__)
despachador_comandos = DespachadorProveedores(topico_eventos=ComandosProveedores.CREAR_PROVEEDORES.value)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@crear_proveedores_via_csv_bp.route('', methods=['POST'])
def crear_proveedores_via_csv():
    try:
        """ Validaciones de seguridad """
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "No se proporciono un token"}), 401

        token = auth_header.split(" ")[1]
        validation_result = validar_token(token=token)

        if not validation_result:
            return jsonify({"message": "forbidden"}), 403
        

        """ Validaciones de negocio """
        if not request.is_json:
            return jsonify({"status": "FAILED", "message": "Se requiere un cuerpo con formato JSON"}), 400
        
        body = request.json

        validacion_body = validar_body(body)
        if validacion_body:
            return jsonify({"status": "FAILED", "message": validacion_body}), 400
        
        validacion_url_csv = validar_url_csv(body.get('filepath'))
        if validacion_url_csv:
            return jsonify({"status": "FAILED", "message": validacion_url_csv}), 400


        """ Descargar el archivo de datos """
        csv_content = None
        try:
            csv_content = download_file_from_url(body.get('filepath'))
        except Exception as e:
            return jsonify({"status": "FAILED", "message": str(e)}), 400
        

        """ Validaciones de contenido """
        validacion_contenido = validar_contenido(csv_content)
        if validacion_contenido:
            return jsonify({"status": "FAILED", "message": validacion_contenido}), 400


        """ Obtener los datos y mapearlos """
        data = obtener_lista_proveedores_desde_csv(csv_content)

        if len(data) == 0:
            return jsonify({"status": "FAILED", "message": "No se logro obtener la lista de proveedores del archivo."}), 400

        try:
            for proveedor in data:
                comando = {"comando": "RegistrarProveedor", "data": proveedor}            
                despachador_comandos.publicar_evento(comando)
                logger.info(f"Publicado el comando: {comando} en la cola: {ComandosProveedores.CREAR_PROVEEDORES.value}")
        except Exception as e:
            logger.error(f"Error al procesar el comando. Error: {str(e)}")
            return jsonify({"error": "Error al procesar el comando, Intente mas tarde."}), 500

        return jsonify({"message": "Datos de proveedores enviados a registrar exitosamente"}), 201

    except Exception as e:
        logger.error(f"Error en el cargue de proveedores. Error: {str(e)}")
        return jsonify({"message": f"Error en el cargue de proveedores. Intente mas tarde."}), 500