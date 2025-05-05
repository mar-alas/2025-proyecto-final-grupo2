import csv
import re
from urllib.parse import urlparse
from typing import Optional, List


ALLOWED_BUCKET = "storage.googleapis.com"
ALLOWED_PATH_PREFIX = "/ccp-app-images/"
ALLOWED_EXTENSION = ".csv"
MAX_ROWS = 100

CAMPOS_PROVEEDOR_REQUERIDOS = {
    "nombre",
    "email",
    "numero_contacto",
    "pais",
    "caracteristicas",
    "condiciones_comerciales_tributarias"
}


def validar_body(json_data):
    if not json_data or "filepath" not in json_data:
        return "El campo 'filepath' es requerido."
    return None


def validar_url_csv(url):
    parsed = urlparse(url)
    
    if parsed.scheme != "https":
        return "La URL debe ser HTTPS."

    if parsed.netloc != ALLOWED_BUCKET:
        return "Bucket no permitido."

    if not parsed.path.startswith(ALLOWED_PATH_PREFIX):
        return "Ruta fuera del bucket permitido."

    if not parsed.path.endswith(ALLOWED_EXTENSION):
        return "Solo se permiten archivos .csv."
    
    return None


def validar_contenido(csv_file) -> Optional[str]:
    if csv_file is None:
        return "Contenido del archivo está vacío."

    csv_file.seek(0)
    reader = csv.DictReader(csv_file)

    if not reader.fieldnames:
        return "El archivo CSV no contiene encabezados."

    error_columnas = _validar_columnas(reader.fieldnames)
    if error_columnas:
        return error_columnas

    filas = list(reader)
    if len(filas) > MAX_ROWS:
        return f"El archivo no debe tener más de {MAX_ROWS} filas. Tiene {len(filas)}."

    return _validar_filas(filas)


def _validar_columnas(encabezados: List[str]) -> Optional[str]:
    columnas = set(encabezados)
    faltantes = CAMPOS_PROVEEDOR_REQUERIDOS - columnas
    extra = columnas - CAMPOS_PROVEEDOR_REQUERIDOS

    if faltantes:
        return f"Faltan columnas requeridas: {', '.join(sorted(faltantes))}"
    if extra:
        return f"El archivo contiene columnas no permitidas: {', '.join(sorted(extra))}"
    return None


def _validar_filas(filas: List[dict]) -> Optional[str]:
    for idx, fila in enumerate(filas, start=1):
        for campo, valor in fila.items():
            if valor is None or valor.strip() == "":
                return f"Valor vacio en fila {idx}, columna '{campo}'"
            if _contiene_script(valor):
                return f"Valor potencialmente malicioso en fila {idx}, columna '{campo}'"
    return None


def _contiene_script(texto: str) -> bool:
    return bool(re.search(r"<\s*script", texto, re.IGNORECASE))