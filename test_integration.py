#!/usr/bin/env python3
"""
Script de pruebas de integración para la aplicación de gestión de red.
Este script verifica que todos los componentes funcionen correctamente.
"""
import os
import sys
from pathlib import Path
import traceback

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_banner():
    """Muestra el banner de pruebas."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🧪 PRUEBAS DE INTEGRACIÓN                             ║
║                                                              ║
║        🔍 Verificación completa del sistema                  ║
║        🐍 Python + Tkinter + SQLAlchemy                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def test_imports():
    """Prueba las importaciones básicas del sistema."""
    print("🔍 Probando importaciones básicas...")
    
    tests = [
        # Modelos de dominio
        ("domain.models.base_model", "BaseModel"),
        ("domain.models.nodo_ipran", "NodoIPRAN"),
        ("domain.models.nodo_gpon", "NodoGPON"),
        ("domain.models.usuario", "Usuario"),
        ("domain.models.correo_cliente", "CorreoCliente"),
        ("domain.models.documento", "Documento"),
        
        # Servicios
        ("application.services.nodo_ipran_service", "NodoIPRANService"),
        ("application.services.nodo_gpon_service", "NodoGPONService"),
        ("application.services.correo_cliente_service", "CorreoClienteService"),
        ("application.services.auth_service", "AuthService"),
        
        # Repositorios
        ("infrastructure.repositories.nodo_ipran_repository", "NodoIPRANRepository"),
        ("infrastructure.repositories.nodo_gpon_repository", "NodoGPONRepository"),
        ("infrastructure.repositories.correo_cliente_repository", "CorreoClienteRepository"),
        ("infrastructure.repositories.documento_repository", "DocumentoRepository"),
        
        # Vistas
        ("presentation.views.nodos_ipran_view", "NodosIPRANView"),
        ("presentation.views.nodos_gpon_view", "NodosGPONView"),
        ("presentation.views.correo_cliente_view", "CorreoClienteView"),
        ("presentation.main_window", "MainWindow"),
        
        # Configuración de BD
        ("infrastructure.database.config", "engine"),
    ]
    
    passed = 0
    failed = 0
    
    for module_path, class_name in tests:
        try:
            module = __import__(module_path, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_path}.{class_name}")
            passed += 1
        except ImportError as e:
            print(f"  ❌ {module_path}.{class_name} - ImportError: {str(e)}")
            failed += 1
        except AttributeError as e:
            print(f"  ❌ {module_path}.{class_name} - AttributeError: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {module_path}.{class_name} - Error: {str(e)}")
            failed += 1
    
    print(f"\n📊 Resultado importaciones: {passed} ✅ / {failed} ❌")
    return failed == 0

def test_database_connection():
    """Prueba la conexión a la base de datos."""
    print("\n🗄️ Probando conexión a base de datos...")
    
    try:
        from infrastructure.database.config import engine, SessionLocal
        
        # Probar conexión
        with SessionLocal() as session:
            result = session.execute("SELECT 1").fetchone()
            if result[0] == 1:
                print("  ✅ Conexión a base de datos: OK")
                return True
            else:
                print("  ❌ Conexión a base de datos: Error en consulta")
                return False
    except Exception as e:
        print(f"  ❌ Conexión a base de datos: {str(e)}")
        return False

def test_database_tables():
    """Verifica que todas las tablas existan."""
    print("\n📋 Verificando tablas de la base de datos...")
    
    try:
        from infrastructure.database.config import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        
        tablas_esperadas = [
            'usuarios', 'nodos_ipran', 'nodos_gpon', 
            'correo_cliente', 'documentos'
        ]
        
        all_ok = True
        for tabla in tablas_esperadas:
            if tabla in tablas:
                print(f"  ✅ Tabla '{tabla}': Existe")
            else:
                print(f"  ❌ Tabla '{tabla}': NO existe")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"  ❌ Error al verificar tablas: {str(e)}")
        return False

def test_services():
    """Prueba las operaciones básicas de los servicios."""
    print("\n⚙️ Probando servicios...")
    
    try:
        # Test NodoIPRANService
        print("  🔍 Probando NodoIPRANService...")
        from application.services.nodo_ipran_service import NodoIPRANService
        
        ipran_service = NodoIPRANService()
        nodos_ipran = ipran_service.obtener_todos()
        print(f"    ✅ obtener_todos(): {len(nodos_ipran)} nodos encontrados")
        
        # Test NodoGPONService
        print("  🔍 Probando NodoGPONService...")
        from application.services.nodo_gpon_service import NodoGPONService
        
        gpon_service = NodoGPONService()
        nodos_gpon = gpon_service.obtener_todos()
        print(f"    ✅ obtener_todos(): {len(nodos_gpon)} nodos encontrados")
        
        # Test CorreoClienteService
        print("  🔍 Probando CorreoClienteService...")
        from application.services.correo_cliente_service import CorreoClienteService
        
        correo_service = CorreoClienteService()
        plantillas = correo_service.obtener_todas()
        print(f"    ✅ obtener_todas(): {len(plantillas)} plantillas encontradas")
        
        # Test AuthService
        print("  🔍 Probando AuthService...")
        from application.services.auth_service import AuthService
        
        auth_service = AuthService()
        # No probamos autenticación real para evitar conflictos
        print(f"    ✅ AuthService inicializado correctamente")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en servicios: {str(e)}")
        traceback.print_exc()
        return False

def test_views_creation():
    """Prueba la creación de vistas sin mostrarlas."""
    print("\n🖼️ Probando creación de vistas...")
    
    try:
        import tkinter as tk
        
        # Crear ventana temporal para pruebas
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        # Test NodosIPRANView
        print("  🔍 Probando NodosIPRANView...")
        from presentation.views.nodos_ipran_view import NodosIPRANView
        
        frame = tk.Frame(root)
        ipran_view = NodosIPRANView(frame)
        print("    ✅ NodosIPRANView creada correctamente")
        
        # Test NodosGPONView
        print("  🔍 Probando NodosGPONView...")
        from presentation.views.nodos_gpon_view import NodosGPONView
        
        frame = tk.Frame(root)
        gpon_view = NodosGPONView(frame)
        print("    ✅ NodosGPONView creada correctamente")
        
        # Test CorreoClienteView
        print("  🔍 Probando CorreoClienteView...")
        from presentation.views.correo_cliente_view import CorreoClienteView
        
        frame = tk.Frame(root)
        correo_view = CorreoClienteView(frame)
        print("    ✅ CorreoClienteView creada correctamente")
        
        # Limpiar
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al crear vistas: {str(e)}")
        traceback.print_exc()
        return False

def test_main_window():
    """Prueba la creación de la ventana principal."""
    print("\n🏠 Probando ventana principal...")
    
    try:
        import tkinter as tk
        from presentation.main_window import MainWindow
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        # Crear MainWindow
        main_window = MainWindow(root)
        print("    ✅ MainWindow creada correctamente")
        
        # Verificar que tiene las pestañas esperadas
        if hasattr(main_window, 'notebook'):
            print("    ✅ Notebook de pestañas creado")
        else:
            print("    ⚠️ Notebook no encontrado (puede estar en modo login)")
        
        # Limpiar
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error al crear MainWindow: {str(e)}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Verifica las dependencias externas."""
    print("\n📦 Verificando dependencias externas...")
    
    dependencies = [
        'tkinter',
        'sqlalchemy', 
        'alembic',
        'passlib',
        'bcrypt',
        'PIL',  # Pillow
        'docx',  # python-docx
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep}: Disponible")
        except ImportError:
            print(f"  ❌ {dep}: NO disponible")
            all_ok = False
    
    return all_ok

