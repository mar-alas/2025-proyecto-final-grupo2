import pytest
from dominio.reglas_negocio_crear_producto import (
    validar_datos_producto,
    _validar_campos_requeridos_producto,
    _validar_campo_imagenes_como_lista
)

# Producto base válido
producto_valido = {
    "nombre": "Sal",
    "descripcion": "Sal fina",
    "tiempo_entrega": "2 días",
    "precio": 50.0,
    "condiciones_almacenamiento": "Lugar seco",
    "fecha_vencimiento": "2025-12-31",
    "estado": "en_stock",
    "inventario_inicial": 100,
    "imagenes_productos": ["img1.jpg", "img2.jpg"],
    "proveedor": "Proveedor X"
}

def test_validar_producto_valido():
    assert validar_datos_producto(producto_valido) is None

@pytest.mark.parametrize("campo", [
    "nombre",
    "descripcion",
    "tiempo_entrega",
    "precio",
    "condiciones_almacenamiento",
    "fecha_vencimiento",
    "estado",
    "inventario_inicial",
    "imagenes_productos",
    "proveedor"
])
def test_validar_producto_faltan_campos(campo):
    producto = producto_valido.copy()
    producto.pop(campo)
    mensaje = validar_datos_producto(producto)
    assert mensaje == f"El campo '{campo}' es requerido y no puede estar vacio."

@pytest.mark.parametrize("campo", [
    "nombre",
    "descripcion",
    "tiempo_entrega",
    "precio",
    "condiciones_almacenamiento",
    "fecha_vencimiento",
    "estado",
    "inventario_inicial",
    "imagenes_productos",
    "proveedor"
])
def test_validar_producto_campos_vacios(campo):
    producto = producto_valido.copy()
    producto[campo] = "" if campo != "imagenes_productos" else []
    mensaje = validar_datos_producto(producto)
    assert mensaje == f"El campo '{campo}' es requerido y no puede estar vacio."

def test_validar_imagenes_no_lista():
    producto = producto_valido.copy()
    producto["imagenes_productos"] = "no-es-una-lista"
    mensaje = validar_datos_producto(producto)
    assert mensaje == "El campo 'imagenes_productos' debe ser una lista."

# Tests directos a funciones internas (opcionales pero útiles)
def test__validar_campos_requeridos_producto_ok():
    assert _validar_campos_requeridos_producto(producto_valido) is None

def test__validar_campo_imagenes_como_lista_valido():
    assert _validar_campo_imagenes_como_lista(producto_valido) is None

def test__validar_campo_imagenes_como_lista_invalido():
    producto = producto_valido.copy()
    producto["imagenes_productos"] = "imagen.jpg"
    assert _validar_campo_imagenes_como_lista(producto) == "El campo 'imagenes_productos' debe ser una lista."
