# src/presentation/views/correo_cliente_view.py
"""
Vista para la gestión de plantillas de correo para clientes.
Esta vista permite crear, editar y gestionar plantillas de email predefinidas.
"""
import tkinter as tk
from tkinter import ttk, messagebox

# Importamos el servicio que maneja la lógica de negocio para plantillas de correo
from application.services.correo_cliente_service import CorreoClienteService

class CorreoClienteView(ttk.Frame):
    """Clase que representa la vista para gestionar plantillas de correo."""
    
    def __init__(self, parent):
        """
        Constructor de la vista de plantillas de correo.
        
        Args:
            parent: Widget padre donde se mostrará esta vista
        """
        super().__init__(parent)  # Llamamos al constructor de la clase padre
        
        # Inicializar el servicio que maneja la lógica de negocio
        self.service = CorreoClienteService()
        
        # Variable para controlar si estamos editando una plantilla existente
        self.editing_id = None  # None = creando nueva, número = editando existente
        
        # Configurar la interfaz de usuario
        self.setup_ui()
        # Cargar los datos desde la base de datos
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario dividida en formulario y lista."""
        # Panel principal dividido verticalmente (formulario arriba, lista abajo)
        self.main_paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior (formulario para crear/editar plantillas)
        self.form_frame = ttk.LabelFrame(self.main_paned, text="Editor de Plantilla", padding=10)
        
        # Panel inferior (lista de plantillas existentes)
        self.list_frame = ttk.LabelFrame(self.main_paned, text="Plantillas Existentes", padding=10)
        
        # Agregar los paneles al contenedor principal
        self.main_paned.add(self.form_frame, weight=2)   # Formulario ocupa más espacio
        self.main_paned.add(self.list_frame, weight=1)   # Lista ocupa menos espacio
        
        # Configurar cada panel por separado
        self.setup_form()     # Configurar el formulario de edición
        self.setup_list()     # Configurar la lista de plantillas
    
    def setup_form(self):
        """Configura el formulario para crear/editar plantillas de correo."""
        # Título del formulario que cambia según el modo (crear/editar)
        self.title_label = ttk.Label(
            self.form_frame, 
            text="Nueva Plantilla de Correo",
            font=("Arial", 12, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Campo: Nombre de la plantilla
        ttk.Label(self.form_frame, text="Nombre de la plantilla:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.nombre_entry = ttk.Entry(self.form_frame, width=40)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.W + tk.E, pady=(0, 5), padx=(5, 0))
        
        # Campo: Asunto del correo
        ttk.Label(self.form_frame, text="Asunto:").grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.asunto_entry = ttk.Entry(self.form_frame, width=40)
        self.asunto_entry.grid(row=2, column=1, sticky=tk.W + tk.E, pady=(0, 5), padx=(5, 0))
        
        # Campo: Contenido de la plantilla (área de texto grande)
        ttk.Label(self.form_frame, text="Contenido:").grid(
            row=3, column=0, sticky=tk.NW, pady=(0, 5)
        )
        
        # Frame para el área de texto con scrollbar
        text_frame = ttk.Frame(self.form_frame)
        text_frame.grid(row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=(0, 5), padx=(5, 0))
        
        # Área de texto con scrollbar vertical
        self.contenido_text = tk.Text(
            text_frame, 
            height=8,      # 8 líneas de alto
            width=50,      # 50 caracteres de ancho
            wrap=tk.WORD,  # Ajustar palabras automáticamente
            font=("Arial", 10)
        )
        
        # Scrollbar para el área de texto
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.contenido_text.yview)
        self.contenido_text.config(yscrollcommand=scrollbar.set)
        
        # Posicionar el área de texto y scrollbar
        self.contenido_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para los botones de acción
        buttons_frame = ttk.Frame(self.form_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, sticky=tk.E, pady=(15, 0))
        
        # Botón para limpiar el formulario
        self.clear_button = ttk.Button(
            buttons_frame,
            text="Limpiar",
            command=self.clear_form
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón para cancelar edición
        self.cancel_button = ttk.Button(
            buttons_frame,
            text="Cancelar",
            style="Secondary.TButton",
            command=self.cancel_edit
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón para guardar la plantilla
        self.save_button = ttk.Button(
            buttons_frame,
            text="Guardar",
            style="Success.TButton",
            command=self.save_template
        )
        self.save_button.pack(side=tk.LEFT)
        
        # Configurar el grid para que se expanda correctamente
        self.form_frame.grid_columnconfigure(1, weight=1)  # La columna 1 se expande
        self.form_frame.grid_rowconfigure(3, weight=1)     # La fila 3 (contenido) se expande
    
    def setup_list(self):
        """Configura la lista de plantillas existentes."""
        # Frame para la barra de herramientas
        toolbar_frame = ttk.Frame(self.list_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo de búsqueda para filtrar plantillas
        ttk.Label(toolbar_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()  # Variable para almacenar el texto de búsqueda
        # Ejecutar filtro cada vez que cambie el texto
        self.search_var.trace("w", self.filter_list)
        
        self.search_entry = ttk.Entry(
            toolbar_frame, 
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para crear nueva plantilla
        ttk.Button(
            toolbar_frame,
            text="Nueva Plantilla",
            style="Primary.TButton",
            command=self.new_template
        ).pack(side=tk.RIGHT)
        
        # Frame para la lista con scrollbar
        list_container = ttk.Frame(self.list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # Lista de plantillas (Treeview configurado como lista)
        self.template_tree = ttk.Treeview(
            list_container,
            columns=("id", "nombre", "asunto"),  # Columnas de datos
            show="headings",                     # Solo mostrar encabezados
            height=6                            # 6 filas visibles
        )
        
        # Configurar las columnas
        self.template_tree.column("id", width=50, anchor=tk.CENTER)
        self.template_tree.column("nombre", width=200)
        self.template_tree.column("asunto", width=300)
        
        # Configurar los encabezados
        self.template_tree.heading("id", text="ID")
        self.template_tree.heading("nombre", text="Nombre")
        self.template_tree.heading("asunto", text="Asunto")
        
        # Scrollbar para la lista
        list_scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.template_tree.yview)
        self.template_tree.config(yscrollcommand=list_scrollbar.set)
        
        # Posicionar la lista y scrollbar
        self.template_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar eventos de la lista
        self.template_tree.bind("<Double-1>", self.on_template_double_click)  # Doble clic = editar
        self.template_tree.bind("<ButtonRelease-1>", self.on_template_select)  # Clic = seleccionar
        
        # Menú contextual (clic derecho)
        self.context_menu = tk.Menu(self.template_tree, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.edit_selected)
        self.context_menu.add_command(label="Duplicar", command=self.duplicate_selected)
        self.context_menu.add_command(label="Eliminar", command=self.delete_selected)
        
        # Vincular el clic derecho con el menú contextual
        self.template_tree.bind("<Button-3>", self.show_context_menu)
    
    def load_data(self):
        """Carga las plantillas desde la base de datos y las muestra en la lista."""
        # Limpiar la lista actual
        for item in self.template_tree.get_children():
            self.template_tree.delete(item)
        
        # Obtener todas las plantillas desde el servicio
        plantillas = self.service.obtener_todas()
        
        # Insertar cada plantilla en la lista
        for plantilla in plantillas:
            # Truncar el asunto si es muy largo para que se vea bien en la tabla
            asunto_mostrar = plantilla.asunto
            if len(asunto_mostrar) > 50:  # Si tiene más de 50 caracteres
                asunto_mostrar = asunto_mostrar[:47] + "..."  # Cortar y agregar puntos
            
            self.template_tree.insert("", tk.END, values=(
                plantilla.id,
                plantilla.nombre,
                asunto_mostrar
            ))
    
    def filter_list(self, *args):
        """
        Filtra la lista de plantillas según el texto de búsqueda.
        Se ejecuta automáticamente cada vez que cambia el texto de búsqueda.
        """
        # Obtener el texto de búsqueda en minúsculas
        search_text = self.search_var.get().lower()
        
        # Limpiar la lista actual
        for item in self.template_tree.get_children():
            self.template_tree.delete(item)
        
        # Obtener todas las plantillas
        plantillas = self.service.obtener_todas()
        
        # Filtrar e insertar solo las plantillas que coinciden
        for plantilla in plantillas:
            # Verificar si el texto está en el nombre o asunto
            if (search_text in plantilla.nombre.lower() or 
                search_text in plantilla.asunto.lower()):
                
                # Truncar el asunto si es necesario
                asunto_mostrar = plantilla.asunto
                if len(asunto_mostrar) > 50:
                    asunto_mostrar = asunto_mostrar[:47] + "..."
                
                self.template_tree.insert("", tk.END, values=(
                    plantilla.id,
                    plantilla.nombre,
                    asunto_mostrar
                ))
    
    def on_template_select(self, event):
        """Maneja el evento cuando se selecciona una plantilla en la lista."""
        # Por ahora no hacemos nada especial, pero está preparado para funcionalidades futuras
        pass
    
    def on_template_double_click(self, event):
        """Maneja el doble clic en una plantilla para editarla."""
        self.edit_selected()
    
    def show_context_menu(self, event):
        """Muestra el menú contextual cuando se hace clic derecho."""
        # Identificar en qué elemento se hizo clic
        item = self.template_tree.identify_row(event.y)
        if item:
            # Seleccionar el elemento y mostrar el menú
            self.template_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def new_template(self):
        """Prepara el formulario para crear una nueva plantilla."""
        self.clear_form()  # Limpiar el formulario
        self.editing_id = None  # Asegurarse de que estamos en modo creación
        self.title_label.config(text="Nueva Plantilla de Correo")
        self.nombre_entry.focus()  # Poner el foco en el primer campo
    
    def edit_selected(self):
        """Edita la plantilla seleccionada en la lista."""
        # Obtener la plantilla seleccionada
        selected = self.template_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar una plantilla para editar")
            return
        
        # Obtener el ID de la plantilla seleccionada
        item = self.template_tree.item(selected[0])
        template_id = item["values"][0]
        
        # Obtener la plantilla completa desde la base de datos
        plantilla = self.service.obtener_por_id(template_id)
        if not plantilla:
            messagebox.showerror("Error", f"No se encontró la plantilla con ID {template_id}")
            return
        
        # Cambiar a modo edición
        self.editing_id = template_id
        self.title_label.config(text=f"Editar Plantilla: {plantilla.nombre}")
        
        # Rellenar el formulario con los datos de la plantilla
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, plantilla.nombre)
        
        self.asunto_entry.delete(0, tk.END)
        self.asunto_entry.insert(0, plantilla.asunto)
        
        self.contenido_text.delete(1.0, tk.END)  # Para Text widget se usa 1.0, no 0
        self.contenido_text.insert(1.0, plantilla.plantilla)
        
        # Poner el foco en el primer campo
        self.nombre_entry.focus()
    
    def duplicate_selected(self):
        """Duplica la plantilla seleccionada."""
        # Obtener la plantilla seleccionada
        selected = self.template_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar una plantilla para duplicar")
            return
        
        # Obtener el ID de la plantilla seleccionada
        item = self.template_tree.item(selected[0])
        template_id = item["values"][0]
        
        # Obtener la plantilla completa
        plantilla = self.service.obtener_por_id(template_id)
        if not plantilla:
            messagebox.showerror("Error", "No se encontró la plantilla seleccionada")
            return
        
        # Cambiar a modo creación con los datos de la plantilla existente
        self.editing_id = None  # Modo creación
        self.title_label.config(text="Nueva Plantilla de Correo (Duplicada)")
        
        # Rellenar el formulario con los datos, pero cambiar el nombre
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, f"Copia de {plantilla.nombre}")
        
        self.asunto_entry.delete(0, tk.END)
        self.asunto_entry.insert(0, plantilla.asunto)
        
        self.contenido_text.delete(1.0, tk.END)
        self.contenido_text.insert(1.0, plantilla.plantilla)
        
        # Poner el foco en el nombre para que el usuario pueda cambiarlo
        self.nombre_entry.focus()
        self.nombre_entry.select_range(0, tk.END)  # Seleccionar todo el texto
    
    def delete_selected(self):
        """Elimina la plantilla seleccionada después de confirmar."""
        # Obtener la plantilla seleccionada
        selected = self.template_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Debe seleccionar una plantilla para eliminar")
            return
        
        # Obtener el ID y nombre de la plantilla
        item = self.template_tree.item(selected[0])
        template_id = item["values"][0]
        template_name = item["values"][1]
        
        # Confirmar la eliminación
        if not messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar la plantilla '{template_name}'?\n\nEsta acción no se puede deshacer."
        ):
            return
        
        # Intentar eliminar la plantilla
        try:
            if self.service.eliminar(template_id):
                messagebox.showinfo("Éxito", "Plantilla eliminada correctamente")
                
                # Si estábamos editando esta plantilla, limpiar el formulario
                if self.editing_id == template_id:
                    self.clear_form()
                    self.editing_id = None
                    self.title_label.config(text="Nueva Plantilla de Correo")
                
                # Recargar la lista
                self.load_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la plantilla")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la plantilla: {str(e)}")
    
    def save_template(self):
        """Guarda la plantilla (crea nueva o actualiza existente)."""
        # Obtener los datos del formulario
        nombre = self.nombre_entry.get().strip()
        asunto = self.asunto_entry.get().strip()
        contenido = self.contenido_text.get(1.0, tk.END).strip()  # Para Text se usa 1.0, tk.END
        
        # Validar que todos los campos estén llenos
        if not nombre:
            messagebox.showerror("Error", "El nombre de la plantilla es obligatorio")
            self.nombre_entry.focus()
            return
        
        if not asunto:
            messagebox.showerror("Error", "El asunto es obligatorio")
            self.asunto_entry.focus()
            return
        
        if not contenido:
            messagebox.showerror("Error", "El contenido de la plantilla es obligatorio")
            self.contenido_text.focus()
            return
        
        # Intentar guardar la plantilla
        try:
            if self.editing_id:
                # Estamos editando una plantilla existente
                plantilla = self.service.actualizar(self.editing_id, nombre, asunto, contenido)
                messagebox.showinfo("Éxito", "Plantilla actualizada correctamente")
            else:
                # Estamos creando una plantilla nueva
                plantilla = self.service.crear(nombre, asunto, contenido)
                messagebox.showinfo("Éxito", "Plantilla creada correctamente")
            
            # Limpiar el formulario y volver al modo de creación
            self.clear_form()
            self.editing_id = None
            self.title_label.config(text="Nueva Plantilla de Correo")
            
            # Recargar la lista para mostrar los cambios
            self.load_data()
            
        except ValueError as e:
            # Error de validación de negocio (ej: nombre duplicado)
            messagebox.showerror("Error", str(e))
        except Exception as e:
            # Error técnico inesperado
            messagebox.showerror("Error", f"Error al guardar la plantilla: {str(e)}")
    
    def clear_form(self):
        """Limpia todos los campos del formulario."""
        self.nombre_entry.delete(0, tk.END)
        self.asunto_entry.delete(0, tk.END)
        self.contenido_text.delete(1.0, tk.END)
    
    def cancel_edit(self):
        """Cancela la edición actual y limpia el formulario."""
        # Volver al modo de creación
        self.editing_id = None
        self.title_label.config(text="Nueva Plantilla de Correo")
        
        # Limpiar el formulario
        self.clear_form()
        
        # Quitar la selección de la lista
        self.template_tree.selection_remove(self.template_tree.selection())