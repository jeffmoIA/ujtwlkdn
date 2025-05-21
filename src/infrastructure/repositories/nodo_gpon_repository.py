# src/infrastructure/repositories/nodo_gpon_repository.py
"""
Repositorio para el modelo NodoGPON.
"""
from domain.models.nodo_gpon import NodoGPON
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class NodoGPONRepository(SQLAlchemyRepository[NodoGPON]):
    """Repositorio para manejar operaciones CRUD de nodos GPON."""
    
    def __init__(self):
        """Constructor del repositorio."""
        super().__init__(NodoGPON)
    
    def get_by_alias(self, alias: str) -> NodoGPON:
        """
        Obtiene un nodo GPON por su alias.
        
        Args:
            alias: Alias de la OLT a buscar
            
        Returns:
            NodoGPON: El nodo encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(NodoGPON).filter(NodoGPON.alias_olt == alias).first()
    
    def get_by_ip(self, ip: str) -> NodoGPON:
        """
        Obtiene un nodo GPON por su dirección IP.
        
        Args:
            ip: Dirección IP de la OLT a buscar
            
        Returns:
            NodoGPON: El nodo encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(NodoGPON).filter(NodoGPON.ip_olt == ip).first()