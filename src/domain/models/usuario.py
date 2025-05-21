# src/domain/models/usuario.py
"""
Modelo para los usuarios del sistema.
"""
from sqlalchemy import Column, String
from domain.models.base_model import BaseModel

class Usuario(BaseModel):
    """Clase para representar un usuario del sistema."""
    
    __tablename__ = "usuarios"
    
    # Columnas específicas para usuarios
    usuario = Column(String(50), unique=True, nullable=False, index=True)  # Nombre de usuario único
    contraseña = Column(String(100), nullable=False)  # Contraseña (se recomienda hashearla)
    nombre = Column(String(100), nullable=False)  # Nombre completo del usuario
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"<Usuario(usuario='{self.usuario}', nombre='{self.nombre}')>"