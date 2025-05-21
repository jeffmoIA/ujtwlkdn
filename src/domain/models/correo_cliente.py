# src/domain/models/correo_cliente.py
"""
Modelo para las plantillas de correo para clientes.
"""
from sqlalchemy import Column, String, Text
from domain.models.base_model import BaseModel

class CorreoCliente(BaseModel):
    """Clase para representar una plantilla de correo para clientes."""
    
    __tablename__ = "correo_cliente"
    
    # Columnas específicas para plantillas de correo
    nombre = Column(String(100), unique=True, nullable=False, index=True)  # Nombre de la plantilla
    asunto = Column(String(200), nullable=False)  # Asunto del correo
    plantilla = Column(Text, nullable=False)  # Contenido de la plantilla (puede ser HTML)
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"<CorreoCliente(nombre='{self.nombre}')>"