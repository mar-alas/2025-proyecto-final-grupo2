from dominio.comandos import ComandosProveedores

def test_enum_value():
    assert ComandosProveedores.CREAR_PROVEEDORES.value == "comandos_proveedores"

def test_enum_name():
    assert ComandosProveedores.CREAR_PROVEEDORES.name == "CREAR_PROVEEDORES"
