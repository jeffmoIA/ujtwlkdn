# src/application/services/documento_service.py
"""
Servicio para la gestión de documentos.
"""
import json
import os
import datetime
from typing import List, Optional, Dict, Any

from domain.models.documento import Documento
from infrastructure.repositories.documento_repository import DocumentoRepository
from application.services.nodo_ipran_service import NodoIPRANService

class DocumentoService:
    """Servicio para manejar operaciones relacionadas con documentos."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.repository = DocumentoRepository()
        self.nodo_service = NodoIPRANService()
        # Directorio donde se guardarán las plantillas y documentos exportados
        self.docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "recursos", "documentos")
        # Crear el directorio si no existe
        os.makedirs(self.docs_dir, exist_ok=True)
    
    def obtener_todos(self) -> List[Documento]:
        """
        Obtiene todos los documentos.
        
        Returns:
            List[Documento]: Lista de todos los documentos
        """
        return self.repository.get_all()
    
    def obtener_por_id(self, documento_id: int) -> Optional[Documento]:
        """
        Obtiene un documento por su ID.
        
        Args:
            documento_id: ID del documento a buscar
            
        Returns:
            Optional[Documento]: El documento encontrado o None si no existe
        """
        return self.repository.get_by_id(documento_id)
    
    def obtener_por_cliente_id(self, cliente_id: str) -> List[Documento]:
        """
        Obtiene documentos por ID de cliente.
        
        Args:
            cliente_id: ID del cliente a buscar
            
        Returns:
            List[Documento]: Lista de documentos encontrados
        """
        return self.repository.get_by_cliente_id(cliente_id)
    
    def crear(self, 
              titulo: str,
              cliente_id: str, 
              cliente_nombre: str, 
              cliente_direccion: str,
              ancho_banda: str,
              tipo_transaccion: str,
              tipo_topologia: str,
              ingeniero: str,
              nodo_id: Optional[int] = None,
              mikrotik_ip: Optional[str] = None,
              contenido_json: Optional[Dict[str, Any]] = None) -> Documento:
        """
        Crea un nuevo documento.
        
        Args:
            titulo: Título del documento
            cliente_id: ID del cliente
            cliente_nombre: Nombre completo del cliente
            cliente_direccion: Dirección del cliente
            ancho_banda: Ancho de banda (ej: "100 Mbps")
            tipo_transaccion: Tipo de transacción (UPGRADE, DOWNGRADE)
            tipo_topologia: Tipo de topología (IPRAN+MIKROTIK, etc.)
            ingeniero: Nombre del ingeniero
            nodo_id: ID del nodo IPRAN (opcional)
            mikrotik_ip: IP del Mikrotik (opcional)
            contenido_json: Contenido adicional en formato JSON (opcional)
            
        Returns:
            Documento: El documento creado
        """
        # Convertir contenido_json a texto si no es None
        json_content = None
        if contenido_json is not None:
            json_content = json.dumps(contenido_json)
        
        # Crear el nuevo documento
        nuevo_documento = Documento(
            titulo=titulo,
            cliente_id=cliente_id,
            cliente_nombre=cliente_nombre,
            cliente_direccion=cliente_direccion,
            ancho_banda=ancho_banda,
            tipo_transaccion=tipo_transaccion,
            tipo_topologia=tipo_topologia,
            ingeniero=ingeniero,
            nodo_id=nodo_id,
            mikrotik_ip=mikrotik_ip,
            contenido_json=json_content
        )
        
        # Guardar el documento en la base de datos
        return self.repository.create(nuevo_documento)
    
    def actualizar(self, 
                  documento_id: int,
                  titulo: Optional[str] = None,
                  cliente_id: Optional[str] = None,
                  cliente_nombre: Optional[str] = None,
                  cliente_direccion: Optional[str] = None,
                  ancho_banda: Optional[str] = None,
                  tipo_transaccion: Optional[str] = None,
                  tipo_topologia: Optional[str] = None,
                  ingeniero: Optional[str] = None,
                  nodo_id: Optional[int] = None,
                  mikrotik_ip: Optional[str] = None,
                  contenido_json: Optional[Dict[str, Any]] = None) -> Optional[Documento]:
        """
        Actualiza un documento existente.
        
        Args:
            documento_id: ID del documento a actualizar
            [Campos opcionales a actualizar]
            
        Returns:
            Optional[Documento]: El documento actualizado o None si no existe
        """
        # Obtener el documento existente
        documento = self.repository.get_by_id(documento_id)
        if not documento:
            return None
        
        # Actualizar los campos si se proporcionan
        if titulo:
            documento.titulo = titulo
        if cliente_id:
            documento.cliente_id = cliente_id
        if cliente_nombre:
            documento.cliente_nombre = cliente_nombre
        if cliente_direccion:
            documento.cliente_direccion = cliente_direccion
        if ancho_banda:
            documento.ancho_banda = ancho_banda
        if tipo_transaccion:
            documento.tipo_transaccion = tipo_transaccion
        if tipo_topologia:
            documento.tipo_topologia = tipo_topologia
        if ingeniero:
            documento.ingeniero = ingeniero
        if nodo_id is not None:
            documento.nodo_id = nodo_id
        if mikrotik_ip:
            documento.mikrotik_ip = mikrotik_ip
        if contenido_json is not None:
            documento.contenido_json = json.dumps(contenido_json)
        
        # Guardar los cambios
        return self.repository.update(documento)
    
    def eliminar(self, documento_id: int) -> bool:
        """
        Elimina un documento.
        
        Args:
            documento_id: ID del documento a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        return self.repository.delete(documento_id)
    
    def generar_etiqueta_cliente(self, cliente_id: str, cliente_nombre: str, ancho_banda: str) -> str:
        """
        Genera la etiqueta de identificación del cliente.
        
        Args:
            cliente_id: ID del cliente
            cliente_nombre: Nombre del cliente
            ancho_banda: Ancho de banda
            
        Returns:
            str: Etiqueta generada (formato: ID)NOMBRE - INTERNET - ANCHO_BANDA)
        """
        return f"{cliente_id}){cliente_nombre} - INTERNET - {ancho_banda}"
    
    def generar_texto_correo(self, cliente_id: str, cliente_nombre: str, cliente_direccion: str, 
                             ancho_banda: str, tipo_transaccion: str) -> Dict[str, str]:
        """
        Genera el texto para el correo de notificación.
        
        Args:
            cliente_id: ID del cliente
            cliente_nombre: Nombre del cliente
            cliente_direccion: Dirección del cliente
            ancho_banda: Ancho de banda
            tipo_transaccion: Tipo de transacción (UPGRADE, DOWNGRADE)
            
        Returns:
            Dict[str, str]: Diccionario con el asunto y cuerpo del correo
        """
        # Asunto del correo
        asunto = f"{tipo_transaccion.capitalize()} a {ancho_banda} - {cliente_id} - {cliente_nombre}"
        
        # Cuerpo del correo
        if tipo_transaccion.upper() == "UPGRADE":
            cuerpo = f"""Buen día estimado cliente

Es un gusto saludarle, el motivo de este correo es para poderle notificar que se ha aplicado un upgrade a {ancho_banda} sobre su enlace con ID {cliente_id} ubicado en {cliente_direccion}

Upgrade queda aplicado inmediatamente por lo que desde este momento ya cuenta con {ancho_banda} su servicio.

Saludos Cordiales
"""
        else:  # DOWNGRADE
            cuerpo = f"""Buen día estimado cliente

Es un gusto saludarle, el motivo de este correo es para poderle notificar que se ha aplicado un downgrade a {ancho_banda} sobre su enlace con ID {cliente_id} ubicado en {cliente_direccion}

Downgrade queda aplicado inmediatamente por lo que desde este momento su servicio cuenta con {ancho_banda}.

Saludos Cordiales
"""
        
        return {
            "asunto": asunto,
            "cuerpo": cuerpo
        }