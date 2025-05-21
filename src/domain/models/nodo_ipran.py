# src/domain/models/nodo_ipran.py
"""
Modelo para los nodos de la red IPRAN.
"""
from sqlalchemy import Column, String
from domain.models.base_model import BaseModel

class NodoIPRAN(BaseModel):
    """Clase para representar un nodo IPRAN en la red."""
    
    __tablename__ = "nodos_ipran"
    
    # Columnas específicas para nodos IPRAN
    alias_nodo = Column(String(50), unique=True, nullable=False, index=True)  # Alias único del nodo
    nombre_nodo = Column(String(100), nullable=False)  # Nombre completo del nodo
    ip_nodo = Column(String(15), unique=True, nullable=False)  # Dirección IP del nodo (formato IPv4)
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"<NodoIPRAN(alias='{self.alias_nodo}', ip='{self.ip_nodo}')>"