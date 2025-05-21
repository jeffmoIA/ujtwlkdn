# src/application/services/correo_cliente_service.py
"""
Servicio para la gestión de plantillas de correo.
"""
from typing import List, Optional

from domain.models.correo_cliente import CorreoCliente
from infrastructure.repositories.correo_cliente_repository import CorreoClienteRepository

class CorreoClienteService:
    """Servicio para manejar operaciones relacionadas con plantillas de correo."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.repository = CorreoClienteRepository()
    
    def obtener_todas(self) -> List[CorreoCliente]:
        """
        Obtiene todas las plantillas de correo.
        
        Returns:
            List[CorreoCliente]: Lista de todas las plantillas de correo
        """
        return self.repository.get_all()
    
    def obtener_por_id(self, plantilla_id: int) -> Optional[CorreoCliente]:
        """
        Obtiene una plantilla de correo por su ID.
        
        Args:
            plantilla_id: ID de la plantilla a buscar
            
        Returns:
            Optional[CorreoCliente]: La plantilla encontrada o None si no existe
        """
        return self.repository.get_by_id(plantilla_id)
    
    def obtener_por_nombre(self, nombre: str) -> Optional[CorreoCliente]:
        """
        Obtiene una plantilla de correo por su nombre.
        
        Args:
            nombre: Nombre de la plantilla a buscar
            
        Returns:
            Optional[CorreoCliente]: La plantilla encontrada o None si no existe
        """
        return self.repository.get_by_nombre(nombre)
    
    def crear(self, nombre: str, asunto: str, contenido: str) -> CorreoCliente:
        """
        Crea una nueva plantilla de correo.
        
        Args:
            nombre: Nombre de la plantilla
            asunto: Asunto del correo
            contenido: Contenido de la plantilla
            
        Returns:
            CorreoCliente: La plantilla creada
            
        Raises:
            ValueError: Si ya existe una plantilla con el mismo nombre
        """
        # Verificar si ya existe una plantilla con el mismo nombre
        if self.repository.get_by_nombre(nombre):
            raise ValueError(f"Ya existe una plantilla con el nombre '{nombre}'")
        
        # Crear la nueva plantilla
        nueva_plantilla = CorreoCliente(
            nombre=nombre,
            asunto=asunto,
            plantilla=contenido
        )
        
        # Guardar la plantilla en la base de datos
        return self.repository.create(nueva_plantilla)
    
    # [Resto de métodos similares a los anteriores]