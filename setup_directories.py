#!/usr/bin/env python3
"""
Script para configurar los directorios de recursos necesarios para la aplicación.
Este script crea la estructura de carpetas necesaria para almacenar documentos,
plantillas y otros recursos de la aplicación.
"""
import os
import sys
from pathlib import Path

def crear_estructura_directorios():
    """
    Crea la estructura de directorios necesaria para la aplicación.
    """
    # Obtener la ruta raíz del proyecto
    # Este script debe estar en la raíz del proyecto
    proyecto_root = Path(__file__).parent
    
    print("🏗️ Configurando estructura de directorios...")
    print(f"📁 Directorio del proyecto: {proyecto_root}")
    
    # Definir la estructura de directorios a crear
    directorios = [
        # Directorio principal de recursos
        "recursos",
        
        # Subdirectorios para diferentes tipos de recursos
        "recursos/documentos",           # Documentos exportados (Word, PDF, etc.)
        "recursos/documentos/imagenes",  # Imágenes extraídas de documentos
        "recursos/plantillas",           # Plantillas de documentos Word
        "recursos/imagenes",             # Imágenes de la aplicación (logos, iconos)
        "recursos/exports",              # Exports de configuración de equipos
        "recursos/backup",               # Respaldos de la base de datos
        "recursos/logs",                 # Archivos de log de la aplicación
        "recursos/temp",                 # Archivos temporales
        
        # Directorios para diferentes tipos de documentos
        "recursos/documentos/upgrades",   # Documentos de upgrades
        "recursos/documentos/downgrades", # Documentos de downgrades
        "recursos/documentos/instalaciones", # Documentos de nuevas instalaciones
        
        # Directorios para plantillas específicas
        "recursos/plantillas/word",       # Plantillas de Word
        "recursos/plantillas/correo",     # Plantillas de correo
        
        # Directorio para configuraciones
        "config",                        # Archivos de configuración
    ]
    
    # Crear cada directorio
    directorios_creados = []
    directorios_existentes = []
    
    for directorio in directorios:
        ruta_completa = proyecto_root / directorio
        
        try:
            if ruta_completa.exists():
                directorios_existentes.append(directorio)
                print(f"  ✅ Ya existe: {directorio}")
            else:
                ruta_completa.mkdir(parents=True, exist_ok=True)
                directorios_creados.append(directorio)
                print(f"  ✨ Creado: {directorio}")
        except Exception as e:
            print(f"  ❌ Error al crear {directorio}: {str(e)}")
            return False
    
    print(f"\n📊 Resumen:")
    print(f"  • Directorios creados: {len(directorios_creados)}")
    print(f"  • Directorios existentes: {len(directorios_existentes)}")
    print(f"  • Total de directorios: {len(directorios)}")
    
    return True

def crear_archivos_configuracion():
    """
    Crea archivos de configuración básicos si no existen.
    """
    proyecto_root = Path(__file__).parent
    
    print("\n⚙️ Creando archivos de configuración...")
    
    # Archivo de configuración principal
    config_file = proyecto_root / "config" / "app_config.py"
    if not config_file.exists():
        contenido_config = '''"""
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
'''
        
        try:
            config_file.write_text(contenido_config, encoding='utf-8')
            print(f"  ✨ Creado: config/app_config.py")
        except Exception as e:
            print(f"  ❌ Error al crear config/app_config.py: {str(e)}")
    else:
        print(f"  ✅ Ya existe: config/app_config.py")
    
    # Archivo README para los recursos
    readme_file = proyecto_root / "recursos" / "README.md"
    if not readme_file.exists():
        contenido_readme = '''# Directorio de Recursos

Este directorio contiene todos los recursos necesarios para la aplicación de gestión de red.

## Estructura de Directorios

### 📄 `/documentos`
Documentos generados por la aplicación:
- `upgrades/` - Documentos de upgrades de servicio
- `downgrades/` - Documentos de downgrades de servicio
- `instalaciones/` - Documentos de nuevas instalaciones
- `imagenes/` - Imágenes extraídas o utilizadas en documentos

### 📋 `/plantillas`
Plantillas para generar documentos:
- `word/` - Plantillas de Microsoft Word
- `correo/` - Plantillas de correos electrónicos

### 🖼️ `/imagenes`
Imágenes de la aplicación:
- Logos de la empresa
- Iconos de la interfaz
- Imágenes de referencia

### 📤 `/exports`
Exports de configuración de equipos:
- Configuraciones de Mikrotik
- Configuraciones de switches
- Otros exports de equipos de red

### 💾 `/backup`
Respaldos automáticos:
- Respaldos de la base de datos
- Respaldos de configuraciones importantes

### 📝 `/logs`
Archivos de registro de la aplicación:
- Logs de errores
- Logs de actividad del usuario
- Logs del sistema

### 🔄 `/temp`
Archivos temporales:
- Archivos temporales durante la exportación
- Imágenes temporales del portapapeles
- Cachés temporales

## Uso

Todos estos directorios son creados automáticamente por la aplicación cuando es necesario.
No elimine estos directorios a menos que esté seguro de lo que está haciendo.

## Mantenimiento

- Los archivos temporales pueden ser eliminados periódicamente
- Los logs antiguos se rotan automáticamente
- Los backups se pueden programar según sus necesidades
'''
        
        try:
            readme_file.write_text(contenido_readme, encoding='utf-8')
            print(f"  ✨ Creado: recursos/README.md")
        except Exception as e:
            print(f"  ❌ Error al crear recursos/README.md: {str(e)}")
    else:
        print(f"  ✅ Ya existe: recursos/README.md")

