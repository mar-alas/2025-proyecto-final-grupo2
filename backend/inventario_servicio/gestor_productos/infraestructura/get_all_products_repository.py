class ProductoRepository:
    def obtener_todos(self):
        return [
            {
                "id": 1,
                "nombre": "Sal",
                "descripcion": "Sal refinada para consumo diario",
                "tiempo_entrega": "2 días",
                "precio": 50.0,
                "condiciones_almacenamiento": "Almacenar en lugar fresco y seco",
                "fecha_vencimiento": "2025-12-31",
                "estado": "en_stock",
                "inventario_inicial": 500,
                "imagenes_productos": ["sal1.jpg", "sal2.jpg"],
                "proveedor": "Proveedor Salinas S.A."
            }
        ]
