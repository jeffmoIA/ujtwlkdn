# src/presentation/main_window.py
"""
Ventana principal de la aplicación.
Esta clase define la estructura y comportamiento de la interfaz gráfica.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from presentation.utils.tk_styles import aplicar_tema
from presentation.views.login_view import LoginView
from presentation.views.nodos_ipran_view import NodosIPRANView
from presentation.views.nodos_gpon_view import NodosGPONView
from presentation.views.correo_cliente_view import CorreoClienteView
from application.services.auth_service import AuthService

class MainWindow:
    """Clase que representa la ventana principal de la aplicación."""
    
    def __init__(self, root):
        """
        Constructor de la ventana principal.
        
        Args:
            root: Ventana raíz de Tkinter
        """
        self.root = root
        self.root.title("Gestor de Red")
        self.root.geometry("1000x600")  # Tamaño inicial
        self.root.minsize(800, 500)  # Tamaño mínimo
        
        # Aplicar el tema personalizado
        self.style = aplicar_tema(self.root)
        
        # Servicios
        self.auth_service = AuthService()
        
        # Usuario actual
        self.current_user = None
        
        # Iniciar la aplicación
        self.setup_ui()
        
        # Mostrar la pantalla de login primero
        self.show_login()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal que contendrá todo
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior para el encabezado
        self.header_frame = ttk.Frame(self.main_frame, style="Secondary.TFrame")
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Título de la aplicación
        self.title_label = ttk.Label(
            self.header_frame, 
            text="Gestor de Red", 
            font=("Arial", 16, "bold"),
            foreground="white",
            background="#2c3e50",
            padding=(10, 5)
        )
        self.title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Información del usuario (inicialmente oculta)
        self.user_frame = ttk.Frame(self.header_frame, style="Secondary.TFrame")
        self.user_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        self.user_label = ttk.Label(
            self.user_frame, 
            text="", 
            foreground="white",
            background="#2c3e50",
            padding=(5, 0)
        )
        self.user_label.pack(side=tk.LEFT)
        
        self.logout_button = ttk.Button(
            self.user_frame, 
            text="Cerrar Sesión", 
            style="Secondary.TButton",
            command=self.logout
        )
        self.logout_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Ocultar la información del usuario hasta que se inicie sesión
        self.user_frame.pack_forget()
        
        # Frame de contenido (cambiará según la vista)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_login(self):
        """Muestra la vista de inicio de sesión."""
        # Limpiar el frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Ocultar la información del usuario
        self.user_frame.pack_forget()
        
        # Crear y mostrar la vista de login
        login_view = LoginView(self.content_frame, self.auth_service, self.on_login_success)
    
    def on_login_success(self, user):
        """
        Callback que se ejecuta cuando el inicio de sesión es exitoso.
        
        Args:
            user: Usuario autenticado
        """
        self.current_user = user
        
        # Actualizar la información del usuario
        self.user_label.config(text=f"Usuario: {user.nombre}")
        self.user_frame.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Mostrar la vista principal
        self.show_main_view()
    
    def logout(self):
        """Cierra la sesión del usuario actual."""
        self.current_user = None
        self.show_login()
    
    def show_main_view(self):
        """Muestra la vista principal de la aplicación."""
        # Limpiar el frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Crear pestañas (notebook)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear las diferentes vistas
        self.ipran_view = NodosIPRANView(self.notebook)
        self.gpon_view = NodosGPONView(self.notebook)
        self.correo_view = CorreoClienteView(self.notebook)
        
        # Añadir las pestañas
        self.notebook.add(self.ipran_view, text="Nodos IPRAN")
        self.notebook.add(self.gpon_view, text="Nodos GPON")
        self.notebook.add(self.correo_view, text="Plantillas de Correo")