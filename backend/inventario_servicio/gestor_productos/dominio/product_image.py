import uuid

from infraestructura.database import db
from sqlalchemy.orm import relationship

class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), primary_key=False, default=lambda: str(uuid.uuid4()))
    imagen_url = db.Column(db.String(255), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)

    producto = relationship("Product", back_populates="imagenes")

    def to_dict(self):
        return {
            "id": self.id,
            "imagen_url": self.imagen_url
        }