# src/domain/models/mikrotik.py
"""
Modelo para equipos MikroTik.
Este modelo almacena la información de los equipos MikroTik que podemos gestionar.
"""
from sqlalchemy import Column, String, Text, Boolean
from domain.models.base_model import BaseModel

class MikroTik(BaseModel):
    """Clase para representar un equipo MikroTik en la red."""
    
    # Nombre de la tabla en la base de datos
    __tablename__ = "mikrotiks"
    
    # === CAMPOS BÁSICOS DE IDENTIFICACIÓN ===
    
    # Nombre/alias del equipo (único) - Ej: "MTK-CLIENTE-001"
    nombre = Column(String(100), unique=True, nullable=False, index=True)
    
    # Dirección IP del MikroTik - Ej: "192.168.1.1"
    ip_mikrotik = Column(String(15), unique=True, nullable=False, index=True)
    
    # === INFORMACIÓN TÉCNICA DEL EQUIPO ===
    
    # Modelo del MikroTik - Ej: "RB750Gr3", "hEX", "CCR1009"
    modelo = Column(String(50), nullable=True)
    
    # Versión de RouterOS instalada - Ej: "6.49.10", "7.1.5"
    version_routeros = Column(String(20), nullable=True)
    
    # === CREDENCIALES DE ACCESO ===
    # NOTA: En producción, estas credenciales deberían estar encriptadas
    
    # Usuario para acceder al MikroTik - Ej: "admin"
    usuario_acceso = Column(String(50), nullable=False, default="admin")
    
    # Contraseña para acceder (almacenada de forma segura)
    # IMPORTANTE: En el futuro deberíamos encriptar esto
    contrasena_acceso = Column(String(100), nullable=True)
    
    # === INFORMACIÓN DE UBICACIÓN Y ESTADO ===
    
    # Ubicación física del equipo - Ej: "Oficina Principal", "Casa Cliente"  
    ubicacion = Column(String(200), nullable=True)
    
    # Estado actual del equipo: "activo", "inactivo", "mantenimiento", "error"
    estado = Column(String(20), nullable=False, default="activo")
    
    # Si el equipo está disponible (responde ping)
    disponible = Column(Boolean, default=False)
    
    # === INFORMACIÓN ADICIONAL ===
    
    # Notas adicionales sobre el equipo
    notas = Column(Text, nullable=True)
    
    # Última configuración exportada (para respaldo)
    ultimo_export = Column(Text, nullable=True)
    
    # === INFORMACIÓN DE CLIENTE (OPCIONAL) ===
    
    # ID del cliente al que pertenece este MikroTik
    cliente_id = Column(String(50), nullable=True)
    
    # Nombre del cliente para referencia rápida
    cliente_nombre = Column(String(200), nullable=True)
    
    def __repr__(self):
        """
        Representación en string del objeto MikroTik.
        Esto se mostrará cuando imprimas el objeto.
        """
        return f"<MikroTik(nombre='{self.nombre}', ip='{self.ip_mikrotik}', estado='{self.estado}')>"
    
    def __str__(self):
        """
        Representación legible para humanos del objeto.
        """
        return f"{self.nombre} ({self.ip_mikrotik}) - {self.estado.title()}"
    
    # === MÉTODOS ÚTILES ===
    
    def esta_activo(self) -> bool:
        """
        Verifica si el MikroTik está en estado activo.
        
        Returns:
            bool: True si está activo, False en caso contrario
        """
        return self.estado.lower() == "activo"
    
    def tiene_credenciales(self) -> bool:
        """
        Verifica si el MikroTik tiene credenciales configuradas.
        
        Returns:
            bool: True si tiene usuario y contraseña, False en caso contrario
        """
        return bool(self.usuario_acceso and self.contrasena_acceso)
    
    def get_info_basica(self) -> dict:
        """
        Obtiene información básica del MikroTik en formato diccionario.
        Útil para mostrar en interfaces o logs.
        
        Returns:
            dict: Información básica del MikroTik
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ip": self.ip_mikrotik,
            "modelo": self.modelo or "No especificado",
            "version": self.version_routeros or "Desconocida",
            "estado": self.estado,
            "disponible": self.disponible,
            "ubicacion": self.ubicacion or "No especificada"
        }
    
    def actualizar_disponibilidad(self, disponible: bool):
        """
        Actualiza el estado de disponibilidad del MikroTik.
        Se llamará después de hacer ping.
        
        Args:
            disponible (bool): True si responde ping, False si no
        """
        self.disponible = disponible
        # Si no está disponible, podríamos cambiar el estado
        if not disponible and self.estado == "activo":
            self.estado = "error"
        elif disponible and self.estado == "error":
            self.estado = "activo"