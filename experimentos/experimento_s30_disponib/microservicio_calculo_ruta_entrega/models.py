from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

Base = declarative_base()

class Ruta(Base):
    __tablename__ = 'rutas_calculadas'
    
    id = Column(Integer, primary_key=True)
    ruta_sin_calcular = Column(String)
    ruta_calculada = Column(String)
    calculo_correcto = Column(Boolean)
    fecha_creacion = Column(DateTime, default=datetime.now())
    fecha_actualizacion = Column(DateTime, default=datetime.now())
    tuvo_correccion = Column(Boolean, default=False)

class RutaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ruta
        include_relationships = True
        load_instance = True
    

# Create database and tables
engine = create_engine('postgresql://0.0.0.0:5432/rutas-db')
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
