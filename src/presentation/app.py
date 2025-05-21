# src/presentation/app.py
"""
Controlador principal de la aplicación.
Gestiona la inicialización y el flujo entre las diferentes ventanas.
"""
import tkinter as tk
import os
import sys

# Agregamos la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar vistas
from presentation.views.login_view import LoginView
from presentation.views.main_view import MainView

class App:
    """Controlador principal de la aplicación."""
    
    def __init__(self):
        """Inicializa la aplicación."""
        self.root = None
        self.main_view = None
        
    def start(self):
        """Inicia la aplicación."""
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar la ventana principal por ahora
        
        # Aplicar tema y configuraciones
        self.setup_theme()
        
        # Mostrar la ventana de login
        self.show_login()
        
        # Iniciar el bucle principal de la aplicación
        self.root.mainloop()
        
    def setup_theme(self):
        """Configura el tema y apariencia general de la aplicación."""
        # Estilo para ttk
        style = tk.ttk.Style()
        
        # Configurar un tema básico
        style.configure("TButton", padding=6, relief="flat", background="#ddd")
        style.configure("TEntry", padding=6)
        
    def show_login(self):
        """Muestra la ventana de login."""
        # Primero hacemos visible la ventana principal
        self.root.deiconify()
        # Configuramos un tamaño mínimo
        self.root.geometry("500x400")
        # La centramos en la pantalla
        self.center_window(self.root)
        # Ahora mostramos el login
        login_window = LoginView(self.root, on_login_success=self.on_login_success)
        # Asegurémonos de que la ventana de login está por encima
        login_window.lift()
        login_window.focus_force()
        # Imprimimos un mensaje para confirmar
        print("Ventana de login mostrada. Si no la ves, verifica otras ventanas o la barra de tareas.")
        
    def on_login_success(self, username):
        """
        Función que se ejecuta cuando el login es exitoso.
        
        Args:
            username: Nombre de usuario logueado
        """
        # Mostrar la ventana principal
        self.root.deiconify()  # Mostrar la ventana principal
        
        # Crear la vista principal
        self.main_view = MainView(self.root, username)
        
        # Configurar la ventana principal
        self.setup_main_window()
        
    def setup_main_window(self):
        """Configura la ventana principal."""
        # Título y tamaño
        self.root.title("Mi Aplicación")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Centrar la ventana
        self.center_window(self.root)
        
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def center_window(self, window):
        """Centra una ventana en la pantalla."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')
        
    def on_close(self):
        """Función que se ejecuta al cerrar la aplicación."""
        self.root.destroy()