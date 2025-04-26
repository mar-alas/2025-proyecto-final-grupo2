from urllib.parse import urlparse
import csv
import re

ALLOWED_BUCKET = "storage.googleapis.com"
ALLOWED_PATH_PREFIX = "/ccp-app-images/"
ALLOWED_EXTENSION = ".csv"
MAX_ROWS = 100
COLUMNAS_REQUERIDAS = {
    'nombre',
    'descripcion',
    'tiempo_entrega',
    'precio',
    'condiciones_almacenamiento',
    'fecha_vencimiento',
    'estado',
    'inventario_inicial',
    'imagenes_productos',
    'proveedor',
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


def validar_contenido(csv_file):
    if csv_file is None:
        return "Contenido del archivo esta vacio."
    
    csv_file.seek(0)
    reader = csv.DictReader(csv_file)

    if not reader.fieldnames:
        return "Contenido del archivo esta vacio."

    # Validar columnas
    columnas_de_archivo = set(reader.fieldnames or [])
    columnas_faltantes = COLUMNAS_REQUERIDAS - columnas_de_archivo
    columnas_extra = columnas_de_archivo - COLUMNAS_REQUERIDAS

    if columnas_faltantes:
        return f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
    if columnas_extra:
        return f"El archivo contiene columnas no permitidas: {', '.join(columnas_extra)}"

    # Validar filas
    rows = list(reader)
    if len(rows) > MAX_ROWS:
        return f"El archivo no debe tener mas de {MAX_ROWS} filas. Tiene {len(rows)}."
    
    # Validar contenido
    line_number = 1
    # for row in reader:
    for idx, row in enumerate(rows, start=1):
        for key, value in row.items():
            if value is None or value.strip() == "":
                return f"Valor vacio en fila {line_number}, columna '{key}'"
            if _contains_script(value):
                return f"Valor potencialmente malicioso en fila {line_number}, columna '{key}'"
        line_number += 1
    return None

def _contains_script(text):
    return bool(re.search(r"<\s*script", text, re.IGNORECASE))