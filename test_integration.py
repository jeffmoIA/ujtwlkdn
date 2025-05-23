#!/usr/bin/env python3
"""
Script de configuración rápida para solucionar los errores encontrados.
Este script configura todo lo necesario para que la aplicación funcione.
"""
import os
import sys
from pathlib import Path

def crear_directorios():
    """Crea los directorios necesarios."""
    print("📁 Creando estructura de directorios...")
    
    # Directorios principales que necesitamos
    directorios = [
        "recursos",
        "recursos/documentos", 
        "recursos/plantillas",
        "recursos/imagenes",
        "recursos/backup",
        "recursos/logs",
        "recursos/temp",
        "recursos/exports"
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directorio}")
    
    print("✅ Directorios creados correctamente")

def configurar_base_datos():
    """Configura la base de datos."""
    print("\n🗄️ Configurando base de datos...")
    
    try:
        # Agregar src al path
        sys.path.insert(0, "src")
        
        # Importar configuración de base de datos
        from infrastructure.database.config import engine, Base
        
        # Importar todos los modelos para que se registren
        from domain.models.base_model import BaseModel
        from domain.models.nodo_ipran import NodoIPRAN
        from domain.models.nodo_gpon import NodoGPON
        from domain.models.usuario import Usuario
        from domain.models.correo_cliente import CorreoCliente
        from domain.models.documento import Documento
        
        # Crear todas las tablas
        print("  📋 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        
        print("  ✅ Tablas creadas correctamente")
        
        # Crear usuario administrador por defecto
        crear_usuario_admin()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al configurar base de datos: {str(e)}")
        return False

def crear_usuario_admin():
    """Crea el usuario administrador por defecto."""
    print("  👤 Creando usuario administrador...")
    
    try:
        from application.services.auth_service import AuthService
        from infrastructure.repositories.usuario_repository import UsuarioRepository
        
        # Verificar si ya existe
        repo = UsuarioRepository()
        admin_existente = repo.get_by_username("admin")
        
        if admin_existente:
            print("    ✅ Usuario admin ya existe")
            return
        
        # Crear usuario admin
        auth_service = AuthService()
        admin_user = auth_service.registrar(
            username="admin",
            password="admin123",
            nombre="Administrador del Sistema"
        )
        
        print("    ✅ Usuario admin creado (admin/admin123)")
        
    except Exception as e:
        print(f"    ⚠️ Error al crear usuario admin: {str(e)}")

def crear_datos_ejemplo():
    """Crea algunos datos de ejemplo."""
    print("\n📝 Creando datos de ejemplo...")
    
    try:
        from application.services.nodo_ipran_service import NodoIPRANService
        from application.services.nodo_gpon_service import NodoGPONService
        
        # Crear nodos IPRAN de ejemplo
        ipran_service = NodoIPRANService()
        nodos_ipran_ejemplo = [
            ("IPRAN-GT01", "Nodo Central Guatemala", "192.168.1.1"),
            ("IPRAN-MX01", "Nodo Mixco", "192.168.1.2"),
            ("IPRAN-Z10", "Nodo Zona 10", "192.168.1.3")
        ]
        
        print("  📡 Creando nodos IPRAN...")
        for alias, nombre, ip in nodos_ipran_ejemplo:
            try:
                ipran_service.crear(alias, nombre, ip)
                print(f"    ✅ {alias}: {nombre}")
            except ValueError:
                print(f"    ⚠️ {alias}: Ya existe")
        
        # Crear nodos GPON de ejemplo
        gpon_service = NodoGPONService()
        nodos_gpon_ejemplo = [
            ("OLT-GT01", "OLT Principal Guatemala", "192.168.2.1"),
            ("OLT-ZR01", "OLT Zona Rosa", "192.168.2.2"),
            ("OLT-ES01", "OLT Carretera El Salvador", "192.168.2.3")
        ]
        
        print("  🌐 Creando nodos GPON...")
        for alias, nombre, ip in nodos_gpon_ejemplo:
            try:
                gpon_service.crear(alias, nombre, ip)
                print(f"    ✅ {alias}: {nombre}")
            except ValueError:
                print(f"    ⚠️ {alias}: Ya existe")
        
        print("  ✅ Datos de ejemplo creados")
        
    except Exception as e:
        print(f"  ⚠️ Error al crear datos de ejemplo: {str(e)}")

def verificar_configuracion():
    """Verifica que todo esté configurado correctamente."""
    print("\n🔍 Verificando configuración...")
    
    try:
        from infrastructure.database.config import SessionLocal
        from sqlalchemy import text
        
        # Probar conexión
        with SessionLocal() as session:
            result = session.execute(text("SELECT 1")).fetchone()
            if result[0] == 1:
                print("  ✅ Conexión a base de datos: OK")
            
        # Verificar directorios
        directorios_requeridos = ["recursos", "recursos/documentos", "recursos/plantillas"]
        for directorio in directorios_requeridos:
            if Path(directorio).exists():
                print(f"  ✅ Directorio {directorio}: OK")
            else:
                print(f"  ❌ Directorio {directorio}: Falta")
        
        print("  ✅ Configuración verificada")
        return True
        
    except Exception as e:
        print(f"  ❌ Error en verificación: {str(e)}")
        return False

def main():
    """Función principal del script de configuración rápida."""
    print("🚀 CONFIGURACIÓN RÁPIDA - Solucionando errores encontrados")
    print("=" * 60)
    
    try:
        # Paso 1: Crear directorios
        crear_directorios()
        
        # Paso 2: Configurar base de datos
        if not configurar_base_datos():
            print("\n❌ Error crítico en la configuración de base de datos")
            sys.exit(1)
        
        # Paso 3: Crear datos de ejemplo
        crear_datos_ejemplo()
        
        # Paso 4: Verificar configuración
        if verificar_configuracion():
            print("\n✅ ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
            print("\n📋 Próximos pasos:")
            print("  1. Ejecutar pruebas: python test_integration.py")
            print("  2. Iniciar aplicación: python src/main.py")
            print("\n🎉 ¡Tu aplicación está lista para usar!")
        else:
            print("\n⚠️ Configuración completada con advertencias")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        print("\n💡 Solución manual:")
        print("  1. python setup_directories.py")
        print("  2. python setup_database.py")
        sys.exit(1)

if __name__ == "__main__":
    main()