def crear_archivo_gitignore():
    """
    Crea o actualiza el archivo .gitignore para excluir archivos no necesarios.
    """
    proyecto_root = Path(__file__).parent
    gitignore_file = proyecto_root / ".gitignore"
    
    print("\n🔒 Configurando .gitignore...")
    
    # Contenido adicional para .gitignore
    contenido_adicional = '''
# === Archivos específicos de la aplicación ===
# Base de datos local
network_app.db
*.db
*.sqlite
*.sqlite3

# Documentos generados
recursos/documentos/*.docx
recursos/documentos/*.pdf
recursos/documentos/imagenes/*
recursos/exports/*

# Archivos temporales
recursos/temp/*
!recursos/temp/.gitkeep

# Logs de la aplicación
recursos/logs/*.log
recursos/logs/*.txt
!recursos/logs/.gitkeep

# Backups
recursos/backup/*
!recursos/backup/.gitkeep

# Configuraciones locales
config/local_config.py
config/secrets.py

# Archivos de imágenes temporales
*.tmp.png
*.tmp.jpg
*.tmp.jpeg

# Archivos de configuración de PyInstaller
*.spec
build/
dist/

# Archivos de entorno local
.env.local
.env.development
'''
    
    try:
        if gitignore_file.exists():
            # Leer contenido existente
            contenido_existente = gitignore_file.read_text(encoding='utf-8')
            
            # Solo agregar si no existe ya
            if "# === Archivos específicos de la aplicación ===" not in contenido_existente:
                # Agregar al final
                with open(gitignore_file, 'a', encoding='utf-8') as f:
                    f.write(contenido_adicional)
                print(f"  ✨ Actualizado: .gitignore")
            else:
                print(f"  ✅ Ya configurado: .gitignore")
        else:
            # Crear nuevo archivo
            gitignore_file.write_text(contenido_adicional.strip(), encoding='utf-8')
            print(f"  ✨ Creado: .gitignore")
    except Exception as e:
        print(f"  ❌ Error al configurar .gitignore: {str(e)}")

def crear_archivos_gitkeep():
    """
    Crea archivos .gitkeep en directorios vacíos para mantener la estructura en Git.
    """
    proyecto_root = Path(__file__).parent
    
    print("\n📌 Creando archivos .gitkeep...")
    
    # Directorios que deben mantenerse vacíos pero presentes en Git
    directorios_gitkeep = [
        "recursos/temp",
        "recursos/logs", 
        "recursos/backup",
        "recursos/documentos/imagenes",
        "recursos/exports"
    ]
    
    for directorio in directorios_gitkeep:
        gitkeep_file = proyecto_root / directorio / ".gitkeep"
        
        try:
            if not gitkeep_file.exists():
                gitkeep_file.write_text("# Este archivo mantiene el directorio en Git\n")
                print(f"  ✨ Creado: {directorio}/.gitkeep")
            else:
                print(f"  ✅ Ya existe: {directorio}/.gitkeep")
        except Exception as e:
            print(f"  ❌ Error al crear {directorio}/.gitkeep: {str(e)}")

def verificar_permisos():
    """
    Verifica que se tengan los permisos necesarios para crear archivos y directorios.
    """
    proyecto_root = Path(__file__).parent
    
    print("\n🔐 Verificando permisos...")
    
    try:
        # Intentar crear un archivo temporal
        test_file = proyecto_root / "test_permissions.tmp"
        test_file.write_text("test")
        test_file.unlink()  # Eliminar el archivo de prueba
        print("  ✅ Permisos de escritura: OK")
        return True
    except Exception as e:
        print(f"  ❌ Error de permisos: {str(e)}")
        print("  💡 Solución: Ejecute el script como administrador o verifique los permisos del directorio")
        return False

def main():
    """Función principal que ejecuta toda la configuración."""
    print("🚀 Iniciando configuración de estructura de directorios...")
    print("=" * 60)
    
    # Verificar permisos antes de comenzar
    if not verificar_permisos():
        print("\n❌ No se puede continuar sin permisos de escritura")
        sys.exit(1)
    
    try:
        # Crear estructura de directorios
        if not crear_estructura_directorios():
            print("\n❌ Error al crear la estructura de directorios")
            sys.exit(1)
        
        # Crear archivos de configuración
        crear_archivos_configuracion()
        
        # Configurar .gitignore
        crear_archivo_gitignore()
        
        # Crear archivos .gitkeep
        crear_archivos_gitkeep()
        
        print("\n" + "=" * 60)
        print("✅ ¡Configuración completada exitosamente!")
        print("\n📋 Próximos pasos:")
        print("  1. Instalar dependencias: pip install -r requirements.txt")
        print("  2. Configurar base de datos: python -c 'from src.infrastructure.database.init_db import init_db; init_db()'")
        print("  3. Ejecutar migraciones: alembic upgrade head")
        print("  4. Ejecutar la aplicación: python src/main.py")
        print("\n🎉 ¡Tu aplicación está lista para usar!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la configuración: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()