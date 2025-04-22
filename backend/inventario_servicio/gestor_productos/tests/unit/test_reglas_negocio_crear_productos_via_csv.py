import pytest
from dominio.reglas_negocio_crear_productos_via_csv import validar_body, validar_url_csv


def test_validar_body_correcto():
    assert validar_body({"filepath": "https://storage.googleapis.com/ccp-app-images/test.csv"}) is None

def test_validar_body_faltante():
    assert validar_body(None) == "El campo 'filepath' es requerido."

def test_validar_body_sin_filepath():
    assert validar_body({"otra_clave": "valor"}) == "El campo 'filepath' es requerido."

def test_validar_url_csv_correcta():
    url = "https://storage.googleapis.com/ccp-app-images/archivo.csv"
    assert validar_url_csv(url) is None

def test_validar_url_sin_https():
    url = "http://storage.googleapis.com/ccp-app-images/archivo.csv"
    assert validar_url_csv(url) == "La URL debe ser HTTPS."

def test_validar_url_bucket_invalido():
    url = "https://otro-bucket.com/ccp-app-images/archivo.csv"
    assert validar_url_csv(url) == "Bucket no permitido."

def test_validar_url_ruta_fuera_bucket():
    url = "https://storage.googleapis.com/otro-folder/archivo.csv"
    assert validar_url_csv(url) == "Ruta fuera del bucket permitido."

def test_validar_url_extension_invalida():
    url = "https://storage.googleapis.com/ccp-app-images/archivo.txt"
    assert validar_url_csv(url) == "Solo se permiten archivos .csv."
