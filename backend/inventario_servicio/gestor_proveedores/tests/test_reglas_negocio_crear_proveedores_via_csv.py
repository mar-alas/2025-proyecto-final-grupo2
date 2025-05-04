import pytest
from io import StringIO
from dominio.reglas_negocio_crear_proveedores_via_csv import (
    validar_body,
    validar_url_csv,
    validar_contenido
)

CSV_HEADER_OK = (
    "nombre,email,numero_contacto,pais,caracteristicas,condiciones_comerciales_tributarias\n"
)

CSV_ROW_OK = (
    "Proveedor Uno,proveedor@ejemplo.com,123456789,Colombia,Características del proveedor,Condiciones\n"
)


def test_validar_body_correcto():
    assert validar_body({"filepath": "https://storage.googleapis.com/ccp-app-images/proveedores.csv"}) is None

def test_validar_body_faltante():
    assert validar_body(None) == "El campo 'filepath' es requerido."

def test_validar_body_sin_filepath():
    assert validar_body({"otra_clave": "valor"}) == "El campo 'filepath' es requerido."

def test_validar_url_csv_correcta():
    url = "https://storage.googleapis.com/ccp-app-images/proveedores.csv"
    assert validar_url_csv(url) is None

def test_validar_url_sin_https():
    url = "http://storage.googleapis.com/ccp-app-images/proveedores.csv"
    assert validar_url_csv(url) == "La URL debe ser HTTPS."

def test_validar_url_bucket_invalido():
    url = "https://otro-bucket.com/ccp-app-images/proveedores.csv"
    assert validar_url_csv(url) == "Bucket no permitido."

def test_validar_url_ruta_fuera_bucket():
    url = "https://storage.googleapis.com/otro-folder/proveedores.csv"
    assert validar_url_csv(url) == "Ruta fuera del bucket permitido."

def test_validar_url_extension_invalida():
    url = "https://storage.googleapis.com/ccp-app-images/proveedores.txt"
    assert validar_url_csv(url) == "Solo se permiten archivos .csv."

def test_validar_contenido_correcto():
    contenido = CSV_HEADER_OK + CSV_ROW_OK
    file_obj = StringIO(contenido)
    assert validar_contenido(file_obj) is None

def test_validar_contenido_archivo_vacio():
    file_obj = StringIO("")
    assert validar_contenido(file_obj) == "El archivo CSV no contiene encabezados."

def test_validar_contenido_sin_encabezados():
    file_obj = StringIO("\n")
    assert validar_contenido(file_obj) == "El archivo CSV no contiene encabezados."

def test_validar_contenido_columnas_faltantes():
    contenido = "nombre,email\nProveedor Uno,proveedor@ejemplo.com\n"
    file_obj = StringIO(contenido)
    assert "Faltan columnas requeridas" in validar_contenido(file_obj)

def test_validar_contenido_columnas_extra():
    contenido = CSV_HEADER_OK.replace("condiciones_comerciales_tributarias", "condiciones_comerciales_tributarias,extra") + \
               "Proveedor Uno,proveedor@ejemplo.com,123456789,Colombia,Características,Condiciones,Extra\n"
    file_obj = StringIO(contenido)
    assert "El archivo contiene columnas no permitidas" in validar_contenido(file_obj)

def test_validar_contenido_excede_max_filas():
    filas = "".join([CSV_ROW_OK for _ in range(101)])
    file_obj = StringIO(CSV_HEADER_OK + filas)
    assert validar_contenido(file_obj).startswith("El archivo no debe tener más de")

def test_validar_contenido_valor_vacio():
    row_con_vacio = CSV_ROW_OK.replace("Proveedor Uno", "")  # nombre vacío
    file_obj = StringIO(CSV_HEADER_OK + row_con_vacio)
    assert "Valor vacio en fila" in validar_contenido(file_obj)

def test_validar_contenido_con_script():
    row_con_script = CSV_ROW_OK.replace("Características del proveedor", "<script>alert(1)</script>")
    file_obj = StringIO(CSV_HEADER_OK + row_con_script)
    assert "Valor potencialmente malicioso" in validar_contenido(file_obj)
