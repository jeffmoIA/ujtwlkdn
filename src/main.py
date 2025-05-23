#!/usr/bin/env python3
"""
Archivo principal de la aplicación.
Este será el punto de entrada de nuestro programa.
"""
import os
import sys

def main():
    """
    Función principal que se ejecuta al iniciar la aplicación.
    Configura y arranca la interfaz gráfica.
    """
    print("🚀 ¡Aplicación iniciada correctamente!")
    print("📁 Proyecto: Aplicación con Tkinter y SQLAlchemy")
    print("✅ Entorno configurado exitosamente")
    
    # Configurar rutas de importación
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Agregar rutas al sys.path
    sys.path.insert(0, project_root)
    sys.path.insert(0, current_dir)
    
    try:
        # Importar y ejecutar el controlador de aplicación
        print("📱 Cargando controlador de aplicación...")
        from application_controller import start_application
        start_application()
        
    except ImportError as e:
        print(f"❌ Error de importación: {str(e)}")
        print("\n🔧 DIAGNÓSTICO:")
        print(f"   📁 Directorio actual: {current_dir}")
        print(f"   📁 Directorio proyecto: {project_root}")
        print(f"   🔍 Buscando: application_controller.py")
        
        # Verificar si el archivo existe
        controller_path = os.path.join(current_dir, "application_controller.py")
        if os.path.exists(controller_path):
            print(f"   ✅ Archivo encontrado: {controller_path}")
        else:
            print(f"   ❌ Archivo NO encontrado: {controller_path}")
            print("\n💡 SOLUCIÓN:")
            print("   1. Crear el archivo 'application_controller.py' en la carpeta 'src'")
            print("   2. Copiar el código del controlador en ese archivo")
        
        input("\nPresione Enter para salir...")
        
    except Exception as e:
        print(f"❌ Error al iniciar la aplicación: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nPresione Enter para salir...")

# Esta línea hace que main() se ejecute solo si ejecutamos este archivo directamente
if __name__ == "__main__":
    main()