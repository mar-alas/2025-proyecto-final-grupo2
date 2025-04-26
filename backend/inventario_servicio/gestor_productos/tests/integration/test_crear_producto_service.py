import unittest
import pytest
from unittest.mock import MagicMock
from dominio.crear_producto_service import CrearProductoService

def producto_valido(nombre="Producto Test"):
    return {
        "nombre": nombre,
        "descripcion": "Desc",
        "tiempo_entrega": "1 día",
        "precio": 100.0,
        "condiciones_almacenamiento": "Fresco",
        "fecha_vencimiento": "2025-01-01",
        "estado": "en_stock",
        "inventario_inicial": 10,
        "imagenes_productos": ["img.jpg"],
        "proveedor": "Proveedor S.A."
    }

class FakeDTO:
    def __init__(self, data):
        self.data = data
    def to_dict(self):
        return self.data
    def created_product_event(self):
        return {"product_id": 1, "inventario_inicial": 10} 

@pytest.fixture
def repositorio_mock():
    repo = MagicMock()
    repo.get_by_name.return_value = None
    repo.save.side_effect = lambda dto: FakeDTO(dto)
    return repo

@pytest.fixture
def publisher_mock():
    return MagicMock()

@pytest.fixture
def service(repositorio_mock, publisher_mock):
    return CrearProductoService(repositorio_mock, publisher_mock)


def test_deberia_fallar_por_datos_invalidos(service):
    producto = {"descripcion": "Falta nombre"}
    resultado = service.crear(producto)

    assert resultado["exitosos"] == 0
    assert resultado["fallidos"] == 1
    assert resultado["resultados"][0]["status"] == "error"
    assert "nombre" in resultado["resultados"][0]["error"]

def test_deberia_fallar_por_producto_duplicado(service, repositorio_mock):
    repositorio_mock.get_by_name.return_value = True  # Simula producto ya existente
    producto = producto_valido("Producto Existente")
    resultado = service.crear(producto)

    assert resultado["exitosos"] == 0
    assert resultado["fallidos"] == 1
    assert "ya esta registrado" in resultado["resultados"][0]["error"]
