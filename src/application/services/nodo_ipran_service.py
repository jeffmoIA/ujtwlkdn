# src/application/services/nodo_ipran_service.py
"""
Servicio para la gestión de nodos IPRAN.
"""
from typing import List, Optional

from domain.models.nodo_ipran import NodoIPRAN
from infrastructure.repositories.nodo_ipran_repository import NodoIPRANRepository

class NodoIPRANService:
    """Servicio para manejar operaciones relacionadas con nodos IPRAN."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.repository = NodoIPRANRepository()
    
    def obtener_todos(self) -> List[NodoIPRAN]:
        """
        Obtiene todos los nodos IPRAN.
        
        Returns:
            List[NodoIPRAN]: Lista de todos los nodos IPRAN
        """
        return self.repository.get_all()
    
    def obtener_por_id(self, nodo_id: int) -> Optional[NodoIPRAN]:
        """
        Obtiene un nodo IPRAN por su ID.
        
        Args:
            nodo_id: ID del nodo a buscar
            
        Returns:
            Optional[NodoIPRAN]: El nodo encontrado o None si no existe
        """
        return self.repository.get_by_id(nodo_id)
    
    def obtener_por_alias(self, alias: str) -> Optional[NodoIPRAN]:
        """
        Obtiene un nodo IPRAN por su alias.
        
        Args:
            alias: Alias del nodo a buscar
            
        Returns:
            Optional[NodoIPRAN]: El nodo encontrado o None si no existe
        """
        return self.repository.get_by_alias(alias)
    
    def crear(self, alias: str, nombre: str, ip: str) -> NodoIPRAN:
        """
        Crea un nuevo nodo IPRAN.
        
        Args:
            alias: Alias del nodo
            nombre: Nombre completo del nodo
            ip: Dirección IP del nodo
            
        Returns:
            NodoIPRAN: El nodo creado
            
        Raises:
            ValueError: Si ya existe un nodo con el mismo alias o IP
        """
        # Verificar si ya existe un nodo con el mismo alias o IP
        if self.repository.get_by_alias(alias):
            raise ValueError(f"Ya existe un nodo con el alias '{alias}'")
        
        if self.repository.get_by_ip(ip):
            raise ValueError(f"Ya existe un nodo con la IP '{ip}'")
        
        # Crear el nuevo nodo
        nuevo_nodo = NodoIPRAN(
            alias_nodo=alias,
            nombre_nodo=nombre,
            ip_nodo=ip
        )
        
        # Guardar el nodo en la base de datos
        return self.repository.create(nuevo_nodo)
    
    def actualizar(self, nodo_id: int, alias: str, nombre: str, ip: str) -> NodoIPRAN:
        """
        Actualiza un nodo IPRAN existente.
        
        Args:
            nodo_id: ID del nodo a actualizar
            alias: Nuevo alias del nodo
            nombre: Nuevo nombre completo del nodo
            ip: Nueva dirección IP del nodo
            
        Returns:
            NodoIPRAN: El nodo actualizado
            
        Raises:
            ValueError: Si no existe un nodo con el ID especificado o si ya existe otro nodo con el mismo alias o IP
        """
        # Obtener el nodo existente
        nodo = self.repository.get_by_id(nodo_id)
        if not nodo:
            raise ValueError(f"No existe un nodo con el ID {nodo_id}")
        
        # Verificar si ya existe otro nodo con el mismo alias o IP
        nodo_mismo_alias = self.repository.get_by_alias(alias)
        if nodo_mismo_alias and nodo_mismo_alias.id != nodo_id:
            raise ValueError(f"Ya existe otro nodo con el alias '{alias}'")
        
        nodo_misma_ip = self.repository.get_by_ip(ip)
        if nodo_misma_ip and nodo_misma_ip.id != nodo_id:
            raise ValueError(f"Ya existe otro nodo con la IP '{ip}'")
        
        # Actualizar los datos del nodo
        nodo.alias_nodo = alias
        nodo.nombre_nodo = nombre
        nodo.ip_nodo = ip
        
        # Guardar los cambios en la base de datos
        return self.repository.update(nodo)
    
    def eliminar(self, nodo_id: int) -> bool:
        """
        Elimina un nodo IPRAN.
        
        Args:
            nodo_id: ID del nodo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.repository.delete(nodo_id)
    
    def buscar_por_nombre(self, nombre: str) -> List[NodoIPRAN]:
        """
        Busca nodos IPRAN por su nombre.
        
        Args:
            nombre: Texto a buscar en el nombre de los nodos
            
        Returns:
            List[NodoIPRAN]: Lista de nodos que contienen el texto en su nombre
        """
        with self.repository._get_db() as db:
            return db.query(NodoIPRAN).filter(NodoIPRAN.nombre_nodo.ilike(f"%{nombre}%")).all()