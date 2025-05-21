#!/usr/bin/env python3
"""
Archivo principal de la aplicación.
Este será el punto de entrada de nuestro programa.
"""
import os
import sys

# Agrega la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar el controlador de la aplicación
from presentation.app import App

def main():
    """
    Función principal que se ejecuta al iniciar la aplicación.
    Configura y arranca la interfaz gráfica.
    """
    print("🚀 ¡Aplicación iniciada correctamente!")
    print("📁 Proyecto: Aplicación con Tkinter y SQLAlchemy")
    print("✅ Entorno configurado exitosamente")
    
    # Crear y arrancar la aplicación
    app = App()
    app.start()

# Esta línea hace que main() se ejecute solo si ejecutamos este archivo directamente
if __name__ == "__main__":
    main()