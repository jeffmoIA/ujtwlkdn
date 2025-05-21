# src/presentation/views/login_view.py
"""
Vista de login de la aplicación.
Permite al usuario iniciar sesión en el sistema.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Agregamos la ruta del proyecto al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class LoginView(tk.Toplevel):
    """Ventana de login de la aplicación."""
    
    def __init__(self, parent, on_login_success=None):
        """
        Inicializa la ventana de login.
        
        Args:
            parent: Ventana padre
            on_login_success: Función que se ejecuta cuando el login es exitoso
        """
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        
        # Configuración de la ventana
        self.title("Iniciar Sesión")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        
        # Centrar la ventana
        self.center_window()
        
        # Crear widgets
        self.create_widgets()
        
        # Hacer que esta ventana sea modal (bloquea la interacción con la ventana padre)
        self.transient(parent)
        self.grab_set()
        
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
        
    def create_widgets(self):
        """Crea los widgets de la ventana de login."""
        # Frame principal
        main_frame = tk.Frame(self, bg="#f5f5f5", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="Bienvenido", 
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        # Frame para el formulario
        form_frame = tk.Frame(main_frame, bg="#f5f5f5")
        form_frame.pack(fill=tk.X)
        
        # Usuario
        username_label = tk.Label(
            form_frame, 
            text="Usuario:", 
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#333333",
            anchor="w"
        )
        username_label.pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Contraseña
        password_label = tk.Label(
            form_frame, 
            text="Contraseña:", 
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#333333",
            anchor="w"
        )
        password_label.pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = ttk.Entry(form_frame, width=30, show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Botón de login
        self.login_button = ttk.Button(
            form_frame,
            text="Iniciar Sesión",
            command=self.login
        )
        self.login_button.pack(fill=tk.X)
        
        # Configurar el evento Enter para iniciar sesión
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Focus en el campo de usuario
        self.username_entry.focus()
        
    def login(self):
        """Valida las credenciales del usuario e inicia sesión."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar campos vacíos
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        
        # TODO: En el futuro, aquí irá la lógica real de autenticación con la base de datos
        # Por ahora, aceptamos cualquier usuario/contraseña para fines de desarrollo
        
        # Simular éxito de login
        if self.on_login_success:
            self.on_login_success(username)
            
        # Cerrar la ventana de login
        self.destroy()