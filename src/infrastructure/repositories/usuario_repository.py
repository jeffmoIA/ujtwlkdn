# src/infrastructure/repositories/usuario_repository.py
"""
Repositorio para el modelo Usuario.
"""
from domain.models.usuario import Usuario
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class UsuarioRepository(SQLAlchemyRepository[Usuario]):
    """Repositorio para manejar operaciones CRUD de usuarios."""
    
    def __init__(self):
        """Constructor del repositorio."""
        super().__init__(Usuario)
    
    def get_by_username(self, username: str) -> Usuario:
        """
        Obtiene un usuario por su nombre de usuario.
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            Usuario: El usuario encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(Usuario).filter(Usuario.usuario == username).first()