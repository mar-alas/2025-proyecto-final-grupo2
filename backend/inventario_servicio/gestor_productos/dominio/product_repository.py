from typing import Protocol
from .product_dto import ProductDTO
from .product_mapper import to_model

class IDatabaseSession(Protocol):
    def query(self, model): ...
    def add(self, instance): ...
    def commit(self): ...


class ProductRepository:
    """Repositorio para manejar la persistencia de productos."""

    def __init__(self, db_session: IDatabaseSession, product_model_class, product_image_model_class):
        """Permite inyectar una sesión de base de datos."""
        self.db_session = db_session
        self.product_model_class = product_model_class 
        self.product_image_model_class = product_image_model_class

    def get_by_name(self, name: str):
        return self.db_session.query(self.product_model_class).filter_by(nombre=name).first()
    
    def save(self, product_dto: ProductDTO):
        product_instance = to_model(
            product_dto,
            self.product_model_class,
            self.product_image_model_class
        )
        
        self.db_session.add(product_instance)
        self.db_session.commit()

        return product_instance
    
    # def get_all(self):
    #    return self.db_session.query(self.product_model_class).all()
    
    def get_all(self, code=None, name=None, status=None, page=1, limit=20):
        query = self.db_session.query(self.product_model_class)

        if code:
            query = query.filter(self.product_model_class.id == code)
        if name:
            query = query.filter(self.product_model_class.nombre.ilike(f"%{name}%"))
        if status:
            query = query.filter(self.product_model_class.estado == status)

        total = query.count()
        productos = query.order_by(self.product_model_class.id.desc()) \
                         .offset((page - 1) * limit) \
                         .limit(limit) \
                         .all()

        return productos, total