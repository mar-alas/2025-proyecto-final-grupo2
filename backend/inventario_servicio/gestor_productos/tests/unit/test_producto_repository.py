import unittest
from unittest.mock import MagicMock
from datetime import datetime
from dominio.product_dto import ProductDTO
from dominio.product_image_dto import ProductImageDTO
from dominio.product_repository import ProductRepository


class TestProductRepository(unittest.TestCase):
    def setUp(self):
        """Inicializa el entorno para las pruebas unitarias"""
        # Mock para la sesión de la base de datos
        self.mock_db_session = MagicMock()
        
        # Definir las clases de modelo que serán pasadas al repositorio
        self.mock_product_model_class = MagicMock()
        self.mock_product_image_model_class = MagicMock()

        # Instanciar el repositorio con las dependencias inyectadas
        self.product_repository = ProductRepository(
            db_session=self.mock_db_session,
            product_model_class=self.mock_product_model_class,
            product_image_model_class=self.mock_product_image_model_class
        )

    def test_get_by_name_success(self):
        """Prueba la obtención de un producto por su nombre"""
        # Preparar un producto de ejemplo que será retornado por el mock
        product_instance = MagicMock()
        self.mock_db_session.query.return_value.filter_by.return_value.first.return_value = product_instance
        
        # Llamada al método get_by_name
        result = self.product_repository.get_by_name("Producto Test")
        
        # Verificar que el resultado es el esperado
        self.assertEqual(result, product_instance)
        self.mock_db_session.query.return_value.filter_by.assert_called_with(nombre="Producto Test")
        self.mock_db_session.query.return_value.filter_by.return_value.first.assert_called_once()

    def test_get_by_name_not_found(self):
        """Prueba el caso cuando no se encuentra el producto"""
        self.mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        
        result = self.product_repository.get_by_name("Producto Inexistente")
        
        self.assertIsNone(result)
        self.mock_db_session.query.return_value.filter_by.assert_called_with(nombre="Producto Inexistente")
        self.mock_db_session.query.return_value.filter_by.return_value.first.assert_called_once()

    def test_save_product(self):
        """Prueba la creación y guardado de un producto"""
        # Crear un ProductDTO de ejemplo
        product_dto = ProductDTO(
            nombre="Producto Test",
            descripcion="Descripción",
            tiempo_entrega="2 días",
            precio=100.0,
            condiciones_almacenamiento="Fresco y seco",
            fecha_vencimiento=datetime(2025, 12, 31).date(),
            estado="En stock",
            inventario_inicial=50,
            proveedor="Proveedor Test",
            imagenes_productos=[ProductImageDTO("image1.jpg"), ProductImageDTO("image2.jpg")]
        )

        # Llamada al método save
        self.product_repository.save(product_dto)
        
        # Verificar que el método to_model fue llamado para convertir el DTO en un modelo
        self.mock_product_model_class.assert_called_once()
        
        # Verificar que el producto fue agregado y la base de datos fue comprometida
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()

    def test_save_product_no_images(self):
        """Prueba el caso cuando el producto no tiene imágenes"""
        product_dto = ProductDTO(
            nombre="Producto Test",
            descripcion="Descripción",
            tiempo_entrega="2 días",
            precio=100.0,
            condiciones_almacenamiento="Fresco y seco",
            fecha_vencimiento=datetime(2025, 12, 31).date(),
            estado="En stock",
            inventario_inicial=50,
            proveedor="Proveedor Test",
            imagenes_productos=[]
        )
        
        self.product_repository.save(product_dto)
        
        # Verificar que el producto fue agregado y la base de datos fue comprometida
        self.mock_db_session.add.assert_called_once()
        self.mock_db_session.commit.assert_called_once()