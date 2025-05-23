# src/presentation/views/login_view.py
"""
Vista de login de la aplicación.
Permite al usuario iniciar sesión en el sistema.
"""
import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(ttk.Frame):
    """Vista de login de la aplicación que hereda de ttk.Frame."""
    
    def __init__(self, parent, auth_service=None, on_login_success=None):
        """
        Inicializa la vista de login.
        
        Args:
            parent: Widget padre donde se mostrará esta vista
            auth_service: Servicio de autenticación (opcional para testing)
            on_login_success: Función callback que se ejecuta cuando el login es exitoso
        """
        # Llamar al constructor de la clase padre (ttk.Frame)
        super().__init__(parent)
        
        # Guardar referencias
        self.parent = parent
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        
        # Configurar la vista para ocupar todo el espacio disponible
        self.pack(fill=tk.BOTH, expand=True)
        
        # Crear la interfaz de usuario
        self.create_widgets()
        
        # Configurar el foco inicial
        self.after(100, self.set_initial_focus)
    
    def create_widgets(self):
        """Crea los widgets de la vista de login."""
        # Frame principal centrado
        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título de bienvenida
        title_label = ttk.Label(
            main_frame, 
            text="🔐 Iniciar Sesión", 
            font=("Arial", 18, "bold"),
            padding=(0, 0, 0, 20)
        )
        title_label.pack(pady=(0, 30))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Sistema de Gestión de Red",
            font=("Arial", 12),
            padding=(0, 0, 0, 10)
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame para el formulario con un borde
        form_frame = ttk.LabelFrame(main_frame, text="Credenciales", padding=20)
        form_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Campo: Usuario
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.username_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0), sticky=tk.W + tk.E)
        
        # Campo: Contraseña
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.password_entry = ttk.Entry(form_frame, width=25, show="•", font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, pady=(0, 20), padx=(10, 0), sticky=tk.W + tk.E)
        
        # Configurar expansión de columnas
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Frame para botones
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Botón de login
        self.login_button = ttk.Button(
            buttons_frame,
            text="🚀 Iniciar Sesión",
            style="Primary.TButton",
            command=self.login,
            width=20
        )
        self.login_button.pack(pady=5)
        
        # Mensaje de ayuda
        help_frame = ttk.Frame(main_frame)
        help_frame.pack(pady=(20, 0))
        
        help_label = ttk.Label(
            help_frame,
            text="💡 Usuario por defecto: admin / admin123",
            font=("Arial", 9),
            foreground="gray"
        )
        help_label.pack()
        
        # Configurar eventos de teclado
        self.bind_keyboard_events()
    
    def bind_keyboard_events(self):
        """Configura los eventos de teclado."""
        # Enter en cualquier campo ejecuta el login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Escape limpia los campos
        self.username_entry.bind("<Escape>", lambda e: self.clear_fields())
        self.password_entry.bind("<Escape>", lambda e: self.clear_fields())
    
    def set_initial_focus(self):
        """Establece el foco inicial en el campo de usuario."""
        self.username_entry.focus()
    
    def clear_fields(self):
        """Limpia todos los campos del formulario."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus()
    
    def login(self):
        """Valida las credenciales del usuario e inicia sesión."""
        # Obtener los datos del formulario
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar campos vacíos
        if not username:
            messagebox.showerror("Error", "Por favor, ingrese su nombre de usuario.")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Por favor, ingrese su contraseña.")
            self.password_entry.focus()
            return
        
        # Deshabilitar el botón durante la autenticación
        self.login_button.config(state=tk.DISABLED, text="🔄 Autenticando...")
        self.update()  # Actualizar la interfaz
        
        try:
            # Si no hay servicio de autenticación, usar credenciales por defecto para testing
            if not self.auth_service:
                if username == "admin" and password == "admin123":
                    # Crear un objeto usuario simulado para testing
                    class MockUser:
                        def __init__(self):
                            self.usuario = "admin"
                            self.nombre = "Administrador"
                    
                    user = MockUser()
                    success = True
                else:
                    user = None
                    success = False
            else:
                # Usar el servicio de autenticación real
                user = self.auth_service.autenticar(username, password)
                success = user is not None
            
            if success:
                # Login exitoso
                messagebox.showinfo("Éxito", f"¡Bienvenido, {user.nombre}!")
                
                # Ejecutar callback si existe
                if self.on_login_success:
                    self.on_login_success(user)
                
                # Limpiar campos por seguridad
                self.clear_fields()
            else:
                # Login fallido
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                self.password_entry.delete(0, tk.END)  # Limpiar solo la contraseña
                self.password_entry.focus()
        
        except Exception as e:
            # Error durante la autenticación
            messagebox.showerror("Error", f"Error durante la autenticación:\n{str(e)}")
            print(f"Error de autenticación: {str(e)}")
        
        finally:
            # Rehabilitar el botón
            self.login_button.config(state=tk.NORMAL, text="🚀 Iniciar Sesión")
    
    def show_register_option(self):
        """Muestra opción para registrar usuario (funcionalidad futura)."""
        messagebox.showinfo(
            "Registro", 
            "La funcionalidad de registro estará disponible en una futura versión.\n\n"
            "Por ahora, use las credenciales por defecto:\n"
            "Usuario: admin\n"
            "Contraseña: admin123"
        )