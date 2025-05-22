# src/presentation/views/nodos_gpon_view.py
"""
Vista para la gestión de nodos GPON (OLT).
Esta vista es muy similar a la de nodos IPRAN pero adaptada para equipos GPON.
"""
import tkinter as tk
from tkinter import ttk, messagebox

# Importamos el servicio que maneja la lógica de negocio para nodos GPON
from application.services.nodo_gpon_service import NodoGPONService

class NodosGPONView(ttk.Frame):
    """Clase que representa la vista para gestionar nodos GPON (OLT)."""
    
    def __init__(self, parent):
        """
        Constructor de la vista de nodos GPON.
        
        Args:
            parent: Widget padre donde se mostrará esta vista
        """
        super().__init__(parent)  # Llamamos al constructor de la clase padre (ttk.Frame)
        
        # Inicializar el servicio que maneja la lógica de negocio
        self.service = NodoGPONService()
        
        # Variable para controlar si estamos editando un nodo existente
        self.editing_id = None  # None = creando nuevo, número = editando existente
        
        # Configurar la interfaz de usuario
        self.setup_ui()
        # Cargar los datos desde la base de datos
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario dividida en panel de formulario y tabla."""
        # Panel principal dividido en dos secciones horizontales
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (formulario para crear/editar)
        self.form_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        # Panel derecho (tabla para mostrar datos)
        self.table_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        # Agregar los paneles al contenedor principal con pesos relativos
        self.paned.add(self.form_frame, weight=1)    # 25% del espacio
        self.paned.add(self.table_frame, weight=3)   # 75% del espacio
        
        # Configurar cada panel por separado
        self.setup_form()   # Configurar el formulario
        self.setup_table()  # Configurar la tabla
    
    def setup_form(self):
        """Configura el formulario para crear/editar nodos GPON."""
        # Título del formulario (cambia según si estamos creando o editando)
        self.title_label = ttk.Label(
            self.form_frame, 
            text="Nueva OLT GPON",  # OLT = Optical Line Terminal
            font=("Arial", 12, "bold"),
            padding=(0, 10)
        )
        self.title_label.pack(anchor=tk.W, padx=10, pady=(10, 20))
        
        # Frame contenedor para los campos del formulario
        self.fields_frame = ttk.Frame(self.form_frame)
        self.fields_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campo: Alias de la OLT
        self.alias_label = ttk.Label(self.fields_frame, text="Alias OLT:")
        self.alias_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.alias_entry = ttk.Entry(self.fields_frame, width=25)
        self.alias_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        # Campo: Nombre completo de la OLT
        self.nombre_label = ttk.Label(self.fields_frame, text="Nombre OLT:")
        self.nombre_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.nombre_entry = ttk.Entry(self.fields_frame, width=25)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # Campo: Dirección IP de la OLT
        self.ip_label = ttk.Label(self.fields_frame, text="IP OLT:")
        self.ip_label.grid(row=2, column=0, sticky=tk.W)
        
        self.ip_entry = ttk.Entry(self.fields_frame, width=25)
        self.ip_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Frame contenedor para los botones de acción
        self.buttons_frame = ttk.Frame(self.form_frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        # Botón para guardar (crear o actualizar)
        self.save_button = ttk.Button(
            self.buttons_frame, 
            text="Guardar", 
            style="Success.TButton",  # Estilo verde para acción positiva
            command=self.save_node     # Función que se ejecuta al hacer clic
        )
        self.save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botón para cancelar la edición
        self.cancel_button = ttk.Button(
            self.buttons_frame, 
            text="Cancelar", 
            style="Secondary.TButton",  # Estilo secundario (gris/azul)
            command=self.cancel_edit      # Función que se ejecuta al hacer clic
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 5))
    
    def setup_table(self):
        """Configura la tabla para mostrar los nodos GPON."""
        # Frame para la barra de herramientas superior
        self.toolbar_frame = ttk.Frame(self.table_frame)
        self.toolbar_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Título de la sección de tabla
        self.table_title = ttk.Label(
            self.toolbar_frame,
            text="OLTs GPON",
            font=("Arial", 12, "bold")
        )
        self.table_title.pack(side=tk.LEFT)
        
        # Campo de búsqueda (filtro en tiempo real)
        self.search_var = tk.StringVar()  # Variable que almacena el texto de búsqueda
        # Cada vez que cambie el texto, se ejecutará la función filter_table
        self.search_var.trace("w", self.filter_table)
        
        self.search_entry = ttk.Entry(
            self.toolbar_frame,
            width=20,
            textvariable=self.search_var  # Conectar con la variable de búsqueda
        )
        self.search_entry.pack(side=tk.RIGHT)
        
        self.search_label = ttk.Label(self.toolbar_frame, text="Buscar:")
        self.search_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Frame contenedor para la tabla con scrollbar
        self.tree_frame = ttk.Frame(self.table_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar vertical para la tabla
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tabla principal (Treeview = widget de tabla de tkinter)
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "alias", "nombre", "ip"),  # Columnas de datos
            show="headings",  # Solo mostrar encabezados, no el árbol
            yscrollcommand=self.scrollbar.set  # Conectar con scrollbar
        )
        
        # Configurar el ancho y alineación de cada columna
        self.tree.column("id", width=50, anchor=tk.CENTER)     # ID centrado, 50px
        self.tree.column("alias", width=100)                   # Alias, 100px
        self.tree.column("nombre", width=250)                  # Nombre, 250px
        self.tree.column("ip", width=120)                      # IP, 120px
        
        # Configurar los títulos de los encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("alias", text="Alias")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("ip", text="IP")
        
        # Mostrar la tabla en el frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Conectar la scrollbar con la tabla
        self.scrollbar.config(command=self.tree.yview)
        
        # Configurar eventos de la tabla
        self.tree.bind("<Double-1>", self.on_item_double_click)  # Doble clic = editar
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)  # Clic simple = seleccionar
        
        # Menú contextual (clic derecho)
        self.context_menu = tk.Menu(self.tree, tearoff=0)  # tearoff=0 evita que se pueda separar
        self.context_menu.add_command(label="Editar", command=self.edit_selected)
        self.context_menu.add_command(label="Eliminar", command=self.delete_selected)
        
        # Vincular el clic derecho con el menú contextual
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def load_data(self):
        """Carga los datos de los nodos GPON desde la base de datos y los muestra en la tabla."""
        # Limpiar todos los elementos actuales de la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los nodos GPON desde el servicio
        nodos = self.service.obtener_todos()
        
        # Insertar cada nodo en la tabla
        for nodo in nodos:
            self.tree.insert("", tk.END, values=(
                nodo.id,           # ID del nodo
                nodo.alias_olt,    # Alias de la OLT
                nodo.nombre_olt,   # Nombre de la OLT
                nodo.ip_olt        # IP de la OLT
            ))
    
    def filter_table(self, *args):
        """
        Filtra la tabla según el texto de búsqueda ingresado.
        Se ejecuta automáticamente cada vez que cambia el texto de búsqueda.
        """
        # Obtener el texto de búsqueda en minúsculas para comparación insensible a mayúsculas
        search_text = self.search_var.get().lower()
        
        # Limpiar la tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los nodos desde la base de datos
        nodos = self.service.obtener_todos()
        
        # Filtrar e insertar solo los nodos que coinciden con la búsqueda
        for nodo in nodos:
            # Verificar si el texto de búsqueda está en alguno de los campos
            if (search_text in str(nodo.id).lower() or           # Buscar en ID
                search_text in nodo.alias_olt.lower() or         # Buscar en alias
                search_text in nodo.nombre_olt.lower() or        # Buscar en nombre
                search_text in nodo.ip_olt.lower()):             # Buscar en IP
                
                # Si coincide, agregar a la tabla
                self.tree.insert("", tk.END, values=(
                    nodo.id,
                    nodo.alias_olt,
                    nodo.nombre_olt,
                    nodo.ip_olt
                ))
    
    def on_item_select(self, event):
        """
        Maneja el evento cuando se selecciona un elemento en la tabla.
        Aquí se podrían habilitar/deshabilitar botones según la selección.
        """
        # Por ahora no hacemos nada especial, pero está preparado para futuras funcionalidades
        pass
    
    def on_item_double_click(self, event):
        """Maneja el evento de doble clic en un elemento de la tabla para editarlo."""
        self.edit_selected()  # Llamar a la función de edición
    
    def show_context_menu(self, event):
        """Muestra el menú contextual cuando se hace clic derecho en un elemento."""
        # Identificar en qué fila se hizo clic
        item = self.tree.identify_row(event.y)
        if item:
            # Si hay un elemento válido, seleccionarlo y mostrar el menú
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)  # Mostrar en posición del mouse
    
    def edit_selected(self):
        """Edita el nodo GPON seleccionado en la tabla."""
        # Obtener el elemento seleccionado
        selected = self.tree.selection()
        if not selected:
            return  # Si no hay nada seleccionado, salir
        
        # Obtener los datos del elemento seleccionado
        item = self.tree.item(selected[0])
        node_id = item["values"][0]  # El ID está en la primera columna
        
        # Obtener el nodo completo desde la base de datos
        nodo = self.service.obtener_por_id(node_id)
        if not nodo:
            messagebox.showerror("Error", f"No se encontró la OLT con ID {node_id}")
            return
        
        # Cambiar a modo edición
        self.editing_id = node_id
        self.title_label.config(text=f"Editar OLT GPON")
        
        # Rellenar el formulario con los datos actuales del nodo
        self.alias_entry.delete(0, tk.END)                    # Limpiar campo
        self.alias_entry.insert(0, nodo.alias_olt)            # Insertar valor actual
        
        self.nombre_entry.delete(0, tk.END)                   # Limpiar campo
        self.nombre_entry.insert(0, nodo.nombre_olt)          # Insertar valor actual
        
        self.ip_entry.delete(0, tk.END)                       # Limpiar campo
        self.ip_entry.insert(0, nodo.ip_olt)                  # Insertar valor actual
    
    def delete_selected(self):
        """Elimina el nodo GPON seleccionado después de confirmar."""
        # Obtener el elemento seleccionado
        selected = self.tree.selection()
        if not selected:
            return  # Si no hay nada seleccionado, salir
        
        # Obtener el ID del nodo a eliminar
        item = self.tree.item(selected[0])
        node_id = item["values"][0]
        
        # Mostrar diálogo de confirmación
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta OLT?"):
            return  # Si el usuario cancela, salir
        
        # Intentar eliminar el nodo
        try:
            if self.service.eliminar(node_id):
                messagebox.showinfo("Éxito", "OLT eliminada correctamente")
                self.load_data()  # Recargar la tabla para reflejar los cambios
            else:
                messagebox.showerror("Error", "No se pudo eliminar la OLT")
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir
            messagebox.showerror("Error", f"Error al eliminar la OLT: {str(e)}")
    
    def save_node(self):
        """Guarda el nodo GPON (crea uno nuevo o actualiza uno existente)."""
        # Obtener los datos del formulario
        alias = self.alias_entry.get().strip()      # .strip() elimina espacios al inicio/final
        nombre = self.nombre_entry.get().strip()
        ip = self.ip_entry.get().strip()
        
        # Validar que todos los campos estén llenos
        if not alias or not nombre or not ip:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar formato de la IP usando expresión regular
        import re
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            messagebox.showerror("Error", "La IP no tiene un formato válido")
            return
        
        # Intentar guardar el nodo
        try:
            if self.editing_id:
                # Estamos editando un nodo existente
                nodo = self.service.actualizar(self.editing_id, alias, nombre, ip)
                messagebox.showinfo("Éxito", "OLT actualizada correctamente")
            else:
                # Estamos creando un nodo nuevo
                nodo = self.service.crear(alias, nombre, ip)
                messagebox.showinfo("Éxito", "OLT creada correctamente")
            
            # Limpiar el formulario y volver al modo de creación
            self.cancel_edit()
            
            # Recargar la tabla para mostrar los cambios
            self.load_data()
            
        except ValueError as e:
            # Error de validación de negocio (ej: alias duplicado)
            messagebox.showerror("Error", str(e))
        except Exception as e:
            # Error técnico inesperado
            messagebox.showerror("Error", f"Error al guardar la OLT: {str(e)}")
    
    def cancel_edit(self):
        """Cancela la edición actual y limpia el formulario."""
        # Volver al modo de creación
        self.editing_id = None
        self.title_label.config(text="Nueva OLT GPON")
        
        # Limpiar todos los campos del formulario
        self.alias_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.ip_entry.delete(0, tk.END)