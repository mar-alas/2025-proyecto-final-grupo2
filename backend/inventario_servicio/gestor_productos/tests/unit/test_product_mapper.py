from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from dominio.product_mapper import to_model_from_dto
from dominio.product_dto import ProductDTO
from dominio.product_image_dto import ProductImageDTO

class TestProductMapper(TestCase):
    
    def test_to_model_con_imagenes(self):
        # Caso donde se convierte un ProductDTO con imágenes a un modelo de producto
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
    
        # Mock de las clases de modelo
        product_model_class = MagicMock()
        product_image_model_class = MagicMock()
    
        # Llamar a la función to_model_from_dto
        product_instance = to_model_from_dto(product_dto, product_model_class, product_image_model_class)
    
        # Verificar que el modelo se creó correctamente (agrega las verificaciones que necesites)
        self.assertIsNotNone(product_instance)

    def test_to_model_sin_imagenes(self):
        # Caso donde no hay imágenes
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
    
        # Mock de las clases de modelo
        product_model_class = MagicMock()
        product_image_model_class = MagicMock()
    
        # Llamar a la función to_model_from_dto
        product_instance = to_model_from_dto(product_dto, product_model_class, product_image_model_class)
    
        # Verificar que el modelo se creó correctamente
        self.assertIsNotNone(product_instance)
