# src/infrastructure/repositories/mikrotik_repository.py
"""
Repositorio para el modelo MikroTik.
Este repositorio maneja todas las operaciones de base de datos para equipos MikroTik.
"""
from typing import List, Optional
from sqlalchemy import func, or_, and_  # ← ARREGLO: Importar func, or_, and_ directamente
from domain.models.mikrotik import MikroTik
from infrastructure.repositories.sqlalchemy_repository import SQLAlchemyRepository

class MikroTikRepository(SQLAlchemyRepository[MikroTik]):
    """Repositorio para manejar operaciones CRUD de equipos MikroTik."""
    
    def __init__(self):
        """Constructor del repositorio."""
        # Llamamos al constructor padre pasando la clase del modelo MikroTik
        super().__init__(MikroTik)
    
    # === MÉTODOS DE BÚSQUEDA ESPECÍFICOS ===
    
    def get_by_nombre(self, nombre: str) -> Optional[MikroTik]:
        """
        Obtiene un MikroTik por su nombre/alias.
        
        Args:
            nombre: Nombre del MikroTik a buscar
            
        Returns:
            Optional[MikroTik]: El MikroTik encontrado o None si no existe
        """
        # Usar el contexto de base de datos para hacer la consulta
        with self._get_db() as db:
            return db.query(MikroTik).filter(MikroTik.nombre == nombre).first()
    
    def get_by_ip(self, ip: str) -> Optional[MikroTik]:
        """
        Obtiene un MikroTik por su dirección IP.
        
        Args:
            ip: Dirección IP del MikroTik a buscar
            
        Returns:
            Optional[MikroTik]: El MikroTik encontrado o None si no existe
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(MikroTik.ip_mikrotik == ip).first()
    
    def get_by_estado(self, estado: str) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks que tienen un estado específico.
        
        Args:
            estado: Estado a buscar ('activo', 'inactivo', 'mantenimiento', 'error')
            
        Returns:
            List[MikroTik]: Lista de MikroTiks con el estado especificado
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                MikroTik.estado == estado.lower()
            ).order_by(MikroTik.nombre).all()
    
    def get_activos(self) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks en estado activo.
        
        Returns:
            List[MikroTik]: Lista de MikroTiks activos
        """
        return self.get_by_estado("activo")
    
    def get_disponibles(self) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks que están disponibles (responden ping).
        
        Returns:
            List[MikroTik]: Lista de MikroTiks disponibles
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                MikroTik.disponible == True
            ).order_by(MikroTik.nombre).all()
    
    def get_by_cliente(self, cliente_id: str) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks de un cliente específico.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            List[MikroTik]: Lista de MikroTiks del cliente
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                MikroTik.cliente_id == cliente_id
            ).order_by(MikroTik.nombre).all()
    
    def get_by_modelo(self, modelo: str) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks de un modelo específico.
        
        Args:
            modelo: Modelo del MikroTik (ej: 'RB750Gr3', 'hEX')
            
        Returns:
            List[MikroTik]: Lista de MikroTiks del modelo especificado
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                MikroTik.modelo.ilike(f"%{modelo}%")  # ilike = búsqueda insensible a mayúsculas
            ).order_by(MikroTik.nombre).all()
    
    # === MÉTODOS DE BÚSQUEDA AVANZADA ===
    
    def search_by_text(self, texto_busqueda: str) -> List[MikroTik]:
        """
        Busca MikroTiks que contengan el texto en varios campos.
        
        Args:
            texto_busqueda: Texto a buscar
            
        Returns:
            List[MikroTik]: Lista de MikroTiks que contienen el texto
        """
        with self._get_db() as db:
            # Convertir a minúsculas para búsqueda insensible a mayúsculas
            patron_busqueda = f"%{texto_busqueda.lower()}%"
            
            return db.query(MikroTik).filter(
                # Buscar en múltiples campos usando OR
                # ARREGLO: Usar or_ importado directamente
                or_(
                    MikroTik.nombre.ilike(patron_busqueda),           # En el nombre
                    MikroTik.ip_mikrotik.ilike(patron_busqueda),     # En la IP
                    MikroTik.modelo.ilike(patron_busqueda),          # En el modelo
                    MikroTik.ubicacion.ilike(patron_busqueda),       # En la ubicación
                    MikroTik.cliente_nombre.ilike(patron_busqueda),  # En el nombre del cliente
                    MikroTik.notas.ilike(patron_busqueda)            # En las notas
                )
            ).order_by(MikroTik.nombre).all()
    
    def get_con_credenciales(self) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks que tienen credenciales configuradas.
        
        Returns:
            List[MikroTik]: Lista de MikroTiks con credenciales
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                # Ambos campos deben tener valor (not null y not empty)
                # ARREGLO: Usar and_ importado directamente
                and_(
                    MikroTik.usuario_acceso.isnot(None),
                    MikroTik.usuario_acceso != "",
                    MikroTik.contrasena_acceso.isnot(None),
                    MikroTik.contrasena_acceso != ""
                )
            ).order_by(MikroTik.nombre).all()
    
    def get_sin_credenciales(self) -> List[MikroTik]:
        """
        Obtiene todos los MikroTiks que NO tienen credenciales configuradas.
        
        Returns:
            List[MikroTik]: Lista de MikroTiks sin credenciales
        """
        with self._get_db() as db:
            return db.query(MikroTik).filter(
                # Al menos uno de los campos está vacío
                # ARREGLO: Usar or_ importado directamente
                or_(
                    MikroTik.usuario_acceso.is_(None),
                    MikroTik.usuario_acceso == "",
                    MikroTik.contrasena_acceso.is_(None),
                    MikroTik.contrasena_acceso == ""
                )
            ).order_by(MikroTik.nombre).all()
    
    # === MÉTODOS DE ESTADÍSTICAS ===
    
    def count_by_estado(self) -> dict:
        """
        Cuenta los MikroTiks por estado.
        
        Returns:
            dict: Diccionario con el conteo por estado
        """
        with self._get_db() as db:
            # Hacer consulta agrupada para contar por estado
            # ARREGLO: Usar func importado directamente, no db.func
            results = db.query(
                MikroTik.estado,
                func.count(MikroTik.id).label('count')  # ← ARREGLO: func en lugar de db.func
            ).group_by(MikroTik.estado).all()
            
            # Convertir resultado a diccionario
            return {result.estado: result.count for result in results}
    
    def count_by_modelo(self) -> dict:
        """
        Cuenta los MikroTiks por modelo.
        
        Returns:
            dict: Diccionario con el conteo por modelo
        """
        with self._get_db() as db:
            # ARREGLO: Usar func importado directamente
            results = db.query(
                MikroTik.modelo,
                func.count(MikroTik.id).label('count')  # ← ARREGLO: func en lugar de db.func
            ).filter(
                MikroTik.modelo.isnot(None)  # Solo contar los que tienen modelo definido
            ).group_by(MikroTik.modelo).all()
            
            return {result.modelo or "Sin modelo": result.count for result in results}
    
    def get_disponibilidad_stats(self) -> dict:
        """
        Obtiene estadísticas de disponibilidad de los MikroTiks.
        
        Returns:
            dict: Estadísticas de disponibilidad
        """
        with self._get_db() as db:
            total = db.query(MikroTik).count()
            disponibles = db.query(MikroTik).filter(MikroTik.disponible == True).count()
            no_disponibles = total - disponibles
            
            return {
                "total": total,
                "disponibles": disponibles,
                "no_disponibles": no_disponibles,
                "porcentaje_disponibilidad": round((disponibles / total * 100) if total > 0 else 0, 2)
            }
    
    # === MÉTODOS DE ACTUALIZACIÓN MASIVA ===
    
    def actualizar_disponibilidad_masiva(self, ip_disponibles: List[str]):
        """
        Actualiza la disponibilidad de múltiples MikroTiks basado en una lista de IPs.
        
        Args:
            ip_disponibles: Lista de IPs que están disponibles (responden ping)
        """
        with self._get_db() as db:
            # Marcar todos como no disponibles primero
            db.query(MikroTik).update({MikroTik.disponible: False})
            
            # Marcar como disponibles solo los que están en la lista
            if ip_disponibles:
                db.query(MikroTik).filter(
                    MikroTik.ip_mikrotik.in_(ip_disponibles)
                ).update({MikroTik.disponible: True}, synchronize_session=False)
            
            db.commit()
    
    # === MÉTODOS DE VALIDACIÓN ===
    
    def existe_nombre(self, nombre: str, excluir_id: Optional[int] = None) -> bool:
        """
        Verifica si ya existe un MikroTik con el nombre especificado.
        
        Args:
            nombre: Nombre a verificar
            excluir_id: ID a excluir de la búsqueda (útil para ediciones)
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        with self._get_db() as db:
            query = db.query(MikroTik).filter(MikroTik.nombre == nombre)
            
            # Si estamos editando, excluir el ID actual
            if excluir_id:
                query = query.filter(MikroTik.id != excluir_id)
            
            return query.first() is not None
    
    def existe_ip(self, ip: str, excluir_id: Optional[int] = None) -> bool:
        """
        Verifica si ya existe un MikroTik con la IP especificada.
        
        Args:
            ip: IP a verificar
            excluir_id: ID a excluir de la búsqueda (útil para ediciones)
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        with self._get_db() as db:
            query = db.query(MikroTik).filter(MikroTik.ip_mikrotik == ip)
            
            if excluir_id:
                query = query.filter(MikroTik.id != excluir_id)
            
            return query.first() is not None