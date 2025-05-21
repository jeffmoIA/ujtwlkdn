# src/infrastructure/repositories/sqlalchemy_repository.py
"""
Implementación base de repositorio usando SQLAlchemy.
Esta clase implementa los métodos básicos de repositorio utilizando SQLAlchemy.
"""
from typing import Generic, TypeVar, List, Optional, Type, Dict, Any
from sqlalchemy.orm import Session

from domain.repositories.base_repository import BaseRepository
from infrastructure.database.config import SessionLocal

# Tipo genérico para los modelos
T = TypeVar('T')

class SQLAlchemyRepository(BaseRepository[T], Generic[T]):
    """Implementación base de repositorio con SQLAlchemy."""
    
    def __init__(self, model_class: Type[T]):
        """
        Constructor del repositorio.
        
        Args:
            model_class: Clase del modelo que manejará este repositorio
        """
        self.model_class = model_class
    
    def _get_db(self) -> Session:
        """
        Obtiene una sesión de base de datos.
        
        Returns:
            Session: Sesión de SQLAlchemy
        """
        return SessionLocal()
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad a buscar
            
        Returns:
            Optional[T]: La entidad encontrada o None si no existe
        """
        with self._get_db() as db:
            return db.query(self.model_class).filter(self.model_class.id == entity_id).first()
    
    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.
        
        Returns:
            List[T]: Lista de todas las entidades
        """
        with self._get_db() as db:
            return db.query(self.model_class).all()
    
    def create(self, entity: T) -> T:
        """
        Crea una nueva entidad.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            T: La entidad creada con su ID asignado
        """
        with self._get_db() as db:
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
    
    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        
        Args:
            entity: Entidad con los datos actualizados
            
        Returns:
            T: La entidad actualizada
        """
        with self._get_db() as db:
            db.merge(entity)
            db.commit()
            db.refresh(entity)
            return entity
    
    def delete(self, entity_id: int) -> bool:
        """
        Elimina una entidad por su ID.
        
        Args:
            entity_id: ID de la entidad a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        with self._get_db() as db:
            entity = db.query(self.model_class).filter(self.model_class.id == entity_id).first()
            if entity:
                db.delete(entity)
                db.commit()
                return True
            return False
    
    def find_by(self, **kwargs) -> List[T]:
        """
        Busca entidades que cumplan con los criterios especificados.
        
        Args:
            **kwargs: Criterios de búsqueda (atributos y valores)
            
        Returns:
            List[T]: Lista de entidades que cumplen con los criterios
        """
        with self._get_db() as db:
            query = db.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.all()