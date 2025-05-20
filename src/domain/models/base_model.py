"""
Modelo base para todas las entidades de la aplicación.
Proporciona funcionalidad común a todos los modelos.
"""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from infrastructure.database.config import Base

class BaseModel(Base):
    """Clase base abstracta para todos los modelos."""
    
    __abstract__ = True  # Esta línea hace que SQLAlchemy no cree una tabla para esta clase
    
    # Columnas comunes para todos los modelos
    id = Column(Integer, primary_key=True, autoincrement=True)  # ID único
    created_at = Column(DateTime, default=func.current_timestamp())  # Fecha de creación
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())  # Fecha de actualización