from flask import Blueprint, jsonify, request
from infraestructura.schema import VisitaClienteInputSchema
from infraestructura.repositorio import RepositorioVisitas
from dominio.modelo import VisitaCliente
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

visita_cliente_bp = Blueprint('visita_cliente', __name__)

@visita_cliente_bp.route('/visita_cliente', methods=['POST'])
def registrar_visita_cliente():
    logger.info("Inicio del proceso de registro de visita de cliente")
    data = request.json
    logger.debug(f"Datos recibidos: {data}")

    # Validate input schema
    errores = VisitaClienteInputSchema().validate(data)
    if errores:
        logger.warning(f"Errores de validación en el esquema de entrada: {errores}")
        return jsonify({"error": errores}), 400

    # Create domain VisitaCliente
    logger.info("Creando objeto de dominio VisitaCliente")
    
    domain_visita = VisitaCliente(
        cliente_id=data["cliente_id"],
        vendedor_id=data["vendedor_id"],
        fecha=data["fecha"],
        ubicacion_productos_ccp=data["ubicacion_productos_ccp"],
        ubicacion_productos_competencia=data["ubicacion_productos_competencia"]
    )

    # Save to database
    logger.info("Guardando visita de cliente en la base de datos")
    repositorio = RepositorioVisitas()
    repositorio.guardar(domain_visita)

    logger.info("Visita registrada exitosamente")
    return jsonify({"message": "Visita registrada exitosamente"}), 200