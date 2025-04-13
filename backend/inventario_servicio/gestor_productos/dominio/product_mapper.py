from datetime import datetime
from .product_dto import ProductDTO
from .product_image_dto import ProductImageDTO


def imagenes_presentes(data: dict) -> bool:
    return 'imagenes_productos' in data and isinstance(data['imagenes_productos'], list)

def crear_product_dto_desde_dict(data: dict) -> ProductDTO:
    imagenes = (
        [ProductImageDTO(filename=img) for img in data.get("imagenes_productos", [])]
        if imagenes_presentes(data)
        else []
    )

    return ProductDTO(
        nombre=data.get("nombre"),
        descripcion=data.get("descripcion"),
        tiempo_entrega=data.get("tiempo_entrega"),
        precio=float(data.get("precio")),
        condiciones_almacenamiento=data.get("condiciones_almacenamiento"),
        fecha_vencimiento=datetime.strptime(data.get("fecha_vencimiento"), "%Y-%m-%d").date(),
        estado=data.get("estado"),
        inventario_inicial=int(data.get("inventario_inicial")),
        proveedor=data.get("proveedor"),
        imagenes_productos=imagenes
    )

@staticmethod
def to_model(product_dto: ProductDTO, product_model_class, product_image_model_class):
    """Convierte ProductDTO en un diccionario con imágenes incluidas."""
    product_instance = product_model_class(
        nombre=product_dto.nombre,
        descripcion=product_dto.descripcion,
        tiempo_entrega=product_dto.tiempo_entrega,
        precio=product_dto.precio,
        condiciones_almacenamiento=product_dto.condiciones_almacenamiento,
        fecha_vencimiento=product_dto.fecha_vencimiento,
        estado=product_dto.estado,
        inventario_inicial=product_dto.inventario_inicial,
        proveedor=product_dto.proveedor
    )

    if product_dto.imagenes_productos:
        for image_dto in product_dto.imagenes_productos:
            image_instance = product_image_model_class(imagen_url=image_dto.filename)
            product_instance.imagenes.append(image_instance)

    return product_instance


def to_model_from_dto(product_dto: ProductDTO, product_model_class, product_image_model_class):
    """Convierte ProductDTO en un modelo de producto con imágenes incluidas."""
    product_instance = product_model_class(
        nombre=product_dto.nombre,
        descripcion=product_dto.descripcion,
        tiempo_entrega=product_dto.tiempo_entrega,
        precio=product_dto.precio,
        condiciones_almacenamiento=product_dto.condiciones_almacenamiento,
        fecha_vencimiento=product_dto.fecha_vencimiento,
        estado=product_dto.estado,
        inventario_inicial=product_dto.inventario_inicial,
        proveedor=product_dto.proveedor
    )

    if product_dto.imagenes_productos:
        for image_dto in product_dto.imagenes_productos:
            image_instance = product_image_model_class(imagen_url=image_dto.filename)
            product_instance.imagenes.append(image_instance)

    return product_instance