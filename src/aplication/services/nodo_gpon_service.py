# src/application/services/nodo_gpon_service.py
"""
Servicio para la gestión de nodos GPON.
"""
from typing import List, Optional

from domain.models.nodo_gpon import NodoGPON
from infrastructure.repositories.nodo_gpon_repository import NodoGPONRepository

class NodoGPONService:
    """Servicio para manejar operaciones relacionadas con nodos GPON."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.repository = NodoGPONRepository()
    
    def obtener_todos(self) -> List[NodoGPON]:
        """
        Obtiene todos los nodos GPON.
        
        Returns:
            List[NodoGPON]: Lista de todos los nodos GPON
        """
        return self.repository.get_all()
    
    def obtener_por_id(self, nodo_id: int) -> Optional[NodoGPON]:
        """
        Obtiene un nodo GPON por su ID.
        
        Args:
            nodo_id: ID del nodo a buscar
            
        Returns:
            Optional[NodoGPON]: El nodo encontrado o None si no existe
        """
        return self.repository.get_by_id(nodo_id)
    
    def obtener_por_alias(self, alias: str) -> Optional[NodoGPON]:
        """
        Obtiene un nodo GPON por su alias.
        
        Args:
            alias: Alias de la OLT a buscar
            
        Returns:
            Optional[NodoGPON]: El nodo encontrado o None si no existe
        """
        return self.repository.get_by_alias(alias)
    
    def crear(self, alias: str, nombre: str, ip: str) -> NodoGPON:
        """
        Crea un nuevo nodo GPON.
        
        Args:
            alias: Alias de la OLT
            nombre: Nombre completo de la OLT
            ip: Dirección IP de la OLT
            
        Returns:
            NodoGPON: El nodo creado
            
        Raises:
            ValueError: Si ya existe un nodo con el mismo alias o IP
        """
        # Verificar si ya existe un nodo con el mismo alias o IP
        if self.repository.get_by_alias(alias):
            raise ValueError(f"Ya existe una OLT con el alias '{alias}'")
        
        if self.repository.get_by_ip(ip):
            raise ValueError(f"Ya existe una OLT con la IP '{ip}'")
        
        # Crear el nuevo nodo
        nuevo_nodo = NodoGPON(
            alias_olt=alias,
            nombre_olt=nombre,
            ip_olt=ip
        )
        
        # Guardar el nodo en la base de datos
        return self.repository.create(nuevo_nodo)
    
    # [Resto de métodos similares a NodoIPRANService]