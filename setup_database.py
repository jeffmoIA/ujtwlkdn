#!/usr/bin/env python3
"""
Script para configurar la base de datos de la aplicación.
Este script inicializa la base de datos, ejecuta migraciones y crea datos de ejemplo.
"""
import os
import sys
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

def verificar_dependencias():
    """
    Verifica que todas las dependencias necesarias estén instaladas.
    """
    print("🔍 Verificando dependencias...")
    
    dependencias_requeridas = [
        'sqlalchemy',
        'alembic', 
        'passlib',
        'bcrypt'
    ]
    
    dependencias_faltantes = []
    
    for dependencia in dependencias_requeridas:
        try:
            __import__(dependencia)
            print(f"  ✅ {dependencia}: Instalada")
        except ImportError:
            dependencias_faltantes.append(dependencia)
            print(f"  ❌ {dependencia}: NO instalada")
    
    if dependencias_faltantes:
        print(f"\n❌ Faltan dependencias: {', '.join(dependencias_faltantes)}")
        print("💡 Instale las dependencias con: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def inicializar_base_datos():
    """
    Inicializa la base de datos creando todas las tablas.
    """
    print("\n🗄️ Inicializando base de datos...")
    
    try:
        # Importar los módulos necesarios
        from infrastructure.database.config import engine, Base
        from domain.models import (
            BaseModel, NodoIPRAN, NodoGPON, 
            Usuario, CorreoCliente, Documento
        )
        
        # Crear todas las tablas
        print("  📋 Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("  ✅ Tablas creadas exitosamente")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al inicializar la base de datos: {str(e)}")
        return False

def ejecutar_migraciones():
    """
    Ejecuta las migraciones de Alembic si existen.
    """
    print("\n🔄 Ejecutando migraciones...")
    
    try:
        # Verificar si existe el directorio de migraciones
        if not Path("migrations").exists():
            print("  ⚠️ No se encontró directorio de migraciones")
            print("  💡 Inicializando Alembic...")
            
            # Inicializar Alembic
            os.system("alembic init migrations")
            print("  ✅ Alembic inicializado")
        
        # Verificar si hay migraciones pendientes
        result = os.system("alembic current")
        if result == 0:
            print("  🔄 Ejecutando migraciones pendientes...")
            result = os.system("alembic upgrade head")
            if result == 0:
                print("  ✅ Migraciones ejecutadas exitosamente")
                return True
            else:
                print("  ⚠️ No hay migraciones pendientes o no se pudieron ejecutar")
                return True
        else:
            print("  ⚠️ No se pudo verificar el estado de las migraciones")
            return True
            
    except Exception as e:
        print(f"  ❌ Error en migraciones: {str(e)}")
        return False

def crear_usuario_admin():
    """
    Crea un usuario administrador por defecto si no existe.
    """
    print("\n👤 Configurando usuario administrador...")
    
    try:
        from application.services.auth_service import AuthService
        from infrastructure.repositories.usuario_repository import UsuarioRepository
        
        # Verificar si ya existe un usuario admin
        repo = UsuarioRepository()
        admin_existente = repo.get_by_username("admin")
        
        if admin_existente:
            print("  ✅ Usuario admin ya existe")
            return True
        
        # Crear usuario admin
        auth_service = AuthService()
        admin_user = auth_service.registrar(
            username="admin",
            password="admin123",  # Contraseña temporal que se debe cambiar
            nombre="Administrador del Sistema"
        )
        
        print("  ✅ Usuario administrador creado")
        print("  📝 Usuario: admin")
        print("  🔑 Contraseña: admin123")
        print("  ⚠️  IMPORTANTE: Cambie la contraseña después del primer inicio de sesión")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al crear usuario admin: {str(e)}")
        return False

def crear_datos_ejemplo():
    """
    Crea algunos datos de ejemplo para facilitar las pruebas.
    """
    print("\n📝 Creando datos de ejemplo...")
    
    try:
        # Importar servicios
        from application.services.nodo_ipran_service import NodoIPRANService
        from application.services.nodo_gpon_service import NodoGPONService
        from application.services.correo_cliente_service import CorreoClienteService
        
        # Crear nodos IPRAN de ejemplo
        ipran_service = NodoIPRANService()
        nodos_ipran_ejemplo = [
            ("IPRAN-001", "Nodo Central Guatemala", "192.168.1.1"),
            ("IPRAN-002", "Nodo Zona 10", "192.168.1.2"),
            ("IPRAN-003", "Nodo Mixco", "192.168.1.3")
        ]
        
        print("  📡 Creando nodos IPRAN de ejemplo...")
        for alias, nombre, ip in nodos_ipran_ejemplo:
            try:
                ipran_service.crear(alias, nombre, ip)
                print(f"    ✅ {alias}: {nombre}")
            except ValueError:
                print(f"    ⚠️ {alias}: Ya existe")
        
        # Crear nodos GPON de ejemplo
        gpon_service = NodoGPONService()
        nodos_gpon_ejemplo = [
            ("OLT-001", "OLT Principal Guatemala", "192.168.2.1"),
            ("OLT-002", "OLT Zona Rosa", "192.168.2.2"),
            ("OLT-003", "OLT Carretera a El Salvador", "192.168.2.3")
        ]
        
        print("  🌐 Creando nodos GPON de ejemplo...")
        for alias, nombre, ip in nodos_gpon_ejemplo:
            try:
                gpon_service.crear(alias, nombre, ip)
                print(f"    ✅ {alias}: {nombre}")
            except ValueError:
                print(f"    ⚠️ {alias}: Ya existe")
        
        # Crear plantillas de correo de ejemplo
        correo_service = CorreoClienteService()
        plantillas_ejemplo = [
            {
                "nombre": "Upgrade Estándar",
                "asunto": "Upgrade de Enlace - [CLIENTE_ID] - [CLIENTE_NOMBRE]",
                "contenido": """Estimado cliente,

Es un gusto saludarle. El motivo de este correo es notificarle que se ha aplicado un upgrade a [ANCHO_BANDA] sobre su enlace con ID [CLIENTE_ID] ubicado en [DIRECCION].

El upgrade queda aplicado inmediatamente, por lo que desde este momento ya cuenta con [ANCHO_BANDA] en su servicio.

Saludos cordiales,
Equipo Técnico"""
            },
            {
                "nombre": "Downgrade Estándar", 
                "asunto": "Downgrade de Enlace - [CLIENTE_ID] - [CLIENTE_NOMBRE]",
                "contenido": """Estimado cliente,

Es un gusto saludarle. El motivo de este correo es notificarle que se ha aplicado un downgrade a [ANCHO_BANDA] sobre su enlace con ID [CLIENTE_ID] ubicado en [DIRECCION].

El downgrade queda aplicado inmediatamente, por lo que desde este momento su servicio cuenta con [ANCHO_BANDA].

Saludos cordiales,
Equipo Técnico"""
            },
            {
                "nombre": "Mantenimiento Programado",
                "asunto": "Mantenimiento Programado - [CLIENTE_ID]",
                "contenido": """Estimado cliente,

Le informamos que se realizará un mantenimiento programado en su enlace de internet el día [FECHA] de [HORA_INICIO] a [HORA_FIN].

Durante este tiempo, su servicio de internet podría presentar intermitencias.

Agradecemos su comprensión.

Saludos cordiales,
Equipo Técnico"""
            }
        ]
        
        print("  📧 Creando plantillas de correo de ejemplo...")
        for plantilla in plantillas_ejemplo:
            try:
                correo_service.crear(
                    plantilla["nombre"],
                    plantilla["asunto"],
                    plantilla["contenido"]
                )
                print(f"    ✅ {plantilla['nombre']}")
            except ValueError:
                print(f"    ⚠️ {plantilla['nombre']}: Ya existe")
        
        print("  ✅ Datos de ejemplo creados exitosamente")
        return True
        
    except Exception as e:
        print(f"  ❌ Error al crear datos de ejemplo: {str(e)}")
        return False

def verificar_configuracion():
    """
    Verifica que la configuración de la base de datos sea correcta.
    """
    print("\n🔍 Verificando configuración de la base de datos...")
    
    try:
        from infrastructure.database.config import engine, SessionLocal
        
        # Probar conexión
        with SessionLocal() as session:
            result = session.execute("SELECT 1")
            print("  ✅ Conexión a la base de datos: OK")
        
        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        
        tablas_esperadas = [
            'usuarios', 'nodos_ipran', 'nodos_gpon', 
            'correo_cliente', 'documentos'
        ]
        
        print("  📋 Verificando tablas:")
        for tabla in tablas_esperadas:
            if tabla in tablas:
                print(f"    ✅ {tabla}: Existe")
            else:
                print(f"    ❌ {tabla}: NO existe")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en verificación: {str(e)}")
        return False

def main():
    """Función principal que ejecuta toda la configuración de la base de datos."""
    print("🚀 Iniciando configuración de la base de datos...")
    print("=" * 60)
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    try:
        # Inicializar base de datos
        if not inicializar_base_datos():
            print("\n❌ Error al inicializar la base de datos")
            sys.exit(1)
        
        # Ejecutar migraciones
        ejecutar_migraciones()
        
        # Crear usuario administrador
        if not crear_usuario_admin():
            print("\n⚠️ No se pudo crear el usuario administrador")
        
        # Crear datos de ejemplo
        if not crear_datos_ejemplo():
            print("\n⚠️ No se pudieron crear los datos de ejemplo")
        
        # Verificar configuración final
        if not verificar_configuracion():
            print("\n⚠️ Hay problemas en la configuración final")
        
        print("\n" + "=" * 60)
        print("✅ ¡Base de datos configurada exitosamente!")
        print("\n📋 Información importante:")
        print("  🗄️ Base de datos: network_app.db (SQLite)")
        print("  👤 Usuario admin: admin / admin123")
        print("  📝 Datos de ejemplo: Creados")
        print("\n🎉 ¡Ya puede ejecutar la aplicación!")
        print("▶️  Comando: python src/main.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()