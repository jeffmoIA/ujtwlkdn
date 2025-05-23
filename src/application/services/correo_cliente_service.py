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
    
    def actualizar(self, plantilla_id: int, nombre: str, asunto: str, contenido: str) -> CorreoCliente:
        """
        Actualiza una plantilla de correo existente.
        
        Args:
            plantilla_id: ID de la plantilla a actualizar
            nombre: Nuevo nombre de la plantilla
            asunto: Nuevo asunto del correo
            contenido: Nuevo contenido de la plantilla
            
        Returns:
            CorreoCliente: La plantilla actualizada
            
        Raises:
            ValueError: Si no existe una plantilla con el ID especificado o si ya existe otra plantilla con el mismo nombre
        """
        # Obtener la plantilla existente
        plantilla = self.repository.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError(f"No existe una plantilla con el ID {plantilla_id}")
        
        # Verificar si ya existe otra plantilla con el mismo nombre
        plantilla_mismo_nombre = self.repository.get_by_nombre(nombre)
        if plantilla_mismo_nombre and plantilla_mismo_nombre.id != plantilla_id:
            raise ValueError(f"Ya existe otra plantilla con el nombre '{nombre}'")
        
        # Actualizar los datos de la plantilla
        plantilla.nombre = nombre
        plantilla.asunto = asunto
        plantilla.plantilla = contenido
        
        # Guardar los cambios en la base de datos
        return self.repository.update(plantilla)
    
    def eliminar(self, plantilla_id: int) -> bool:
        """
        Elimina una plantilla de correo.
        
        Args:
            plantilla_id: ID de la plantilla a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.repository.delete(plantilla_id)
    
    def buscar_por_texto(self, texto: str) -> List[CorreoCliente]:
        """
        Busca plantillas por texto en nombre, asunto o contenido.
        
        Args:
            texto: Texto a buscar
            
        Returns:
            List[CorreoCliente]: Lista de plantillas que contienen el texto
        """
        with self.repository._get_db() as db:
            # Buscar en nombre, asunto y contenido de la plantilla
            return db.query(CorreoCliente).filter(
                db.or_(
                    CorreoCliente.nombre.ilike(f"%{texto}%"),
                    CorreoCliente.asunto.ilike(f"%{texto}%"),
                    CorreoCliente.plantilla.ilike(f"%{texto}%")
                )
            ).all()
    
    def duplicar_plantilla(self, plantilla_id: int, nuevo_nombre: str) -> CorreoCliente:
        """
        Duplica una plantilla existente con un nuevo nombre.
        
        Args:
            plantilla_id: ID de la plantilla a duplicar
            nuevo_nombre: Nombre para la nueva plantilla
            
        Returns:
            CorreoCliente: La nueva plantilla duplicada
            
        Raises:
            ValueError: Si no existe la plantilla original o si ya existe una plantilla con el nuevo nombre
        """
        # Obtener la plantilla original
        plantilla_original = self.repository.get_by_id(plantilla_id)
        if not plantilla_original:
            raise ValueError(f"No existe una plantilla con el ID {plantilla_id}")
        
        # Verificar que el nuevo nombre no esté en uso
        if self.repository.get_by_nombre(nuevo_nombre):
            raise ValueError(f"Ya existe una plantilla con el nombre '{nuevo_nombre}'")
        
        # Crear la nueva plantilla duplicada
        plantilla_duplicada = CorreoCliente(
            nombre=nuevo_nombre,
            asunto=plantilla_original.asunto,
            plantilla=plantilla_original.plantilla
        )
        
        # Guardar la plantilla duplicada
        return self.repository.create(plantilla_duplicada)
    
    def procesar_plantilla(self, plantilla_id: int, variables: dict) -> dict:
        """
        Procesa una plantilla reemplazando variables con valores específicos.
        
        Args:
            plantilla_id: ID de la plantilla a procesar
            variables: Diccionario con las variables a reemplazar
                      Ejemplo: {"CLIENTE_NOMBRE": "Juan Pérez", "ANCHO_BANDA": "100 Mbps"}
            
        Returns:
            dict: Diccionario con el asunto y contenido procesados
            
        Raises:
            ValueError: Si no existe la plantilla
        """
        # Obtener la plantilla
        plantilla = self.repository.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError(f"No existe una plantilla con el ID {plantilla_id}")
        
        # Procesar el asunto
        asunto_procesado = plantilla.asunto
        for variable, valor in variables.items():
            asunto_procesado = asunto_procesado.replace(f"[{variable}]", str(valor))
        
        # Procesar el contenido
        contenido_procesado = plantilla.plantilla
        for variable, valor in variables.items():
            contenido_procesado = contenido_procesado.replace(f"[{variable}]", str(valor))
        
        return {
            "asunto": asunto_procesado,
            "contenido": contenido_procesado,
            "plantilla_original": plantilla.nombre
        }
    
    def obtener_variables_plantilla(self, plantilla_id: int) -> List[str]:
        """
        Extrae las variables definidas en una plantilla.
        
        Args:
            plantilla_id: ID de la plantilla
            
        Returns:
            List[str]: Lista de variables encontradas en la plantilla
            
        Raises:
            ValueError: Si no existe la plantilla
        """
        # Obtener la plantilla
        plantilla = self.repository.get_by_id(plantilla_id)
        if not plantilla:
            raise ValueError(f"No existe una plantilla con el ID {plantilla_id}")
        
        import re
        
        # Buscar variables en formato [VARIABLE] en asunto y contenido
        texto_completo = plantilla.asunto + " " + plantilla.plantilla
        variables = re.findall(r'\[([A-Z_]+)\]', texto_completo)
        
        # Eliminar duplicados y ordenar
        return sorted(list(set(variables)))
    
    def contar_plantillas(self) -> int:
        """
        Cuenta el total de plantillas en la base de datos.
        
        Returns:
            int: Número total de plantillas
        """
        return len(self.repository.get_all())
    
    def validar_plantilla(self, nombre: str, asunto: str, contenido: str) -> List[str]:
        """
        Valida una plantilla antes de guardarla.
        
        Args:
            nombre: Nombre de la plantilla
            asunto: Asunto del correo
            contenido: Contenido de la plantilla
            
        Returns:
            List[str]: Lista de errores de validación (vacía si es válida)
        """
        errores = []
        
        # Validar nombre
        if not nombre or len(nombre.strip()) == 0:
            errores.append("El nombre de la plantilla es obligatorio")
        elif len(nombre.strip()) > 100:
            errores.append("El nombre de la plantilla no puede exceder 100 caracteres")
        
        # Validar asunto
        if not asunto or len(asunto.strip()) == 0:
            errores.append("El asunto del correo es obligatorio")
        elif len(asunto.strip()) > 200:
            errores.append("El asunto no puede exceder 200 caracteres")
        
        # Validar contenido
        if not contenido or len(contenido.strip()) == 0:
            errores.append("El contenido de la plantilla es obligatorio")
        elif len(contenido.strip()) > 10000:
            errores.append("El contenido no puede exceder 10,000 caracteres")
        
        return errores