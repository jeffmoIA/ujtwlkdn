# src/infrastructure/repositories/documento_repository.py
"""
Repositorio para el modelo Documento.
Este repositorio maneja todas las operaciones de base de datos para los documentos.
"""
from typing import List, Optional
from domain.models.documento import Documento
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class DocumentoRepository(SQLAlchemyRepository[Documento]):
    """Repositorio para manejar operaciones CRUD de documentos."""
    
    def __init__(self):
        """Constructor del repositorio."""
        # Llamamos al constructor padre pasando la clase del modelo
        super().__init__(Documento)
    
    def get_by_cliente_id(self, cliente_id: str) -> List[Documento]:
        """
        Obtiene todos los documentos de un cliente específico.
        
        Args:
            cliente_id: ID del cliente a buscar
            
        Returns:
            List[Documento]: Lista de documentos del cliente
        """
        # Usar el contexto de base de datos para hacer la consulta
        with self._get_db() as db:
            return db.query(Documento).filter(
                Documento.cliente_id == cliente_id
            ).order_by(
                Documento.fecha_creacion.desc()  # Ordenar por fecha descendente (más recientes primero)
            ).all()
    
    def get_by_tipo_transaccion(self, tipo_transaccion: str) -> List[Documento]:
        """
        Obtiene todos los documentos de un tipo de transacción específico.
        
        Args:
            tipo_transaccion: Tipo de transacción a buscar (UPGRADE, DOWNGRADE)
            
        Returns:
            List[Documento]: Lista de documentos del tipo especificado
        """
        with self._get_db() as db:
            return db.query(Documento).filter(
                Documento.tipo_transaccion == tipo_transaccion
            ).order_by(
                Documento.fecha_creacion.desc()
            ).all()
    
    def get_by_ingeniero(self, ingeniero: str) -> List[Documento]:
        """
        Obtiene todos los documentos creados por un ingeniero específico.
        
        Args:
            ingeniero: Nombre del ingeniero
            
        Returns:
            List[Documento]: Lista de documentos del ingeniero
        """
        with self._get_db() as db:
            return db.query(Documento).filter(
                Documento.ingeniero.ilike(f"%{ingeniero}%")  # ilike = búsqueda insensible a mayúsculas
            ).order_by(
                Documento.fecha_creacion.desc()
            ).all()
    
    def get_by_nodo_id(self, nodo_id: int) -> List[Documento]:
        """
        Obtiene todos los documentos asociados a un nodo IPRAN específico.
        
        Args:
            nodo_id: ID del nodo IPRAN
            
        Returns:
            List[Documento]: Lista de documentos asociados al nodo
        """
        with self._get_db() as db:
            return db.query(Documento).filter(
                Documento.nodo_id == nodo_id
            ).order_by(
                Documento.fecha_creacion.desc()
            ).all()
    
    def search_by_text(self, search_text: str) -> List[Documento]:
        """
        Busca documentos que contengan el texto especificado en varios campos.
        
        Args:
            search_text: Texto a buscar
            
        Returns:
            List[Documento]: Lista de documentos que contienen el texto
        """
        with self._get_db() as db:
            # Convertir el texto de búsqueda a minúsculas para búsqueda insensible a mayúsculas
            search_pattern = f"%{search_text.lower()}%"
            
            return db.query(Documento).filter(
                # Buscar en múltiples campos usando OR
                db.or_(
                    Documento.titulo.ilike(search_pattern),          # En el título
                    Documento.cliente_id.ilike(search_pattern),      # En el ID del cliente
                    Documento.cliente_nombre.ilike(search_pattern),  # En el nombre del cliente
                    Documento.cliente_direccion.ilike(search_pattern), # En la dirección
                    Documento.ingeniero.ilike(search_pattern),       # En el nombre del ingeniero
                    Documento.tipo_transaccion.ilike(search_pattern), # En el tipo de transacción
                    Documento.tipo_topologia.ilike(search_pattern)   # En el tipo de topología
                )
            ).order_by(
                Documento.fecha_creacion.desc()
            ).all()
    
    def get_recent_documents(self, limit: int = 10) -> List[Documento]:
        """
        Obtiene los documentos más recientes.
        
        Args:
            limit: Número máximo de documentos a retornar (por defecto 10)
            
        Returns:
            List[Documento]: Lista de documentos más recientes
        """
        with self._get_db() as db:
            return db.query(Documento).order_by(
                Documento.fecha_creacion.desc()
            ).limit(limit).all()
    
    def get_documents_by_date_range(self, fecha_inicio, fecha_fin) -> List[Documento]:
        """
        Obtiene documentos creados en un rango de fechas específico.
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            
        Returns:
            List[Documento]: Lista de documentos en el rango de fechas
        """
        with self._get_db() as db:
            return db.query(Documento).filter(
                Documento.fecha_creacion >= fecha_inicio,
                Documento.fecha_creacion <= fecha_fin
            ).order_by(
                Documento.fecha_creacion.desc()
            ).all()
    
    def count_by_tipo_transaccion(self) -> dict:
        """
        Cuenta los documentos por tipo de transacción.
        
        Returns:
            dict: Diccionario con el conteo por tipo de transacción
        """
        with self._get_db() as db:
            # Hacer una consulta agrupada para contar por tipo
            results = db.query(
                Documento.tipo_transaccion,
                db.func.count(Documento.id).label('count')
            ).group_by(
                Documento.tipo_transaccion
            ).all()
            
            # Convertir el resultado a un diccionario
            return {result.tipo_transaccion: result.count for result in results}
    
    def get_all_cliente_ids(self) -> List[str]:
        """
        Obtiene una lista única de todos los IDs de cliente que tienen documentos.
        
        Returns:
            List[str]: Lista de IDs de cliente únicos
        """
        with self._get_db() as db:
            # Obtener IDs únicos de cliente ordenados alfabéticamente
            results = db.query(Documento.cliente_id).distinct().order_by(
                Documento.cliente_id
            ).all()
            
            # Extraer solo los valores de cliente_id de los resultados
            return [result.cliente_id for result in results]