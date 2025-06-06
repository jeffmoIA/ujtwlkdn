# src/domain/models/__init__.py
"""
Inicialización del módulo de modelos.
Este archivo facilita la importación y exposición de todos los modelos.
"""
from domain.models.base_model import BaseModel
from domain.models.nodo_ipran import NodoIPRAN
from domain.models.nodo_gpon import NodoGPON
from domain.models.usuario import Usuario
from domain.models.correo_cliente import CorreoCliente
from domain.models.documento import Documento
from domain.models.mikrotik import MikroTik  # ← NUEVO: Agregamos MikroTik

# Exportamos todos los modelos para facilitar su importación desde otros módulos
__all__ = [
    'BaseModel', 
    'NodoIPRAN', 
    'NodoGPON', 
    'Usuario', 
    'CorreoCliente', 
    'Documento',
    'MikroTik'  # ← NUEVO: Agregamos MikroTik a la lista de exportación
]