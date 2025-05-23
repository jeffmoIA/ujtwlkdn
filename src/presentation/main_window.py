# src/presentation/main_window.py
"""
Ventana principal de la aplicación.
Esta clase define la estructura y comportamiento de la interfaz gráfica.
"""
import tkinter as tk
from tkinter import ttk, messagebox

# Importar el sistema de estilos personalizado
from presentation.utils.tk_styles import aplicar_tema

# Importar las vistas de la aplicación
from presentation.views.login_view import LoginView
from presentation.views.nodos_ipran_view import NodosIPRANView
from presentation.views.nodos_gpon_view import NodosGPONView
from presentation.views.correo_cliente_view import CorreoClienteView
from presentation.views.documento_view import DocumentoView

# Importar el servicio de autenticación
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
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Aplicar el tema personalizado
        self.style = aplicar_tema(self.root)
        
        # Servicios
        self.auth_service = AuthService()
        
        # Usuario actual
        self.current_user = None
        
        # Referencias a las vistas (para manejo de memoria)
        self.vistas = {}
        
        # Variable para controlar si ya se inicializó el login
        self.login_initialized = False
        
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
            text="Gestor de Red - Sistema de Gestión de Infraestructura", 
            font=("Arial", 14, "bold"),
            foreground="white",
            background="#2c3e50",
            padding=(15, 8)
        )
        self.title_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Información del usuario (inicialmente oculta)
        self.user_frame = ttk.Frame(self.header_frame, style="Secondary.TFrame")
        self.user_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Etiqueta con información del usuario
        self.user_label = ttk.Label(
            self.user_frame, 
            text="", 
            foreground="white",
            background="#2c3e50",
            font=("Arial", 10),
            padding=(8, 0)
        )
        self.user_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para cerrar sesión
        self.logout_button = ttk.Button(
            self.user_frame, 
            text="Cerrar Sesión", 
            style="Secondary.TButton",
            command=self.logout
        )
        self.logout_button.pack(side=tk.RIGHT)
        
        # Ocultar la información del usuario hasta que se inicie sesión
        self.user_frame.pack_forget()
        
        # Frame de contenido (cambiará según la vista)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
    
    def show_login(self):
        """Muestra la vista de inicio de sesión."""
        # ARREGLO: Evitar crear múltiples LoginViews
        if self.login_initialized:
            return
        
        # Limpiar el frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Limpiar referencias a vistas
        self.vistas.clear()
        
        # Ocultar la información del usuario
        self.user_frame.pack_forget()
        
        # Crear y mostrar la vista de login
        try:
            self.login_view = LoginView(self.content_frame, self.auth_service, self.on_login_success)
            self.login_initialized = True
        except Exception as e:
            print(f"Error al crear LoginView: {str(e)}")
            # Si hay error, usar autenticación automática para testing
            self.auto_login()
    
    def auto_login(self):
        """Login automático para casos de error."""
        class MockUser:
            def __init__(self):
                self.usuario = "admin"
                self.nombre = "Administrador del Sistema"
        
        user = MockUser()
        self.on_login_success(user)
    
    def on_login_success(self, user):
        """
        Callback que se ejecuta cuando el inicio de sesión es exitoso.
        
        Args:
            user: Usuario autenticado
        """
        self.current_user = user
        self.login_initialized = False  # Reset para permitir nuevo login si es necesario
        
        # Actualizar la información del usuario
        self.user_label.config(text=f"👤 {user.nombre} ({user.usuario})")
        self.user_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Mostrar la vista principal con pestañas
        self.show_main_view()
    
    def logout(self):
        """Cierra la sesión del usuario actual."""
        # Confirmar cierre de sesión
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.current_user = None
            self.login_initialized = False  # Reset login flag
            
            # ARREGLO: Limpiar completamente las vistas antes de mostrar login
            self.cleanup_views()
            self.show_login()
    
    def cleanup_views(self):
        """Limpia todas las vistas y libera memoria."""
        # Limpiar referencias a vistas
        for vista_name, vista in self.vistas.items():
            try:
                if hasattr(vista, 'destroy'):
                    vista.destroy()
            except Exception as e:
                print(f"Error al limpiar vista {vista_name}: {str(e)}")
        
        self.vistas.clear()
        
        # Limpiar widgets del frame de contenido
        for widget in self.content_frame.winfo_children():
            try:
                widget.destroy()
            except Exception as e:
                print(f"Error al limpiar widget: {str(e)}")
    
    def show_main_view(self):
        """Muestra la vista principal de la aplicación con todas las pestañas."""
        # Limpiar el frame de contenido
        self.cleanup_views()
        
        # Crear el contenedor de pestañas (notebook)
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configurar estilo del notebook
        self.style.configure("TNotebook", tabposition="n")
        self.style.configure("TNotebook.Tab", padding=[15, 8])
        
        # Crear las diferentes vistas como pestañas
        self.crear_pestanas()
        
        # Configurar evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        print("✅ Vista principal cargada con todas las pestañas")
    
    def crear_pestanas(self):
        """Crea todas las pestañas de la aplicación."""
        try:
            # 🏢 Pestaña 1: Nodos IPRAN
            print("📡 Creando pestaña de Nodos IPRAN...")
            self.vistas['ipran'] = NodosIPRANView(self.notebook)
            self.notebook.add(self.vistas['ipran'], text="📡 Nodos IPRAN")
            
            # 🌐 Pestaña 2: Nodos GPON
            print("🌐 Creando pestaña de Nodos GPON...")
            self.vistas['gpon'] = NodosGPONView(self.notebook)
            self.notebook.add(self.vistas['gpon'], text="🌐 Nodos GPON")
            
            # 📧 Pestaña 3: Plantillas de Correo
            print("📧 Creando pestaña de Plantillas de Correo...")
            self.vistas['correo'] = CorreoClienteView(self.notebook)
            self.notebook.add(self.vistas['correo'], text="📧 Plantillas Correo")
            
            # 📄 Pestaña 4: Documentos
            print("📄 Creando pestaña de Documentos...")
            self.vistas['documentos'] = DocumentoView(self.notebook)
            self.notebook.add(self.vistas['documentos'], text="📄 Documentos")
            
            print("✅ Todas las pestañas creadas exitosamente")
            
        except Exception as e:
            print(f"❌ Error al crear pestañas: {str(e)}")
            messagebox.showerror(
                "Error de Inicialización", 
                f"No se pudieron cargar todas las funcionalidades:\n\n{str(e)}\n\nAlgunas pestañas pueden no estar disponibles."
            )
    
    def on_tab_changed(self, event):
        """
        Maneja el evento de cambio de pestaña.
        
        Args:
            event: Evento de cambio de pestaña
        """
        try:
            # Obtener la pestaña seleccionada
            selection = event.widget.select()
            tab_text = event.widget.tab(selection, "text")
            
            print(f"📋 Cambiando a pestaña: {tab_text}")
            
            # Obtener el índice de la pestaña
            tab_index = self.notebook.index(selection)
            
            # Refrescar datos según la pestaña seleccionada
            if tab_index == 0 and 'ipran' in self.vistas:
                # Pestaña IPRAN
                self.vistas['ipran'].load_data()
            elif tab_index == 1 and 'gpon' in self.vistas:
                # Pestaña GPON
                self.vistas['gpon'].load_data()
            elif tab_index == 2 and 'correo' in self.vistas:
                # Pestaña Correo
                self.vistas['correo'].load_data()
            elif tab_index == 3 and 'documentos' in self.vistas:
                # Pestaña Documentos
                if hasattr(self.vistas['documentos'], 'cargar_documentos'):
                    self.vistas['documentos'].cargar_documentos()
                elif hasattr(self.vistas['documentos'], 'load_data'):
                    self.vistas['documentos'].load_data()
                
        except Exception as e:
            print(f"⚠️ Error al cambiar pestaña: {str(e)}")
    
    def refresh_all_views(self):
        """Refresca los datos de todas las vistas."""
        print("🔄 Refrescando todas las vistas...")
        
        try:
            for nombre_vista, vista in self.vistas.items():
                if hasattr(vista, 'load_data'):
                    vista.load_data()
                elif hasattr(vista, 'cargar_documentos'):
                    vista.cargar_documentos()
                    
            print("✅ Todas las vistas refrescadas")
        except Exception as e:
            print(f"❌ Error al refrescar vistas: {str(e)}")
    
    def get_current_view(self):
        """
        Obtiene la vista actualmente seleccionada.
        
        Returns:
            Vista actualmente seleccionada o None
        """
        try:
            current_tab = self.notebook.select()
            tab_index = self.notebook.index(current_tab)
            
            vista_nombres = ['ipran', 'gpon', 'correo', 'documentos']
            if 0 <= tab_index < len(vista_nombres):
                nombre_vista = vista_nombres[tab_index]
                return self.vistas.get(nombre_vista)
        except Exception as e:
            print(f"❌ Error al obtener vista actual: {str(e)}")
        
        return None
    
    def show_about(self):
        """Muestra información sobre la aplicación."""
        about_text = """
🌐 Gestor de Red v1.0

Sistema integral para la gestión de infraestructura de red.

Funcionalidades:
• 📡 Gestión de Nodos IPRAN
• 🌐 Gestión de Nodos GPON
• 📧 Plantillas de Correo
• 📄 Documentos Técnicos

Desarrollado con Python + Tkinter + SQLAlchemy
        """
        
        messagebox.showinfo("Acerca del Sistema", about_text)
    
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir de la aplicación?"):
            # Limpiar recursos
            self.cleanup_views()
            self.root.destroy()
    
    def configure_window_events(self):
        """Configura los eventos de la ventana."""
        # Configurar el cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Atajos de teclado opcionales
        self.root.bind("<Control-q>", lambda e: self.on_closing())
        self.root.bind("<F5>", lambda e: self.refresh_all_views())
        
        # Centrar la ventana al iniciar
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        # Configurar eventos después de centrar
        self.configure_window_events()