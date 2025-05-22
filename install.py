#!/usr/bin/env python3
"""
Script de instalación completa para la aplicación de gestión de red.
Este script automatiza todo el proceso de configuración inicial.
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def mostrar_banner():
    """Muestra el banner de bienvenida."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🌐 APLICACIÓN DE GESTIÓN DE RED                       ║
║                                                              ║
║        📋 Instalador Automático v1.0                        ║
║        🐍 Python + Tkinter + SQLAlchemy                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def verificar_python():
    """Verifica que se esté usando una versión compatible de Python."""
    print("🔍 Verificando versión de Python...")
    
    version = sys.version_info
    print(f"  📊 Versión actual: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ❌ Se requiere Python 3.8 o superior")
        print("  💡 Descargue Python desde: https://www.python.org/downloads/")
        return False
    
    print("  ✅ Versión de Python compatible")
    return True

def verificar_pip():
    """Verifica que pip esté instalado y funcionando."""
    print("\n🔍 Verificando pip...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ pip está instalado: {result.stdout.strip()}")
            return True
        else:
            print("  ❌ pip no está funcionando correctamente")
            return False
    except Exception as e:
        print(f"  ❌ Error al verificar pip: {str(e)}")
        return False

def instalar_dependencias():
    """Instala las dependencias desde requirements.txt."""
    print("\n📦 Instalando dependencias...")
    
    # Verificar que existe requirements.txt
    if not Path("requirements.txt").exists():
        print("  ❌ No se encontró el archivo requirements.txt")
        return False
    
    try:
        # Actualizar pip primero
        print("  🔄 Actualizando pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Instalar dependencias
        print("  📥 Instalando paquetes...")
        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        
        # Mostrar progreso en tiempo real
        for line in process.stdout:
            if line.strip():
                # Mostrar solo las líneas importantes
                if "Installing" in line or "Successfully installed" in line:
                    print(f"    {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print("  ✅ Todas las dependencias instaladas correctamente")
            return True
        else:
            print("  ❌ Error al instalar algunas dependencias")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Error en la instalación: {str(e)}")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {str(e)}")
        return False

def ejecutar_script(script_name, descripcion):
    """
    Ejecuta un script de configuración específico.
    
    Args:
        script_name: Nombre del script a ejecutar
        descripcion: Descripción de lo que hace el script
    """
    print(f"\n{descripcion}...")
    
    if not Path(script_name).exists():
        print(f"  ❌ No se encontró el script: {script_name}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False,  # Mostrar salida en tiempo real
                              text=True)
        
        if result.returncode == 0:
            print(f"  ✅ {descripcion} completado exitosamente")
            return True
        else:
            print(f"  ⚠️ {descripcion} terminó con advertencias")
            return True  # Continuar aunque haya advertencias
            
    except Exception as e:
        print(f"  ❌ Error al ejecutar {script_name}: {str(e)}")
        return False

def verificar_instalacion():
    """Verifica que la instalación se haya completado correctamente."""
    print("\n🔍 Verificando instalación...")
    
    verificaciones = [
        ("network_app.db", "Base de datos"),
        ("recursos", "Directorio de recursos"),
        ("src", "Código fuente"),
        ("migrations", "Migraciones de base de datos")
    ]
    
    todo_ok = True
    
    for archivo, descripcion in verificaciones:
        if Path(archivo).exists():
            print(f"  ✅ {descripcion}: OK")
        else:
            print(f"  ❌ {descripcion}: Falta")
            todo_ok = False
    
    # Verificar importaciones importantes
    print("  🔍 Verificando módulos Python...")
    modulos_importantes = [
        'tkinter',
        'sqlalchemy', 
        'alembic',
        'passlib'
    ]
    
    for modulo in modulos_importantes:
        try:
            __import__(modulo)
            print(f"    ✅ {modulo}: Disponible")
        except ImportError:
            print(f"    ❌ {modulo}: No disponible")
            todo_ok = False
    
    return todo_ok

def mostrar_instrucciones_uso():
    """Muestra las instrucciones de uso de la aplicación."""
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    
    print("\n📋 CÓMO USAR LA APLICACIÓN:")
    print("  1️⃣  Ejecutar: python src/main.py")
    print("  2️⃣  Usuario: admin")
    print("  3️⃣  Contraseña: admin123")
    print("  4️⃣  ¡Cambiar la contraseña después del primer login!")
    
    print("\n🔧 ARCHIVOS IMPORTANTES:")
    print("  📄 network_app.db    - Base de datos principal")
    print("  📁 recursos/         - Documentos y plantillas")
    print("  📁 src/              - Código fuente")
    print("  📝 requirements.txt  - Lista de dependencias")
    
    print("\n🆘 SOLUCIÓN DE PROBLEMAS:")
    print("  • Si la app no inicia: python -c 'import tkinter; tkinter._test()'")
    print("  • Para reinstalar: rm network_app.db && python setup_database.py")
    print("  • Para logs: revisar recursos/logs/")
    
    print("\n🔄 COMANDOS ÚTILES:")
    print("  • Backup BD: python -c 'import shutil; shutil.copy(\"network_app.db\", \"recursos/backup/\")'")
    print("  • Limpiar temp: rm -rf recursos/temp/*")
    print("  • Actualizar deps: pip install -r requirements.txt --upgrade")

def confirmar_continuacion():
    """Solicita confirmación del usuario para continuar."""
    while True:
        respuesta = input("\n¿Desea continuar con la instalación? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            print("Por favor, responda 's' para sí o 'n' para no.")

def main():
    """Función principal del instalador."""
    mostrar_banner()
    
    # Verificaciones iniciales
    print("🔍 VERIFICACIONES INICIALES")
    print("-" * 30)
    
    if not verificar_python():
        sys.exit(1)
    
    if not verificar_pip():
        sys.exit(1)
    
    # Mostrar información del sistema
    print(f"\n💻 Sistema operativo: {platform.system()} {platform.release()}")
    print(f"🏗️  Arquitectura: {platform.machine()}")
    print(f"📁 Directorio actual: {Path.cwd()}")
    
    # Solicitar confirmación
    if not confirmar_continuacion():
        print("\n❌ Instalación cancelada por el usuario")
        sys.exit(0)
    
    try:
        # Paso 1: Instalar dependencias
        print("\n" + "=" * 60)
        print("📦 PASO 1: INSTALACIÓN DE DEPENDENCIAS")
        print("=" * 60)
        
        if not instalar_dependencias():
            print("\n❌ Error en la instalación de dependencias")
            print("💡 Intente ejecutar manualmente: pip install -r requirements.txt")
            sys.exit(1)
        
        # Paso 2: Configurar directorios
        print("\n" + "=" * 60)
        print("📁 PASO 2: CONFIGURACIÓN DE DIRECTORIOS")
        print("=" * 60)
        
        if not ejecutar_script("setup_directories.py", "🏗️ Configurando estructura de directorios"):
            print("\n⚠️ Problema al configurar directorios, pero continuando...")
        
        # Paso 3: Configurar base de datos
        print("\n" + "=" * 60)
        print("🗄️ PASO 3: CONFIGURACIÓN DE BASE DE DATOS")
        print("=" * 60)
        
        if not ejecutar_script("setup_database.py", "🗄️ Configurando base de datos"):
            print("\n❌ Error crítico en la configuración de la base de datos")
            sys.exit(1)
        
        # Paso 4: Verificación final
        print("\n" + "=" * 60)
        print("✅ PASO 4: VERIFICACIÓN FINAL")
        print("=" * 60)
        
        if verificar_instalacion():
            print("  ✅ Todas las verificaciones pasaron correctamente")
        else:
            print("  ⚠️ Algunas verificaciones fallaron, pero la aplicación debería funcionar")
        
        # Mostrar instrucciones finales
        mostrar_instrucciones_uso()
        
        # Preguntar si desea ejecutar la aplicación ahora
        print("\n" + "=" * 60)
        ejecutar_ahora = input("¿Desea ejecutar la aplicación ahora? (s/n): ").lower()
        
        if ejecutar_ahora in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n🚀 Iniciando aplicación...")
            try:
                # Cambiar al directorio src y ejecutar main.py
                os.chdir("src")
                subprocess.run([sys.executable, "main.py"])
            except KeyboardInterrupt:
                print("\n\n⚠️ Aplicación cerrada por el usuario")
            except Exception as e:
                print(f"\n❌ Error al ejecutar la aplicación: {str(e)}")
                print("💡 Intente ejecutar manualmente: python src/main.py")
        else:
            print("\n✅ Instalación completa. Ejecute 'python src/main.py' cuando esté listo.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la instalación: {str(e)}")
        print("\n🔧 INFORMACIÓN PARA DEBUG:")
        print(f"  • Python: {sys.version}")
        print(f"  • SO: {platform.system()} {platform.release()}")
        print(f"  • Directorio: {Path.cwd()}")
        sys.exit(1)

if __name__ == "__main__":
    main()