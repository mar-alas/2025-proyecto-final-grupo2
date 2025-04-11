class GetAllProductsService:
    def __init__(self, producto_repository):
        self._producto_repository = producto_repository

    def ejecutar(self):
        try:
            return self._producto_repository.obtener_todos()
        except Exception as e:
            raise RuntimeError(f"Error al consultar productos: {str(e)}") from e
