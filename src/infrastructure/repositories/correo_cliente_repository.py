# src/infrastructure/repositories/correo_cliente_repository.py
"""
Repositorio para el modelo CorreoCliente.
"""
from domain.models.correo_cliente import CorreoCliente
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class CorreoClienteRepository(SQLAlchemyRepository[CorreoCliente]):
    """Repositorio para manejar operaciones CRUD de plantillas de correo."""
    
    def __init__(self):
        """Constructor del repositorio."""
        super().__init__(CorreoCliente)
    
    def get_by_nombre(self, nombre: str) -> CorreoCliente:
        """
        Obtiene una plantilla de correo por su nombre.
        
        Args:
            nombre: Nombre de la plantilla a buscar
            
        Returns:
            CorreoCliente: La plantilla encontrada o None si no existe
        """
        with self._get_db() as db:
            return db.query(CorreoCliente).filter(CorreoCliente.nombre == nombre).first()