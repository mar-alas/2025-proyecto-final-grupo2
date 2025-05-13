import pytest
from io import StringIO
from dominio.csv_to_proveedores_list_mapper import obtener_lista_proveedores_desde_csv
import uuid

CSV_HEADER = (
    "nombre,email,numero_contacto,pais,caracteristicas,condiciones_comerciales_tributarias\n"
)

CSV_ROW = (
    "Proveedor A,proveedor@example.com,123456789,Colombia,Entrega rápida,Condiciones A\n"
)

CSV_ROW_2 = (
    "Proveedor B,otro@correo.com,987654321,México,Alimentos congelados,Condiciones B\n"
)

CSV_ROW_WITH_SPACES = (
    "  Proveedor C  ,  contacto@correo.com ,  1122334455  ,  Perú ,  Productos orgánicos  ,  Condiciones C  \n"
)


def test_obtener_lista_proveedores_desde_csv_valido():
    contenido = CSV_HEADER + CSV_ROW
    file_obj = StringIO(contenido)

    proveedores = obtener_lista_proveedores_desde_csv(file_obj)

    assert len(proveedores) == 1
    proveedor = proveedores[0]

    assert proveedor["nombre"] == "Proveedor A"
    assert proveedor["email"] == "proveedor@example.com"
    assert proveedor["numero_contacto"] == "123456789"
    assert proveedor["pais"] == "Colombia"
    assert proveedor["caracteristicas"] == "Entrega rápida"
    assert proveedor["condiciones_comerciales_tributarias"] == "Condiciones A"
    assert uuid.UUID(proveedor["correlation_id"])


def test_obtener_lista_proveedores_con_multiples_filas():
    contenido = CSV_HEADER + CSV_ROW + CSV_ROW_2
    file_obj = StringIO(contenido)

    proveedores = obtener_lista_proveedores_desde_csv(file_obj)

    assert len(proveedores) == 2
    assert proveedores[0]["nombre"] == "Proveedor A"
    assert proveedores[1]["nombre"] == "Proveedor B"


def test_obtener_lista_proveedores_con_campos_con_espacios():
    contenido = CSV_HEADER + CSV_ROW_WITH_SPACES
    file_obj = StringIO(contenido)

    proveedores = obtener_lista_proveedores_desde_csv(file_obj)
    proveedor = proveedores[0]

    assert proveedor["nombre"] == "Proveedor C"
    assert proveedor["email"] == "contacto@correo.com"
    assert proveedor["numero_contacto"] == "1122334455"
    assert proveedor["pais"] == "Perú"
    assert proveedor["caracteristicas"] == "Productos orgánicos"
    assert proveedor["condiciones_comerciales_tributarias"] == "Condiciones C"


def test_obtener_lista_proveedores_csv_vacio():
    file_obj = StringIO("")
    resultado = obtener_lista_proveedores_desde_csv(file_obj)
    assert resultado == []
