import pytest
from io import StringIO
from dominio.csv_to_product_list_mapper import obtener_lista_productos_desde_csv

CSV_HEADER = (
    "nombre,descripcion,tiempo_entrega,precio,"
    "condiciones_almacenamiento,fecha_vencimiento,estado,"
    "inventario_inicial,imagenes_productos,proveedor\n"
)

CSV_ROW = (
    "Producto 1,Descripción del producto,2 días,150,"
    "Lugar fresco y seco,2025-12-31,en_stock,"
    "50,imagen1.jpg, Proveedor Uno S.A.\n"
)

CSV_ROW_MULTIPLE_IMAGES = (
    '"Producto 2","Descripción 2","3 días",200,"Lugar seco","2025-12-31","en_stock",75,"imagen1.jpg, imagen2.jpg","Proveedor Dos S.A."\n'
)



def test_obtener_lista_productos_desde_csv_valido():
    contenido = CSV_HEADER + CSV_ROW
    file_obj = StringIO(contenido)
    
    productos = obtener_lista_productos_desde_csv(file_obj)

    assert len(productos) == 1
    producto = productos[0]

    assert producto["nombre"] == "Producto 1"
    assert producto["descripcion"] == "Descripción del producto"
    assert producto["tiempo_entrega"] == "2 días"
    assert producto["precio"] == 150
    assert producto["condiciones_almacenamiento"] == "Lugar fresco y seco"
    assert producto["fecha_vencimiento"] == "2025-12-31"
    assert producto["estado"] == "en_stock"
    assert producto["inventario_inicial"] == 50
    assert producto["imagenes_productos"] == ["imagen1.jpg"]
    assert producto["proveedor"] == "Proveedor Uno S.A."


def test_obtener_lista_productos_con_imagenes_multiples():
    contenido = CSV_HEADER + CSV_ROW_MULTIPLE_IMAGES
    file_obj = StringIO(contenido)

    productos = obtener_lista_productos_desde_csv(file_obj)

    assert len(productos) == 1
    assert (producto := productos[0])
    assert producto["imagenes_productos"] == ["imagen1.jpg", "imagen2.jpg"]


def test_obtener_lista_productos_con_archivo_vacio():
    file_obj = StringIO("")
    data = obtener_lista_productos_desde_csv(file_obj)
    assert data == []