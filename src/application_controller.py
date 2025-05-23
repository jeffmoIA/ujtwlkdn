# src/application_controller.py
"""
Controlador principal de la aplicación que maneja el flujo entre login y aplicación principal.
Este enfoque evita los conflictos de widgets de Tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Agregar rutas para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
sys.path.append(current_dir)

# Importar servicios
try:
    from application.services.auth_service import AuthService
except ImportError:
    print("⚠️ AuthService no disponible - usando modo de desarrollo")
    AuthService = None

# Importar estilos
try:
    from presentation.utils.tk_styles import aplicar_tema
except ImportError:
    print("⚠️ Estilos no disponibles - usando estilos básicos")
    def aplicar_tema(root):
        style = ttk.Style()
        style.theme_use('clam')
        return style

class ApplicationController:
    """Controlador principal que maneja todo el flujo de la aplicación."""
    
    def __init__(self):
        """Inicializa el controlador de la aplicación."""
        self.root = None
        self.current_user = None
        
        # Inicializar auth_service si está disponible
        try:
            self.auth_service = AuthService() if AuthService else None
        except Exception as e:
            print(f"⚠️ Error al inicializar AuthService: {str(e)}")
            self.auth_service = None
        
        # Estado de la aplicación
        self.state = "login"  # "login" o "main"
        
    def start(self):
        """Inicia la aplicación."""
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Red")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        
        # Aplicar tema
        try:
            self.style = aplicar_tema(self.root)
        except Exception as e:
            print(f"⚠️ Error al aplicar tema: {str(e)}")
            self.style = ttk.Style()
        
        # Centrar ventana
        self.center_window()
        
        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Mostrar login inicialmente
        self.show_login_screen()
        
        # Iniciar loop principal
        self.root.mainloop()
    
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def clear_window(self):
        """Limpia completamente la ventana."""
        for widget in self.root.winfo_children():
            try:
                widget.destroy()
            except Exception as e:
                print(f"⚠️ Error al limpiar widget: {str(e)}")
    
    def show_login_screen(self):
        """Muestra la pantalla de login."""
        self.state = "login"
        self.clear_window()
        
        # Frame principal para login
        login_frame = ttk.Frame(self.root)
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame centrado para el formulario
        center_frame = ttk.Frame(login_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        title_label = ttk.Label(
            center_frame,
            text="🔐 Sistema de Gestión de Red",
            font=("Arial", 18, "bold"),
            padding=(0, 0, 0, 20)
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(
            center_frame,
            text="Iniciar Sesión",
            font=("Arial", 14),
            padding=(0, 0, 0, 30)
        )
        subtitle_label.pack()
        
        # Frame del formulario con borde
        form_frame = ttk.LabelFrame(center_frame, text="Credenciales", padding=20)
        form_frame.pack(padx=20, pady=20)
        
        # Campo usuario
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, width=25, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, pady=(0, 15), padx=(10, 0))
        
        # Campo contraseña
        ttk.Label(form_frame, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, width=25, show="•", font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, pady=(0, 20), padx=(10, 0))
        
        # Botón login
        self.login_btn = ttk.Button(
            form_frame,
            text="🚀 Iniciar Sesión",
            command=self.handle_login,
            width=20
        )
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Mensaje de ayuda
        help_label = ttk.Label(
            center_frame,
            text="💡 Usuario: admin | Contraseña: admin123",
            font=("Arial", 10),
            foreground="gray"
        )
        help_label.pack(pady=(20, 0))
        
        # Eventos de teclado
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Focus inicial
        self.root.after(100, self.username_entry.focus)
    
    def handle_login(self):
        """Maneja el proceso de login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar campos
        if not username:
            messagebox.showerror("Error", "Ingrese su nombre de usuario")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Error", "Ingrese su contraseña")
            self.password_entry.focus()
            return
        
        # Deshabilitar botón durante autenticación
        self.login_btn.config(state=tk.DISABLED, text="🔄 Autenticando...")
        self.root.update()
        
        try:
            # Crear usuario simulado para desarrollo
            class MockUser:
                def __init__(self, username, nombre):
                    self.usuario = username
                    self.nombre = nombre
            
            user = None
            
            # Credenciales de desarrollo
            if username == "admin" and password == "admin123":
                user = MockUser("admin", "Administrador del Sistema")
            elif username == "test" and password == "test":
                user = MockUser("test", "Usuario de Prueba")
            else:
                # Intentar con base de datos si está disponible
                try:
                    if self.auth_service:
                        user = self.auth_service.autenticar(username, password)
                except Exception as e:
                    print(f"⚠️ Error en autenticación BD: {str(e)}")
            
            if user:
                # Login exitoso
                self.current_user = user
                messagebox.showinfo("Éxito", f"¡Bienvenido, {user.nombre}!")
                self.show_main_application()
            else:
                # Login fallido
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la autenticación:\n{str(e)}")
            print(f"Error de autenticación: {str(e)}")
        
        finally:
            # Rehabilitar botón si aún existe
            try:
                self.login_btn.config(state=tk.NORMAL, text="🚀 Iniciar Sesión")
            except:
                pass
    
    def show_main_application(self):
        """Muestra la aplicación principal con pestañas."""
        self.state = "main"
        self.clear_window()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con información del usuario
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X)
        header_frame.config(style="Secondary.TFrame")
        
        # Título de la aplicación
        title_label = ttk.Label(
            header_frame,
            text="Gestor de Red - Sistema de Gestión de Infraestructura",
            font=("Arial", 14, "bold"),
            padding=(15, 8)
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Info del usuario y logout
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        user_label = ttk.Label(
            user_frame,
            text=f"👤 {self.current_user.nombre} ({self.current_user.usuario})",
            font=("Arial", 10),
            padding=(8, 0)
        )
        user_label.pack(side=tk.LEFT, padx=(0, 10))
        
        logout_btn = ttk.Button(
            user_frame,
            text="Cerrar Sesión",
            command=self.handle_logout
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Crear pestañas
        self.create_tabs()
        
        print("✅ Aplicación principal cargada correctamente")
    
    def create_tabs(self):
        """Crea las pestañas de la aplicación."""
        try:
            # Pestaña 1: Nodos IPRAN
            print("📡 Creando pestaña de Nodos IPRAN...")
            try:
                from presentation.views.nodos_ipran_view import NodosIPRANView
                ipran_view = NodosIPRANView(self.notebook)
                self.notebook.add(ipran_view, text="📡 Nodos IPRAN")
            except Exception as e:
                print(f"⚠️ Error en Nodos IPRAN: {str(e)}")
                self.create_placeholder_tab("📡 Nodos IPRAN", "Gestión de Nodos IPRAN")
            
            # Pestaña 2: Nodos GPON
            print("🌐 Creando pestaña de Nodos GPON...")
            try:
                from presentation.views.nodos_gpon_view import NodosGPONView
                gpon_view = NodosGPONView(self.notebook)
                self.notebook.add(gpon_view, text="🌐 Nodos GPON")
            except Exception as e:
                print(f"⚠️ Error en Nodos GPON: {str(e)}")
                self.create_placeholder_tab("🌐 Nodos GPON", "Gestión de Nodos GPON")
            
            # Pestaña 3: Plantillas de Correo
            print("📧 Creando pestaña de Plantillas de Correo...")
            try:
                from presentation.views.correo_cliente_view import CorreoClienteView
                correo_view = CorreoClienteView(self.notebook)
                self.notebook.add(correo_view, text="📧 Plantillas Correo")
            except Exception as e:
                print(f"⚠️ Error en Plantillas Correo: {str(e)}")
                self.create_placeholder_tab("📧 Plantillas Correo", "Gestión de Plantillas de Correo")
            
            # Pestaña 4: Documentos
            print("📄 Creando pestaña de Documentos...")
            try:
                from presentation.views.documento_view import DocumentoView
                doc_view = DocumentoView(self.notebook)
                self.notebook.add(doc_view, text="📄 Documentos")
            except Exception as e:
                print(f"⚠️ Error en Documentos: {str(e)}")
                self.create_placeholder_tab("📄 Documentos", "Gestión de Documentos Técnicos")
            
            print("✅ Todas las pestañas procesadas")
            
        except Exception as e:
            print(f"❌ Error general al crear pestañas: {str(e)}")
            # Crear al menos una pestaña de inicio
            self.create_placeholder_tab("🏠 Inicio", "Bienvenido al Sistema de Gestión de Red")
    
    def create_placeholder_tab(self, title, description):
        """Crea una pestaña placeholder cuando no se puede cargar la vista real."""
        placeholder_frame = ttk.Frame(self.notebook)
        
        # Contenido de la pestaña placeholder
        content_frame = ttk.Frame(placeholder_frame)
        content_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(
            content_frame,
            text=description,
            font=("Arial", 16, "bold"),
            padding=(0, 0, 0, 20)
        )
        title_label.pack()
        
        # Mensaje
        message_label = ttk.Label(
            content_frame,
            text="Esta funcionalidad está en desarrollo.\n\nPuede que falten algunas dependencias\no que haya errores en la configuración.",
            font=("Arial", 12),
            justify=tk.CENTER,
            padding=(0, 0, 0, 20)
        )
        message_label.pack()
        
        # Botón para recargar
        reload_btn = ttk.Button(
            content_frame,
            text="🔄 Recargar Aplicación",
            command=self.show_main_application
        )
        reload_btn.pack()
        
        # Agregar pestaña al notebook
        self.notebook.add(placeholder_frame, text=title)
    
    def handle_logout(self):
        """Maneja el cierre de sesión."""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.current_user = None
            self.show_login_screen()
    
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
            self.root.destroy()

# Función para iniciar la aplicación
def start_application():
    """Función principal para iniciar la aplicación."""
    print("🎮 Iniciando controlador de aplicación...")
    app = ApplicationController()
    app.start()

if __name__ == "__main__":
    start_application()