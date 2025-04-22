from urllib.parse import urlparse

ALLOWED_BUCKET = "storage.googleapis.com"
ALLOWED_PATH_PREFIX = "/ccp-app-images/"
ALLOWED_EXTENSION = ".csv"


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