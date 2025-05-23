# src/infrastructure/repositories/__init__.py
"""
Inicialización del módulo de repositorios.
Este archivo facilita la importación y exposición de todos los repositorios.
"""
from infrastructure.repositories.nodo_ipran_repository import NodoIPRANRepository
from infrastructure.repositories.nodo_gpon_repository import NodoGPONRepository
from infrastructure.repositories.usuario_repository import UsuarioRepository
from infrastructure.repositories.correo_cliente_repository import CorreoClienteRepository
from infrastructure.repositories.documento_repository import DocumentoRepository
from infrastructure.repositories.mikrotik_repository import MikroTikRepository  # ← NUEVO: Agregamos MikroTikRepository

# Exportamos todos los repositorios para facilitar su importación desde otros módulos
__all__ = [
    'NodoIPRANRepository', 
    'NodoGPONRepository', 
    'UsuarioRepository', 
    'CorreoClienteRepository', 
    'DocumentoRepository',
    'MikroTikRepository'  # ← NUEVO: Agregamos a la lista de exportación
]