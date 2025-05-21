"""
Repositorio base para operaciones CRUD con los modelos.
Proporciona métodos comunes para todos los repositorios.
"""
from typing import TypeVar, Generic, List, Optional, Type

# Tipo genérico para los modelos
T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Clase base para todos los repositorios."""
    
    def __init__(self, session, model_class: Type[T]):
        """
        Inicializa el repositorio.
        
        Args:
            session: Sesión de SQLAlchemy para operaciones de base de datos.
            model_class: Clase del modelo con el que trabaja este repositorio.
        """
        self.session = session
        self.model_class = model_class
    
    def get_all(self) -> List[T]:
        """
        Obtiene todos los registros del modelo.
        
        Returns:
            List[T]: Lista de todos los registros.
        """
        return self.session.query(self.model_class).all()
    
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtiene un registro por su ID.
        
        Args:
            id (int): ID del registro a buscar.
            
        Returns:
            Optional[T]: El registro encontrado o None si no existe.
        """
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()
    
    def create(self, obj: T) -> T:
        """
        Crea un nuevo registro.
        
        Args:
            obj (T): Objeto a crear.
            
        Returns:
            T: El objeto creado con su ID asignado.
        """
        self.session.add(obj)
        self.session.commit()
        return obj
    
    def update(self, obj: T) -> T:
        """
        Actualiza un registro existente.
        
        Args:
            obj (T): Objeto a actualizar.
            
        Returns:
            T: El objeto actualizado.
        """
        self.session.commit()
        return obj
    
    def delete(self, obj: T) -> None:
        """
        Elimina un registro.
        
        Args:
            obj (T): Objeto a eliminar.
        """
        self.session.delete(obj)
        self.session.commit()