from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import Table, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, nullable=False, unique=True)
    inventario = Column(Integer, nullable=False, default=0)
