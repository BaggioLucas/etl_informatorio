from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{database}'

Base = declarative_base()

class Clima(Base):
    __tablename__ = 'clima_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_ciudad = Column(Integer)
    ciudad = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    temp_max = Column(Float)
    temp_min = Column(Float)
    sensacion_termica_dia = Column(Float)
    sensacion_termica_noche = Column(Float)
    presion = Column(Integer)
    porcentaje_humedad = Column(Integer)
    descripcion_clima = Column(String)
    fecha = Column(DateTime)
