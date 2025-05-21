"""
Clase base para la aplicación de Tkinter.
Configura la ventana principal y maneja la carga de estilos.
"""
import tkinter as tk
from tkinter import ttk
import os

class App(tk.Tk):
    """Clase principal de la aplicación Tkinter."""
    
    def __init__(self, title="Mi Aplicación", size="800x600"):
        """
        Inicializa la aplicación Tkinter.
        
        Args:
            title (str): Título de la ventana principal.
            size (str): Tamaño de la ventana en formato "anchoxalto".
        """
        super().__init__()
        
        # Configuración básica de la ventana
        self.title(title)
        self.geometry(size)
        
        # Centro la ventana en la pantalla
        self._center_window()
        
        # Configurar tema y estilos
        self._setup_styles()
        
        # Contenedor principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def _center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def _setup_styles(self):
        """Configura los estilos y temas de la aplicación."""
        # Crear un estilo
        style = ttk.Style(self)
        
        # Usar el tema 'clam' que funciona bien en todas las plataformas
        style.theme_use('clam')
        
        # Configurar estilos para los widgets
        style.configure('TLabel', font=('Arial', 11))
        style.configure('TButton', font=('Arial', 11), padding=5)
        style.configure('TEntry', font=('Arial', 11), padding=5)
        
        # Estilo para encabezados
        style.configure('Heading.TLabel', font=('Arial', 14, 'bold'))
        
        # Estilo para botones de acción principal
        style.configure('Primary.TButton', background='#4CAF50', foreground='white')
        
        # Estilo para botones de acción secundaria
        style.configure('Secondary.TButton', background='#2196F3', foreground='white')
        
        # Estilo para botones de eliminación
        style.configure('Danger.TButton', background='#F44336', foreground='white')