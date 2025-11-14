from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PQRS(Base):
    __tablename__ = "pqrs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    tipo = Column(String(50), nullable=False)
    asunto = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_creacion = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