def test_directory_structure():
    """Verifica la estructura de directorios."""
    print("\n📁 Verificando estructura de directorios...")
    
    expected_dirs = [
        "src",
        "src/domain",
        "src/domain/models",
        "src/application",
        "src/application/services",
        "src/infrastructure",
        "src/infrastructure/repositories",
        "src/presentation",
        "src/presentation/views",
        "recursos",
        "recursos/documentos",
        "recursos/plantillas",
    ]
    
    all_ok = True
    for dir_path in expected_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}: Existe")
        else:
            print(f"  ❌ {dir_path}: NO existe")
            all_ok = False
    
    return all_ok

def run_all_tests():
    """Ejecuta todas las pruebas."""
    test_banner()
    
    print("🚀 Iniciando pruebas de integración...")
    print("=" * 60)
    
    tests = [
        ("Estructura de directorios", test_directory_structure),
        ("Dependencias externas", test_dependencies),
        ("Importaciones básicas", test_imports),
        ("Conexión a base de datos", test_database_connection),
        ("Tablas de base de datos", test_database_tables),
        ("Servicios de aplicación", test_services),
        ("Creación de vistas", test_views_creation),
        ("Ventana principal", test_main_window),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error inesperado en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1
    
    print(f"\n📈 Total: {passed} ✅ / {failed} ❌")
    
    if failed == 0:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
        print("\n▶️  Para ejecutar la aplicación: python src/main.py")
    else:
        print(f"\n⚠️ Hay {failed} pruebas fallidas. Revise los errores antes de usar la aplicación.")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas canceladas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        traceback.print_exc()
        sys.exit(1)