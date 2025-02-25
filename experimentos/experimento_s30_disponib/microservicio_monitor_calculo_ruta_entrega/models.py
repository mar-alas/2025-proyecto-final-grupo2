from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import json

Base = declarative_base()

class Ruta(Base):
    __tablename__ = 'rutas_calculadas'
    
    id = Column(Integer, primary_key=True)
    ruta_sin_calcular = Column(String)
    ruta_calculada = Column(String)
    calculo_correcto = Column(Boolean)
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
    tuvo_correccion = Column(Boolean, default=False)

    def dar_ruta_sin_calcular(self):
        return json.loads(self.ruta_sin_calcular)

    def dar_ruta_calculada(self):
        return json.loads(self.ruta_calculada)

class RutaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ruta
        include_relationships = True
        load_instance = True
    

# Create database and tables
engine = create_engine('postgresql://admin:admin@rutas-db-container:5432/rutas-db')
Base.metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)
