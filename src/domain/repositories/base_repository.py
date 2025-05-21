# src/domain/repositories/base_repository.py
"""
Interfaz base para los repositorios.
Define los métodos que deben implementar todos los repositorios.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any, Dict

# Definimos un tipo genérico T para representar cualquier modelo
T = TypeVar('T')

class BaseRepository(Generic[T], ABC):
    """Clase abstracta base para todos los repositorios."""
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad a buscar
            
        Returns:
            Optional[T]: La entidad encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.
        
        Returns:
            List[T]: Lista de todas las entidades
        """
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """
        Crea una nueva entidad.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            T: La entidad creada con su ID asignado
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        
        Args:
            entity: Entidad con los datos actualizados
            
        Returns:
            T: La entidad actualizada
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """
        Elimina una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def find_by(self, **kwargs) -> List[T]:
        """
        Busca entidades que cumplan con los criterios especificados.
        
        Args:
            **kwargs: Criterios de búsqueda (atributos y valores)
            
        Returns:
            List[T]: Lista de entidades que cumplen con los criterios
        """
        pass