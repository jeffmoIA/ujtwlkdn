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
    
    def actualizar(self, nodo_id: int, alias: str, nombre: str, ip: str) -> NodoGPON:
        """
        Actualiza un nodo GPON existente.
        
        Args:
            nodo_id: ID del nodo a actualizar
            alias: Nuevo alias de la OLT
            nombre: Nuevo nombre completo de la OLT
            ip: Nueva dirección IP de la OLT
            
        Returns:
            NodoGPON: El nodo actualizado
            
        Raises:
            ValueError: Si no existe un nodo con el ID especificado o si ya existe otro nodo con el mismo alias o IP
        """
        # Obtener el nodo existente
        nodo = self.repository.get_by_id(nodo_id)
        if not nodo:
            raise ValueError(f"No existe una OLT con el ID {nodo_id}")
        
        # Verificar si ya existe otro nodo con el mismo alias o IP
        nodo_mismo_alias = self.repository.get_by_alias(alias)
        if nodo_mismo_alias and nodo_mismo_alias.id != nodo_id:
            raise ValueError(f"Ya existe otra OLT con el alias '{alias}'")
        
        nodo_misma_ip = self.repository.get_by_ip(ip)
        if nodo_misma_ip and nodo_misma_ip.id != nodo_id:
            raise ValueError(f"Ya existe otra OLT con la IP '{ip}'")
        
        # Actualizar los datos del nodo
        nodo.alias_olt = alias
        nodo.nombre_olt = nombre
        nodo.ip_olt = ip
        
        # Guardar los cambios en la base de datos
        return self.repository.update(nodo)
    
    def eliminar(self, nodo_id: int) -> bool:
        """
        Elimina un nodo GPON.
        
        Args:
            nodo_id: ID del nodo a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.repository.delete(nodo_id)
    
    def buscar_por_nombre(self, nombre: str) -> List[NodoGPON]:
        """
        Busca nodos GPON por su nombre.
        
        Args:
            nombre: Texto a buscar en el nombre de los nodos
            
        Returns:
            List[NodoGPON]: Lista de nodos que contienen el texto en su nombre
        """
        with self.repository._get_db() as db:
            return db.query(NodoGPON).filter(NodoGPON.nombre_olt.ilike(f"%{nombre}%")).all()
    
    def obtener_por_ip(self, ip: str) -> Optional[NodoGPON]:
        """
        Obtiene un nodo GPON por su dirección IP.
        
        Args:
            ip: Dirección IP de la OLT a buscar
            
        Returns:
            Optional[NodoGPON]: El nodo encontrado o None si no existe
        """
        return self.repository.get_by_ip(ip)
    
    def validar_ip(self, ip: str) -> bool:
        """
        Valida si una dirección IP tiene el formato correcto.
        
        Args:
            ip: Dirección IP a validar
            
        Returns:
            bool: True si la IP es válida, False en caso contrario
        """
        import re
        # Expresión regular para validar IPv4
        patron = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        return bool(re.match(patron, ip))
    
    def contar_nodos(self) -> int:
        """
        Cuenta el total de nodos GPON en la base de datos.
        
        Returns:
            int: Número total de nodos GPON
        """
        return len(self.repository.get_all())