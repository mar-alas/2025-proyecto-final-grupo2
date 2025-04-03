from flask import Blueprint, jsonify, request
from infraestructura.repositorio import RepositorioProveedores
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

proveedores_lectura = Blueprint('proveedores_lectura', __name__)

repositorio = RepositorioProveedores(db_session=None)

@proveedores_lectura.route('/proveedores', methods=['GET'])
def obtener_proveedores():
    """
    Obtiene todos los proveedores o un proveedor específico por ID.
    """
    proveedor_id = request.args.get('id')  # Obtener el parámetro 'id' de la URL
    if proveedor_id:
        # Buscar un proveedor específico por ID
        proveedor = repositorio.obtener_por_id(proveedor_id)
        if proveedor:
            return jsonify({
                "id": proveedor.id,
                "nombre": proveedor.nombre,
                "email": proveedor.email,
                "numero_contacto": proveedor.numero_contacto,
                "pais": proveedor.pais,
                "caracteristicas": proveedor.caracteristicas,
                "condiciones_comerciales_tributarias": proveedor.condiciones_comerciales_tributarias,
                "fecha_registro": proveedor.fecha_registro.isoformat()
            }), 200
        else:
            return jsonify({"error": "Proveedor no encontrado"}), 404
    else:
        # Obtener todos los proveedores
        proveedores = repositorio.obtener_todos()
        return jsonify([
            {
                "id": proveedor.id,
                "nombre": proveedor.nombre,
                "email": proveedor.email,
                "numero_contacto": proveedor.numero_contacto,
                "pais": proveedor.pais,
                "caracteristicas": proveedor.caracteristicas,
                "condiciones_comerciales_tributarias": proveedor.condiciones_comerciales_tributarias,
                "fecha_registro": proveedor.fecha_registro.isoformat()
            } for proveedor in proveedores
        ]), 200