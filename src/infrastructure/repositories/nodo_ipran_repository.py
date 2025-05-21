# src/infrastructure/repositories/nodo_ipran_repository.py
"""
Repositorio para el modelo NodoIPRAN.
"""
from domain.models.nodo_ipran import NodoIPRAN
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class NodoIPRANRepository(SQLAlchemyRepository[NodoIPRAN]):
    """Repositorio para manejar operaciones CRUD de nodos IPRAN."""
    
    def __init__(self):
        """Constructor del repositorio."""
        super().__init__(NodoIPRAN)
    
    def get_by_alias(self, alias: str) -> NodoIPRAN:
        """
        Obtiene un nodo IPRAN por su alias.
        
        Args:
            alias: Alias del nodo a buscar
            
        Returns:
            NodoIPRAN: El nodo encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(NodoIPRAN).filter(NodoIPRAN.alias_nodo == alias).first()
    
    def get_by_ip(self, ip: str) -> NodoIPRAN:
        """
        Obtiene un nodo IPRAN por su dirección IP.
        
        Args:
            ip: Dirección IP del nodo a buscar
            
        Returns:
            NodoIPRAN: El nodo encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(NodoIPRAN).filter(NodoIPRAN.ip_nodo == ip).first()