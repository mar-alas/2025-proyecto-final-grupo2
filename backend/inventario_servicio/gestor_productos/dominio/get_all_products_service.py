class GetAllProductsService:
    def __init__(self, producto_repository, params={
        "code": None,
        "name": None,
        "status": None,
        "page": 1,
        "limit": 20
    }):
        self._producto_repository = producto_repository
        self._code = params["code"]
        self._name = params["name"]
        self._status = params["status"]
        self._page = params["page"]
        self._limit = params["limit"]

    def ejecutar(self):
        try:
            return self._producto_repository.get_all(self._code, self._name, self._status, self._page, self._limit)
        except Exception as e:
            raise RuntimeError(f"Error al consultar productos: {str(e)}") from e
