# src/presentation/views/mikrotik_view.py
"""
Vista para la gestión de equipos MikroTik.
Esta vista permite conectar, gestionar colas y obtener exports de MikroTiks.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue

from application.services.mikrotik_service import MikroTikService

class MikroTikView(ttk.Frame):
    """Clase que representa la vista para gestionar equipos MikroTik."""
    
    def __init__(self, parent):
        """
        Constructor de la vista de MikroTik.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        # Inicializar el servicio
        self.service = MikroTikService()
        
        # Estado de la aplicación
        self.mikrotik_actual = None  # MikroTik seleccionado actualmente
        self.conexion_activa = False  # Si hay conexión activa al MikroTik
        self.editing_id = None  # ID del MikroTik que se está editando
        
        # Cola para comunicación entre hilos (para operaciones de red)
        self.message_queue = queue.Queue()
        
        # Configurar la interfaz
        self.setup_ui()
        self.load_data()
        
        # Verificar mensajes de hilos cada 100ms
        self.check_queue()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Panel principal dividido en dos secciones
        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo: Gestión y conexión
        self.left_panel = ttk.Frame(self.main_paned)
        
        # Panel derecho: Lista de MikroTiks
        self.right_panel = ttk.Frame(self.main_paned)
        
        self.main_paned.add(self.left_panel, weight=2)  # 60% del espacio
        self.main_paned.add(self.right_panel, weight=1)  # 40% del espacio
        
        # Configurar paneles
        self.setup_left_panel()
        self.setup_right_panel()
    
    def setup_left_panel(self):
        """Configura el panel izquierdo con gestión de MikroTik."""
        # === SECCIÓN: SELECCIÓN DE MIKROTIK ===
        selection_frame = ttk.LabelFrame(self.left_panel, text="🔧 Seleccionar MikroTik", padding=10)
        selection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Dropdown para seleccionar MikroTik
        ttk.Label(selection_frame, text="MikroTik:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.mikrotik_var = tk.StringVar()
        self.mikrotik_combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.mikrotik_var,
            state="readonly",
            width=30
        )
        self.mikrotik_combo.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5, padx=(5, 0))
        self.mikrotik_combo.bind("<<ComboboxSelected>>", self.on_mikrotik_selected)
        
        # Botón para refrescar lista
        ttk.Button(
            selection_frame,
            text="🔄",
            width=3,
            command=self.refresh_mikrotik_list
        ).grid(row=0, column=2, padx=5, pady=5)
        
        selection_frame.grid_columnconfigure(1, weight=1)
        
        # === SECCIÓN: CONEXIÓN ===
        connection_frame = ttk.LabelFrame(self.left_panel, text="🌐 Conexión", padding=10)
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # IP del MikroTik
        ttk.Label(connection_frame, text="IP MikroTik:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(connection_frame, textvariable=self.ip_var, width=15)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Botón de ping
        self.ping_button = ttk.Button(
            connection_frame,
            text="🔍 Ping",
            command=self.ping_mikrotik,
            width=8
        )
        self.ping_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Usuario
        ttk.Label(connection_frame, text="Usuario:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.usuario_var = tk.StringVar(value="admin")
        self.usuario_entry = ttk.Entry(connection_frame, textvariable=self.usuario_var, width=15)
        self.usuario_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Contraseña
        ttk.Label(connection_frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(connection_frame, textvariable=self.password_var, show="•", width=15)
        self.password_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Botón de conectar
        self.connect_button = ttk.Button(
            connection_frame,
            text="🔗 Conectar",
            style="Primary.TButton",
            command=self.conectar_mikrotik,
            width=12
        )
        self.connect_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Estado de conexión
        self.status_label = ttk.Label(
            connection_frame,
            text="⚪ Desconectado",
            font=("Arial", 9)
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # === SECCIÓN: UPGRADE/DOWNGRADE ===
        upgrade_frame = ttk.LabelFrame(self.left_panel, text="⚡ Upgrade/Downgrade", padding=10)
        upgrade_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Selector de cola
        ttk.Label(upgrade_frame, text="Cola a modificar:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.cola_var = tk.StringVar()
        self.cola_combo = ttk.Combobox(
            upgrade_frame,
            textvariable=self.cola_var,
            state="readonly",
            width=20
        )
        self.cola_combo.grid(row=0, column=1, sticky=tk.W + tk.E, pady=5, padx=5)
        
        # Botón para obtener colas
        ttk.Button(
            upgrade_frame,
            text="📋 Obtener Colas",
            command=self.obtener_colas,
            width=12
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Ancho de banda
        ttk.Label(upgrade_frame, text="Nuevo ancho:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Frame para ancho de banda
        ancho_frame = ttk.Frame(upgrade_frame)
        ancho_frame.grid(row=1, column=1, sticky=tk.W + tk.E, pady=5, padx=5)
        
        self.ancho_var = tk.StringVar(value="10")
        self.ancho_entry = ttk.Entry(ancho_frame, textvariable=self.ancho_var, width=8)
        self.ancho_entry.pack(side=tk.LEFT)
        
        ttk.Label(ancho_frame, text="Mbps").pack(side=tk.LEFT, padx=(5, 0))
        
        # Mostrar conversión automática
        self.conversion_label = ttk.Label(
            upgrade_frame,
            text="→ 10240 Kbps (up/down)",
            font=("Arial", 9),
            foreground="blue"
        )
        self.conversion_label.grid(row=1, column=2, padx=5, pady=5)
        
        # Vincular cambio de ancho para actualizar conversión
        self.ancho_var.trace("w", self.update_conversion)
        
        # Botón aplicar cambios
        self.apply_button = ttk.Button(
            upgrade_frame,
            text="🚀 Aplicar Cambios",
            style="Success.TButton",
            command=self.aplicar_cambios,
            state=tk.DISABLED
        )
        self.apply_button.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        upgrade_frame.grid_columnconfigure(1, weight=1)
        
        # === SECCIÓN: EXPORT DE CONFIGURACIÓN ===
        export_frame = ttk.LabelFrame(self.left_panel, text="📄 Export de Configuración", padding=10)
        export_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Botones de export
        export_buttons_frame = ttk.Frame(export_frame)
        export_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(
            export_buttons_frame,
            text="📄 Obtener Export",
            command=self.obtener_export,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            export_buttons_frame,
            text="📋 Copiar",
            command=self.copiar_export,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            export_buttons_frame,
            text="🗑️ Limpiar",
            command=self.limpiar_export,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Área de texto para el export
        self.export_text = scrolledtext.ScrolledText(
            export_frame,
            height=12,
            width=50,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        self.export_text.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial en el export
        self.export_text.insert(tk.END, "# Aquí aparecerá el export completo del MikroTik\n")
        self.export_text.insert(tk.END, "# 1. Selecciona un MikroTik\n")
        self.export_text.insert(tk.END, "# 2. Conéctate con credenciales\n")
        self.export_text.insert(tk.END, "# 3. Presiona 'Obtener Export'\n")
    
    def setup_right_panel(self):
        """Configura el panel derecho con la lista de MikroTiks."""
        # === TÍTULO Y BOTONES ===
        header_frame = ttk.Frame(self.right_panel)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(
            header_frame,
            text="🔧 Lista de MikroTiks",
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT)
        
        # Botones de acción
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            buttons_frame,
            text="➕ Nuevo",
            style="Primary.TButton",
            command=self.nuevo_mikrotik,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text="✏️ Editar",
            command=self.editar_mikrotik,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            buttons_frame,
            text="🗑️ Eliminar",
            style="Danger.TButton",
            command=self.eliminar_mikrotik,
            width=8
        ).pack(side=tk.LEFT, padx=2)
        
        # === BÚSQUEDA ===
        search_frame = ttk.Frame(self.right_panel)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="🔍 Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_mikrotiks)
        
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # === LISTA DE MIKROTIKS ===
        list_frame = ttk.Frame(self.right_panel)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(
            list_frame,
            columns=("id", "nombre", "ip", "estado", "disponible"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configurar columnas
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("nombre", width=150)
        self.tree.column("ip", width=120)
        self.tree.column("estado", width=80, anchor=tk.CENTER)
        self.tree.column("disponible", width=80, anchor=tk.CENTER)
        
        # Configurar encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("ip", text="IP")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("disponible", text="Ping")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Eventos
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        # === ESTADÍSTICAS ===
        stats_frame = ttk.LabelFrame(self.right_panel, text="📊 Estadísticas", padding=5)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="Total: 0 | Activos: 0 | Disponibles: 0",
            font=("Arial", 9)
        )
        self.stats_label.pack()
        
        # Botón para verificar conectividad masiva
        ttk.Button(
            stats_frame,
            text="🏓 Verificar Todos",
            command=self.verificar_conectividad_masiva,
            width=15
        ).pack(pady=5)
    
    # === MÉTODOS DE DATOS ===
    
    def load_data(self):
        """Carga los datos de MikroTiks en la lista."""
        # Limpiar el tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los MikroTiks
        mikrotiks = self.service.obtener_todos()
        
        # Insertar en el tree
        for mtk in mikrotiks:
            estado_icon = {
                "activo": "🟢",
                "inactivo": "🔴",
                "mantenimiento": "🟡",
                "error": "❌"
            }.get(mtk.estado, "⚪")
            
            ping_icon = "✅" if mtk.disponible else "❌"
            
            self.tree.insert("", tk.END, values=(
                mtk.id,
                mtk.nombre,
                mtk.ip_mikrotik,
                f"{estado_icon} {mtk.estado.title()}",
                ping_icon
            ))
        
        # Actualizar estadísticas
        self.update_statistics()
        
        # Actualizar dropdown de MikroTiks
        self.refresh_mikrotik_list()
    
    def refresh_mikrotik_list(self):
        """Refresca la lista de MikroTiks en el dropdown."""
        mikrotiks = self.service.obtener_todos()
        
        # Crear lista de opciones: "ID - Nombre (IP)"
        opciones = []
        for mtk in mikrotiks:
            opcion = f"{mtk.id} - {mtk.nombre} ({mtk.ip_mikrotik})"
            opciones.append(opcion)
        
        # Actualizar combobox
        self.mikrotik_combo['values'] = opciones
        
        # Si no hay selección, limpiar
        if not opciones:
            self.mikrotik_var.set("")
            self.mikrotik_actual = None
        
    def filter_mikrotiks(self, *args):
        """Filtra la lista de MikroTiks según el texto de búsqueda."""
        search_text = self.search_var.get().lower()
        
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los MikroTiks
        mikrotiks = self.service.obtener_todos()
        
        # Filtrar e insertar
        for mtk in mikrotiks:
            if (search_text in mtk.nombre.lower() or
                search_text in mtk.ip_mikrotik.lower() or
                search_text in mtk.estado.lower() or
                search_text in (mtk.modelo or "").lower() or
                search_text in (mtk.ubicacion or "").lower()):
                
                estado_icon = {
                    "activo": "🟢",
                    "inactivo": "🔴", 
                    "mantenimiento": "🟡",
                    "error": "❌"
                }.get(mtk.estado, "⚪")
                
                ping_icon = "✅" if mtk.disponible else "❌"
                
                self.tree.insert("", tk.END, values=(
                    mtk.id,
                    mtk.nombre,
                    mtk.ip_mikrotik,
                    f"{estado_icon} {mtk.estado.title()}",
                    ping_icon
                ))
    
    def update_statistics(self):
        """Actualiza las estadísticas mostradas."""
        try:
            stats = self.service.obtener_estadisticas()
            
            total = stats.get("total", 0)
            activos = stats.get("por_estado", {}).get("activo", 0)
            disponibles = stats.get("disponibilidad", {}).get("disponibles", 0)
            
            self.stats_label.config(
                text=f"Total: {total} | Activos: {activos} | Disponibles: {disponibles}"
            )
        except Exception as e:
            self.stats_label.config(text="Error al obtener estadísticas")
            print(f"Error en estadísticas: {str(e)}")
    
    # === MÉTODOS DE EVENTOS ===
    
    def on_mikrotik_selected(self, event):
        """Maneja la selección de un MikroTik en el dropdown."""
        seleccion = self.mikrotik_var.get()
        if not seleccion:
            self.mikrotik_actual = None
            return
        
        # Extraer ID del formato "ID - Nombre (IP)"
        try:
            id_str = seleccion.split(" - ")[0]
            mikrotik_id = int(id_str)
            
            # Obtener el MikroTik
            self.mikrotik_actual = self.service.obtener_por_id(mikrotik_id)
            
            if self.mikrotik_actual:
                # Actualizar campos de conexión
                self.ip_var.set(self.mikrotik_actual.ip_mikrotik)
                self.usuario_var.set(self.mikrotik_actual.usuario_acceso or "admin")
                self.password_var.set(self.mikrotik_actual.contrasena_acceso or "")
                
                # Resetear estado de conexión
                self.conexion_activa = False
                self.status_label.config(text="⚪ Desconectado")
                self.apply_button.config(state=tk.DISABLED)
                
                # Limpiar colas
                self.cola_combo['values'] = []
                self.cola_var.set("")
                
        except (ValueError, IndexError) as e:
            print(f"Error al procesar selección: {str(e)}")
            self.mikrotik_actual = None
    
    def on_tree_select(self, event):
        """Maneja la selección en el tree de MikroTiks."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            mikrotik_id = item["values"][0]
            
            # Buscar en el dropdown y seleccionar
            for i, opcion in enumerate(self.mikrotik_combo['values']):
                if opcion.startswith(f"{mikrotik_id} - "):
                    self.mikrotik_combo.current(i)
                    self.on_mikrotik_selected(None)
                    break
    
    def on_tree_double_click(self, event):
        """Maneja el doble clic en el tree."""
        self.editar_mikrotik()
    
    def update_conversion(self, *args):
        """Actualiza la etiqueta de conversión Mbps → Kbps."""
        try:
            mbps = float(self.ancho_var.get() or 0)
            kbps = int(mbps * 1024)
            self.conversion_label.config(text=f"→ {kbps} Kbps (up/down)")
        except ValueError:
            self.conversion_label.config(text="→ Ingrese un número válido")
    
    # === MÉTODOS DE ACCIONES ===
    
    def ping_mikrotik(self):
        """Hace ping al MikroTik seleccionado."""
        ip = self.ip_var.get().strip()
        if not ip:
            messagebox.showwarning("Advertencia", "Ingrese una IP válida")
            return
        
        # Cambiar estado del botón durante el ping
        self.ping_button.config(state=tk.DISABLED, text="🔄 Ping...")
        self.update()
        
        # Hacer ping en hilo separado
        def ping_thread():
            try:
                resultado = self.service.hacer_ping(ip)
                self.message_queue.put(("ping_result", resultado, ip))
            except Exception as e:
                self.message_queue.put(("ping_error", str(e), ip))
        
        threading.Thread(target=ping_thread, daemon=True).start()
    
    def conectar_mikrotik(self):
        """Conecta al MikroTik seleccionado."""
        if not self.mikrotik_actual:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik primero")
            return
        
        # Actualizar credenciales del MikroTik actual
        usuario = self.usuario_var.get().strip()
        password = self.password_var.get()
        
        if not usuario:
            messagebox.showerror("Error", "Ingrese un usuario")
            return
        
        if not password:
            if not messagebox.askyesno("Confirmar", "¿Conectar sin contraseña?"):
                return
        
        # Actualizar credenciales en base de datos
        try:
            self.service.actualizar(
                self.mikrotik_actual.id,
                usuario=usuario,
                contrasena=password
            )
        except Exception as e:
            print(f"Error al actualizar credenciales: {str(e)}")
        
        # Cambiar estado del botón
        self.connect_button.config(state=tk.DISABLED, text="🔄 Conectando...")
        self.status_label.config(text="🔄 Conectando...")
        self.update()
        
        # Conectar en hilo separado
        def connect_thread():
            try:
                exito, mensaje, conexion = self.service.conectar_mikrotik(self.mikrotik_actual.id)
                
                # Cerrar conexión inmediatamente (solo era para probar)
                if conexion:
                    try:
                        conexion.close()
                    except:
                        pass
                
                self.message_queue.put(("connect_result", exito, mensaje))
            except Exception as e:
                self.message_queue.put(("connect_error", str(e)))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def obtener_colas(self):
        """Obtiene las colas del MikroTik."""
        if not self.mikrotik_actual:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik primero")
            return
        
        if not self.conexion_activa:
            messagebox.showwarning("Advertencia", "Debe conectarse al MikroTik primero")
            return
        
        def get_queues_thread():
            try:
                exito, mensaje, colas = self.service.obtener_colas(self.mikrotik_actual.id)
                self.message_queue.put(("queues_result", exito, mensaje, colas))
            except Exception as e:
                self.message_queue.put(("queues_error", str(e)))
        
        threading.Thread(target=get_queues_thread, daemon=True).start()
    
    def aplicar_cambios(self):
        """Aplica los cambios de ancho de banda a la cola seleccionada."""
        if not self.mikrotik_actual:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik")
            return
        
        if not self.conexion_activa:
            messagebox.showwarning("Advertencia", "Debe conectarse al MikroTik primero")
            return
        
        cola = self.cola_var.get()
        if not cola:
            messagebox.showwarning("Advertencia", "Seleccione una cola")
            return
        
        try:
            mbps = float(self.ancho_var.get() or 0)
            if mbps <= 0:
                raise ValueError("El ancho debe ser mayor a 0")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ancho de banda válido")
            return
        
        # Confirmar cambios
        kbps = int(mbps * 1024)
        if not messagebox.askyesno(
            "Confirmar Cambios",
            f"¿Aplicar {mbps} Mbps ({kbps} Kbps) a la cola '{cola}'?\n\n"
            f"⚠️ Esto modificará la configuración del MikroTik."
        ):
            return
        
        # Aplicar en hilo separado
        def apply_thread():
            try:
                exito, mensaje = self.service.modificar_cola(
                    self.mikrotik_actual.id, cola, mbps
                )
                self.message_queue.put(("apply_result", exito, mensaje))
            except Exception as e:
                self.message_queue.put(("apply_error", str(e)))
        
        threading.Thread(target=apply_thread, daemon=True).start()
    
    def obtener_export(self):
        """Obtiene el export completo del MikroTik."""
        if not self.mikrotik_actual:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik primero")
            return
        
        if not self.conexion_activa:
            messagebox.showwarning("Advertencia", "Debe conectarse al MikroTik primero")
            return
        
        # Limpiar área de texto
        self.export_text.delete(1.0, tk.END)
        self.export_text.insert(tk.END, "🔄 Obteniendo export completo...\n")
        self.update()
        
        # Obtener export en hilo separado
        def export_thread():
            try:
                exito, mensaje, export_data = self.service.obtener_export_completo(self.mikrotik_actual.id)
                self.message_queue.put(("export_result", exito, mensaje, export_data))
            except Exception as e:
                self.message_queue.put(("export_error", str(e)))
        
        threading.Thread(target=export_thread, daemon=True).start()
    
    def copiar_export(self):
        """Copia el export al portapapeles."""
        try:
            export_content = self.export_text.get(1.0, tk.END).strip()
            
            if not export_content or export_content.startswith("#"):
                messagebox.showwarning("Advertencia", "No hay export para copiar")
                return
            
            # Copiar al portapapeles
            self.clipboard_clear()
            self.clipboard_append(export_content)
            
            messagebox.showinfo("Éxito", "Export copiado al portapapeles")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar: {str(e)}")
    
    def limpiar_export(self):
        """Limpia el área de export."""
        self.export_text.delete(1.0, tk.END)
        self.export_text.insert(tk.END, "# Área de export limpiada\n")
        self.export_text.insert(tk.END, "# Presiona 'Obtener Export' para ver la configuración\n")
    
    def verificar_conectividad_masiva(self):
        """Verifica la conectividad de todos los MikroTiks."""
        if not messagebox.askyesno(
            "Verificar Conectividad",
            "¿Verificar conectividad de todos los MikroTiks?\n\n"
            "Esto puede tomar varios segundos."
        ):
            return
        
        # Ejecutar en hilo separado
        def verify_all_thread():
            try:
                resultados = self.service.verificar_conectividad_masiva()
                self.message_queue.put(("verify_all_result", resultados))
            except Exception as e:
                self.message_queue.put(("verify_all_error", str(e)))
        
        threading.Thread(target=verify_all_thread, daemon=True).start()
    
    # === MÉTODOS CRUD ===
    
    def nuevo_mikrotik(self):
        """Abre ventana para crear nuevo MikroTik."""
        self.abrir_dialogo_mikrotik()
    
    def editar_mikrotik(self):
        """Edita el MikroTik seleccionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik para editar")
            return
        
        item = self.tree.item(selection[0])
        mikrotik_id = item["values"][0]
        
        mikrotik = self.service.obtener_por_id(mikrotik_id)
        if not mikrotik:
            messagebox.showerror("Error", "MikroTik no encontrado")
            return
        
        self.abrir_dialogo_mikrotik(mikrotik)
    
    def eliminar_mikrotik(self):
        """Elimina el MikroTik seleccionado."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un MikroTik para eliminar")
            return
        
        item = self.tree.item(selection[0])
        mikrotik_id = item["values"][0]
        mikrotik_nombre = item["values"][1]
        
        if not messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Eliminar el MikroTik '{mikrotik_nombre}'?\n\n"
            "Esta acción no se puede deshacer."
        ):
            return
        
        try:
            if self.service.eliminar(mikrotik_id):
                messagebox.showinfo("Éxito", "MikroTik eliminado correctamente")
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el MikroTik")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def abrir_dialogo_mikrotik(self, mikrotik=None):
        """
        Abre el diálogo para crear/editar MikroTik.
        
        Args:
            mikrotik: MikroTik a editar (None para crear nuevo)
        """
        # Crear ventana de diálogo
        dialog = tk.Toplevel(self)
        dialog.title("Nuevo MikroTik" if not mikrotik else f"Editar MikroTik: {mikrotik.nombre}")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Crear Nuevo MikroTik" if not mikrotik else "Editar MikroTik"
        ttk.Label(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Variables
        nombre_var = tk.StringVar(value=mikrotik.nombre if mikrotik else "")
        ip_var = tk.StringVar(value=mikrotik.ip_mikrotik if mikrotik else "")
        usuario_var = tk.StringVar(value=mikrotik.usuario_acceso if mikrotik else "admin")
        password_var = tk.StringVar(value=mikrotik.contrasena_acceso if mikrotik else "")
        modelo_var = tk.StringVar(value=mikrotik.modelo if mikrotik and mikrotik.modelo else "")
        version_var = tk.StringVar(value=mikrotik.version_routeros if mikrotik and mikrotik.version_routeros else "")
        ubicacion_var = tk.StringVar(value=mikrotik.ubicacion if mikrotik and mikrotik.ubicacion else "")
        cliente_id_var = tk.StringVar(value=mikrotik.cliente_id if mikrotik and mikrotik.cliente_id else "")
        cliente_nombre_var = tk.StringVar(value=mikrotik.cliente_nombre if mikrotik and mikrotik.cliente_nombre else "")
        
        # Campos del formulario
        campos = [
            ("Nombre*:", nombre_var, False),
            ("IP*:", ip_var, False),
            ("Usuario:", usuario_var, False),
            ("Contraseña:", password_var, True),
            ("Modelo:", modelo_var, False),
            ("Versión RouterOS:", version_var, False),
            ("Ubicación:", ubicacion_var, False),
            ("ID Cliente:", cliente_id_var, False),
            ("Nombre Cliente:", cliente_nombre_var, False),
        ]
        
        entries = {}
        for i, (label, variable, is_password) in enumerate(campos, start=1):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if is_password:
                entry = ttk.Entry(main_frame, textvariable=variable, show="•", width=25)
            else:
                entry = ttk.Entry(main_frame, textvariable=variable, width=25)
            
            entry.grid(row=i, column=1, sticky=tk.W + tk.E, pady=5, padx=(10, 0))
            entries[label] = entry
        
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Nota sobre campos obligatorios
        ttk.Label(
            main_frame,
            text="* Campos obligatorios",
            font=("Arial", 9),
            foreground="gray"
        ).grid(row=len(campos) + 1, column=0, columnspan=2, pady=(10, 0))
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(campos) + 2, column=0, columnspan=2, pady=(20, 0))
        
        # Función para guardar
        def guardar():
            try:
                # Validar campos obligatorios
                if not nombre_var.get().strip():
                    messagebox.showerror("Error", "El nombre es obligatorio")
                    entries["Nombre*:"].focus()
                    return
                
                if not ip_var.get().strip():
                    messagebox.showerror("Error", "La IP es obligatoria")
                    entries["IP*:"].focus()
                    return
                
                # Crear o actualizar
                if mikrotik:
                    # Actualizar MikroTik existente
                    mikrotik_actualizado = self.service.actualizar(
                        mikrotik.id,
                        nombre=nombre_var.get().strip(),
                        ip=ip_var.get().strip(),
                        usuario=usuario_var.get().strip(),
                        contrasena=password_var.get(),
                        modelo=modelo_var.get().strip() or None,
                        version=version_var.get().strip() or None,
                        ubicacion=ubicacion_var.get().strip() or None,
                        cliente_id=cliente_id_var.get().strip() or None,
                        cliente_nombre=cliente_nombre_var.get().strip() or None
                    )
                    
                    if mikrotik_actualizado:
                        messagebox.showinfo("Éxito", "MikroTik actualizado correctamente")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar el MikroTik")
                        return
                else:
                    # Crear nuevo MikroTik
                    nuevo_mikrotik = self.service.crear(
                        nombre=nombre_var.get().strip(),
                        ip=ip_var.get().strip(),
                        usuario=usuario_var.get().strip(),
                        contrasena=password_var.get(),
                        modelo=modelo_var.get().strip(),
                        version=version_var.get().strip(),
                        ubicacion=ubicacion_var.get().strip(),
                        cliente_id=cliente_id_var.get().strip(),
                        cliente_nombre=cliente_nombre_var.get().strip()
                    )
                    
                    messagebox.showinfo("Éxito", "MikroTik creado correctamente")
                
                # Recargar datos y cerrar diálogo
                self.load_data()
                dialog.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error de Validación", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        # Botones
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            width=12
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Guardar",
            style="Primary.TButton",
            command=guardar,
            width=12
        ).pack(side=tk.LEFT)
        
        # Focus en primer campo
        entries["Nombre*:"].focus()
    
    # === PROCESAMIENTO DE MENSAJES DE HILOS ===
    
    def check_queue(self):
        """Verifica mensajes de hilos en segundo plano."""
        try:
            while True:
                message_type, *args = self.message_queue.get_nowait()
                self.process_message(message_type, *args)
        except queue.Empty:
            pass
        
        # Programar siguiente verificación
        self.after(100, self.check_queue)
    
    def process_message(self, message_type, *args):
        """
        Procesa mensajes de hilos en segundo plano.
        
        Args:
            message_type: Tipo de mensaje
            *args: Argumentos del mensaje
        """
        try:
            if message_type == "ping_result":
                resultado, ip = args
                self.ping_button.config(state=tk.NORMAL, text="🔍 Ping")
                
                if resultado:
                    messagebox.showinfo("Ping Exitoso", f"✅ {ip} responde correctamente")
                else:
                    messagebox.showwarning("Ping Fallido", f"❌ {ip} no responde")
                
                # Actualizar disponibilidad si es el MikroTik actual
                if self.mikrotik_actual and ip == self.mikrotik_actual.ip_mikrotik:
                    try:
                        self.service.verificar_conectividad(self.mikrotik_actual.id)
                        self.load_data()  # Recargar para actualizar estado
                    except Exception as e:
                        print(f"Error al actualizar disponibilidad: {str(e)}")
            
            elif message_type == "ping_error":
                error_msg, ip = args
                self.ping_button.config(state=tk.NORMAL, text="🔍 Ping")
                messagebox.showerror("Error de Ping", f"Error al hacer ping a {ip}:\n{error_msg}")
            
            elif message_type == "connect_result":
                exito, mensaje = args
                self.connect_button.config(state=tk.NORMAL, text="🔗 Conectar")
                
                if exito:
                    self.conexion_activa = True
                    self.status_label.config(text="✅ Conectado", foreground="green")
                    self.apply_button.config(state=tk.NORMAL)
                    messagebox.showinfo("Conexión Exitosa", mensaje)
                else:
                    self.conexion_activa = False
                    self.status_label.config(text="❌ Error de conexión", foreground="red")
                    self.apply_button.config(state=tk.DISABLED)
                    messagebox.showerror("Error de Conexión", mensaje)
            
            elif message_type == "connect_error":
                error_msg = args[0]
                self.connect_button.config(state=tk.NORMAL, text="🔗 Conectar")
                self.conexion_activa = False
                self.status_label.config(text="❌ Error de conexión", foreground="red")
                messagebox.showerror("Error de Conexión", f"Error inesperado:\n{error_msg}")
            
            elif message_type == "queues_result":
                exito, mensaje, colas = args
                
                if exito:
                    # Actualizar dropdown de colas
                    nombres_colas = [cola.get('name', f"Cola {i+1}") for i, cola in enumerate(colas)]
                    self.cola_combo['values'] = nombres_colas
                    
                    if nombres_colas:
                        self.cola_combo.current(0)  # Seleccionar primera cola
                        messagebox.showinfo("Colas Obtenidas", f"Se encontraron {len(colas)} colas")
                    else:
                        messagebox.showwarning("Sin Colas", "No se encontraron colas en el MikroTik")
                else:
                    messagebox.showerror("Error", f"Error al obtener colas:\n{mensaje}")
            
            elif message_type == "queues_error":
                error_msg = args[0]
                messagebox.showerror("Error", f"Error al obtener colas:\n{error_msg}")
            
            elif message_type == "apply_result":
                exito, mensaje = args
                
                if exito:
                    messagebox.showinfo("Cambios Aplicados", mensaje)
                    # Actualizar export automáticamente después de cambios
                    self.obtener_export()
                else:
                    messagebox.showerror("Error", f"Error al aplicar cambios:\n{mensaje}")
            
            elif message_type == "apply_error":
                error_msg = args[0]
                messagebox.showerror("Error", f"Error al aplicar cambios:\n{error_msg}")
            
            elif message_type == "export_result":
                exito, mensaje, export_data = args
                
                # Limpiar área de texto
                self.export_text.delete(1.0, tk.END)
                
                if exito:
                    self.export_text.insert(tk.END, export_data)
                    messagebox.showinfo("Export Obtenido", "Export completo obtenido exitosamente")
                else:
                    self.export_text.insert(tk.END, f"# Error al obtener export:\n# {mensaje}")
                    messagebox.showerror("Error", f"Error al obtener export:\n{mensaje}")
            
            elif message_type == "export_error":
                error_msg = args[0]
                self.export_text.delete(1.0, tk.END)
                self.export_text.insert(tk.END, f"# Error inesperado al obtener export:\n# {error_msg}")
                messagebox.showerror("Error", f"Error al obtener export:\n{error_msg}")
            
            elif message_type == "verify_all_result":
                resultados = args[0]
                
                # Recargar datos para mostrar estados actualizados
                self.load_data()
                
                # Mostrar resumen
                total = resultados["total_verificados"]
                disponibles = resultados["disponibles"]
                no_disponibles = resultados["no_disponibles"]
                
                mensaje = f"Verificación completada:\n\n"
                mensaje += f"• Total verificados: {total}\n"
                mensaje += f"• Disponibles: {disponibles}\n"
                mensaje += f"• No disponibles: {no_disponibles}"
                
                messagebox.showinfo("Verificación Completa", mensaje)
            
            elif message_type == "verify_all_error":
                error_msg = args[0]
                messagebox.showerror("Error", f"Error en verificación masiva:\n{error_msg}")
            
        except Exception as e:
            print(f"Error al procesar mensaje {message_type}: {str(e)}")
            messagebox.showerror("Error", f"Error al procesar operación:\n{str(e)}")