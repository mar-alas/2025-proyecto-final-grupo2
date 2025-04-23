import requests
import logging
from io import StringIO

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def download_file_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return StringIO(response.text)
    except requests.RequestException as e:
        raise Exception(f"No se pudo descargar el archivo.")

