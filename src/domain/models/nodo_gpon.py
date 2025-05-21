# src/domain/models/nodo_gpon.py
"""
Modelo para los nodos de la red GPON (OLT).
"""
from sqlalchemy import Column, String
from domain.models.base_model import BaseModel

class NodoGPON(BaseModel):
    """Clase para representar un nodo GPON (OLT) en la red."""
    
    __tablename__ = "nodos_gpon"
    
    # Columnas específicas para nodos GPON
    alias_olt = Column(String(50), unique=True, nullable=False, index=True)  # Alias único de la OLT
    nombre_olt = Column(String(100), nullable=False)  # Nombre completo de la OLT
    ip_olt = Column(String(15), unique=True, nullable=False)  # Dirección IP de la OLT (formato IPv4)
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"<NodoGPON(alias='{self.alias_olt}', ip='{self.ip_olt}')>"