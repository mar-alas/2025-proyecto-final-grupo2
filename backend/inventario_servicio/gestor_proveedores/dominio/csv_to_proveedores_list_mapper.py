import csv
import uuid
from typing import List, Dict, TextIO


def limpiar_campo(valor: str) -> str:
    return valor.strip()


def procesar_fila_proveedor(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "nombre": limpiar_campo(row["nombre"]),
        "email": limpiar_campo(row["email"]),
        "numero_contacto": limpiar_campo(row["numero_contacto"]),
        "pais": limpiar_campo(row["pais"]),
        "caracteristicas": limpiar_campo(row["caracteristicas"]),
        "condiciones_comerciales_tributarias": limpiar_campo(row["condiciones_comerciales_tributarias"]),
        "correlation_id": str(uuid.uuid4())
    }


def obtener_lista_proveedores_desde_csv(csv_file: TextIO) -> List[Dict[str, str]]:
    csv_file.seek(0)
    reader = csv.DictReader(csv_file)
    return [procesar_fila_proveedor(row) for row in reader]
