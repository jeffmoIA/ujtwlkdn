"""
Configuración principal de la aplicación.
Este archivo contiene las configuraciones globales de la aplicación.
"""

# Configuración de la base de datos
DATABASE_CONFIG = {
    "url": "sqlite:///network_app.db",
    "echo": False,  # True para ver las consultas SQL en consola
    "pool_pre_ping": True
}

# Configuración de la aplicación
APP_CONFIG = {
    "name": "Gestor de Red",
    "version": "1.0.0",
    "author": "Tu Nombre",
    "description": "Aplicación para gestión de red y documentos técnicos"
}

# Configuración de directorios
DIRECTORIES = {
    "recursos": "recursos",
    "documentos": "recursos/documentos",
    "plantillas": "recursos/plantillas",
    "imagenes": "recursos/imagenes",
    "exports": "recursos/exports",
    "backup": "recursos/backup",
    "logs": "recursos/logs",
    "temp": "recursos/temp"
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "recursos/logs/app.log",
    "max_size": "10MB",
    "backup_count": 5
}

# Configuración de exportación
EXPORT_CONFIG = {
    "word_template": "recursos/plantillas/word/template_base.docx",
    "default_author": "Sistema de Gestión de Red",
    "company_name": "Tu Empresa",
    "company_logo": "recursos/imagenes/logo.png"
}
