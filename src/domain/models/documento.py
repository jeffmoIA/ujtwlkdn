# src/domain/models/documento.py
"""
Modelo para documentos de configuración.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from domain.models.base_model import BaseModel
import datetime

class Documento(BaseModel):
    """Clase para representar un documento de configuración."""
    
    __tablename__ = "documentos"
    
    # Columnas específicas para documentos
    titulo = Column(String(200), nullable=False)  # Título del documento
    cliente_id = Column(String(50), nullable=False)  # ID del cliente
    cliente_nombre = Column(String(200), nullable=False)  # Nombre del cliente
    cliente_direccion = Column(String(300), nullable=True)  # Dirección del cliente
    ancho_banda = Column(String(20), nullable=False)  # Ancho de banda (ej: "100 Mbps")
    tipo_transaccion = Column(String(50), nullable=False)  # UPGRADE, DOWNGRADE
    tipo_topologia = Column(String(50), nullable=False)  # IPRAN+MIKROTIK, IPRAN+RADWIN, etc.
    ingeniero = Column(String(100), nullable=False)  # Nombre del ingeniero
    fecha_creacion = Column(DateTime, default=datetime.datetime.now)  # Fecha de creación
    nodo_id = Column(Integer, ForeignKey("nodos_ipran.id"), nullable=True)  # ID del nodo IPRAN
    mikrotik_ip = Column(String(20), nullable=True)  # IP del Mikrotik (si aplica)
    contenido_json = Column(Text, nullable=True)  # Contenido del documento en formato JSON
    
    # Relaciones
    nodo = relationship("NodoIPRAN", backref="documentos")  # Relación con el nodo IPRAN
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"<Documento(cliente='{self.cliente_nombre}', tipo='{self.tipo_transaccion}')>"