# src/presentation/views/main_view.py
"""
Vista principal de la aplicación.
Contiene el menú principal y la zona donde se mostrarán las diferentes secciones.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Agregamos la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class MainView(tk.Frame):
    """Ventana principal de la aplicación."""
    
    def __init__(self, parent, username):
        """
        Inicializa la ventana principal.
        
        Args:
            parent: Ventana padre
            username: Nombre de usuario logueado
        """
        super().__init__(parent)
        self.parent = parent
        self.username = username
        
        # Configuración de la ventana
        self.parent.title("Mi Aplicación")
        self.parent.geometry("800x600")
        self.parent.minsize(800, 600)
        
        # Configurar el fondo
        self.configure(bg="#f5f5f5")
        
        # Crear widgets
        self.create_widgets()
        
        # Mostrar la vista inicial
        self.show_welcome_page()
        
        # Empaquetar el frame principal
        self.pack(fill=tk.BOTH, expand=True)
        
    def create_widgets(self):
        """Crea los widgets de la ventana principal."""
        # Frame para la barra superior
        top_bar = tk.Frame(self, bg="#333333", height=50)
        top_bar.pack(fill=tk.X)
        
        # Título de la aplicación
        app_title = tk.Label(
            top_bar,
            text="Mi Aplicación",
            font=("Arial", 12, "bold"),
            bg="#333333",
            fg="white"
        )
        app_title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Información del usuario
        user_info = tk.Label(
            top_bar,
            text=f"Usuario: {self.username}",
            font=("Arial", 10),
            bg="#333333",
            fg="white"
        )
        user_info.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Crear un panel lateral y un área de contenido
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Panel de navegación (sidebar)
        self.sidebar = tk.Frame(self.paned_window, width=200, bg="#f0f0f0")
        
        # Área de contenido
        self.content_area = tk.Frame(self.paned_window, bg="#f5f5f5")
        
        # Añadir los frames al PanedWindow
        self.paned_window.add(self.sidebar, weight=1)
        self.paned_window.add(self.content_area, weight=4)
        
        # Crear menú en el sidebar
        self.create_sidebar_menu()
        
    def create_sidebar_menu(self):
        """Crea el menú en el panel lateral."""
        # Título del menú
        menu_title = tk.Label(
            self.sidebar,
            text="Menú Principal",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        menu_title.pack(pady=(20, 10), padx=10, anchor="w")
        
        # Separador
        ttk.Separator(self.sidebar, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Botones del menú
        menu_items = [
            ("Inicio", self.show_welcome_page),
            ("Gestión de Datos", self.show_data_page),
            ("Configuración", self.show_settings_page),
            ("Cerrar Sesión", self.logout)
        ]
        
        # Crear un frame para los botones
        buttons_frame = tk.Frame(self.sidebar, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear los botones
        for text, command in menu_items:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 10),
                bg="#f0f0f0",
                fg="#333333",
                bd=0,
                highlightthickness=0,
                activebackground="#e0e0e0",
                activeforeground="#333333",
                anchor="w",
                padx=10,
                pady=8,
                command=command
            )
            btn.pack(fill=tk.X, pady=2)
            
    def clear_content_area(self):
        """Limpia el área de contenido."""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def show_welcome_page(self):
        """Muestra la página de bienvenida."""
        self.clear_content_area()
        
        # Frame para el contenido
        content_frame = tk.Frame(self.content_area, bg="#f5f5f5", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(
            content_frame,
            text=f"Bienvenido, {self.username}!",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        title.pack(pady=(0, 20))
        
        # Mensaje de bienvenida
        welcome_msg = tk.Label(
            content_frame,
            text="Esta es la aplicación de ejemplo con Tkinter y SQLAlchemy.\n"
                 "Usa el menú lateral para navegar por las diferentes secciones.",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333",
            justify=tk.LEFT
        )
        welcome_msg.pack(pady=10, anchor="w")
        
    def show_data_page(self):
        """Muestra la página de gestión de datos."""
        self.clear_content_area()
        
        # Frame para el contenido
        content_frame = tk.Frame(self.content_area, bg="#f5f5f5", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(
            content_frame,
            text="Gestión de Datos",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        title.pack(pady=(0, 20))
        
        # Mensaje
        msg = tk.Label(
            content_frame,
            text="Aquí irá la funcionalidad para gestionar los datos de la aplicación.\n"
                 "Esta sección está en desarrollo.",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333",
            justify=tk.LEFT
        )
        msg.pack(pady=10, anchor="w")
        
    def show_settings_page(self):
        """Muestra la página de configuración."""
        self.clear_content_area()
        
        # Frame para el contenido
        content_frame = tk.Frame(self.content_area, bg="#f5f5f5", padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title = tk.Label(
            content_frame,
            text="Configuración",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        title.pack(pady=(0, 20))
        
        # Mensaje
        msg = tk.Label(
            content_frame,
            text="Aquí irá la funcionalidad para configurar la aplicación.\n"
                 "Esta sección está en desarrollo.",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333",
            justify=tk.LEFT
        )
        msg.pack(pady=10, anchor="w")
        
    def logout(self):
        """Cierra la sesión actual."""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            # Destruir la ventana principal y volver a mostrar el login
            self.parent.destroy()
            # Reiniciar la aplicación (esto se manejará desde app.py)