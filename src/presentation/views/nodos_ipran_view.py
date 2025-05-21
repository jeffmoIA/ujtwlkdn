# src/presentation/views/nodos_ipran_view.py
"""
Vista para la gestión de nodos IPRAN.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from application.services.nodo_ipran_service import NodoIPRANService

class NodosIPRANView(ttk.Frame):
    """Clase que representa la vista para gestionar nodos IPRAN."""
    
    def __init__(self, parent):
        """
        Constructor de la vista de nodos IPRAN.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        # Inicializar el servicio
        self.service = NodoIPRANService()
        
        # Estado de edición
        self.editing_id = None  # ID del nodo que se está editando (None si se está creando)
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Panel principal dividido en dos
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (formulario)
        self.form_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        # Panel derecho (tabla)
        self.table_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        self.paned.add(self.form_frame, weight=1)
        self.paned.add(self.table_frame, weight=3)
        
        # Configurar el formulario
        self.setup_form()
        
        # Configurar la tabla
        self.setup_table()
    
    def setup_form(self):
        """Configura el formulario para crear/editar nodos."""
        # Título
        self.title_label = ttk.Label(
            self.form_frame, 
            text="Nuevo Nodo IPRAN", 
            font=("Arial", 12, "bold"),
            padding=(0, 10)
        )
        self.title_label.pack(anchor=tk.W, padx=10, pady=(10, 20))
        
        # Frame para los campos
        self.fields_frame = ttk.Frame(self.form_frame)
        self.fields_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Alias
        self.alias_label = ttk.Label(self.fields_frame, text="Alias:")
        self.alias_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.alias_entry = ttk.Entry(self.fields_frame, width=25)
        self.alias_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        # Nombre
        self.nombre_label = ttk.Label(self.fields_frame, text="Nombre:")
        self.nombre_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.nombre_entry = ttk.Entry(self.fields_frame, width=25)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # IP
        self.ip_label = ttk.Label(self.fields_frame, text="IP:")
        self.ip_label.grid(row=2, column=0, sticky=tk.W)
        
        self.ip_entry = ttk.Entry(self.fields_frame, width=25)
        self.ip_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Frame para los botones
        self.buttons_frame = ttk.Frame(self.form_frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        # Botón de guardar
        self.save_button = ttk.Button(
            self.buttons_frame, 
            text="Guardar", 
            style="Success.TButton",
            command=self.save_node
        )
        self.save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Botón de cancelar
        self.cancel_button = ttk.Button(
            self.buttons_frame, 
            text="Cancelar", 
            style="Secondary.TButton",
            command=self.cancel_edit
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(0, 5))
    
    def setup_table(self):
        """Configura la tabla para mostrar los nodos."""
        # Frame para la barra de herramientas
        self.toolbar_frame = ttk.Frame(self.table_frame)
        self.toolbar_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Etiqueta de título
        self.table_title = ttk.Label(
            self.toolbar_frame,
            text="Nodos IPRAN",
            font=("Arial", 12, "bold")
        )
        self.table_title.pack(side=tk.LEFT)
        
        # Campo de búsqueda
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_table)
        
        self.search_entry = ttk.Entry(
            self.toolbar_frame,
            width=20,
            textvariable=self.search_var
        )
        self.search_entry.pack(side=tk.RIGHT)
        
        self.search_label = ttk.Label(self.toolbar_frame, text="Buscar:")
        self.search_label.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Frame para la tabla con scroll
        self.tree_frame = ttk.Frame(self.table_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tabla (Treeview)
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "alias", "nombre", "ip"),
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        
        # Configurar las columnas
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("alias", width=100)
        self.tree.column("nombre", width=250)
        self.tree.column("ip", width=120)
        
        # Configurar los encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("alias", text="Alias")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("ip", text="IP")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Conectar la scrollbar
        self.scrollbar.config(command=self.tree.yview)
        
        # Eventos de la tabla
        self.tree.bind("<Double-1>", self.on_item_double_click)  # Doble clic
        self.tree.bind("<ButtonRelease-1>", self.on_item_select)  # Selección
        
        # Menú contextual
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.edit_selected)
        self.context_menu.add_command(label="Eliminar", command=self.delete_selected)
        
        self.tree.bind("<Button-3>", self.show_context_menu)  # Clic derecho
    
    def load_data(self):
        """Carga los datos de los nodos en la tabla."""
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los nodos
        nodos = self.service.obtener_todos()
        
        # Insertar los nodos en la tabla
        for nodo in nodos:
            self.tree.insert("", tk.END, values=(
                nodo.id,
                nodo.alias_nodo,
                nodo.nombre_nodo,
                nodo.ip_nodo
            ))
    
    def filter_table(self, *args):
        """Filtra la tabla según el texto de búsqueda."""
        search_text = self.search_var.get().lower()
        
        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener todos los nodos
        nodos = self.service.obtener_todos()
        
        # Filtrar e insertar los nodos en la tabla
        for nodo in nodos:
            # Si el texto de búsqueda está en alguno de los campos
            if (search_text in str(nodo.id).lower() or
                search_text in nodo.alias_nodo.lower() or
                search_text in nodo.nombre_nodo.lower() or
                search_text in nodo.ip_nodo.lower()):
                
                self.tree.insert("", tk.END, values=(
                    nodo.id,
                    nodo.alias_nodo,
                    nodo.nombre_nodo,
                    nodo.ip_nodo
                ))
    
    def on_item_select(self, event):
        """Maneja el evento de selección de un ítem en la tabla."""
        # Aquí se podrían habilitar/deshabilitar botones según si hay algo seleccionado
        pass
    
    def on_item_double_click(self, event):
        """Maneja el evento de doble clic en un ítem de la tabla."""
        self.edit_selected()
    
    def show_context_menu(self, event):
        """Muestra el menú contextual."""
        item = self.tree.identify_row(event.y)
        if item:
            # Seleccionar el ítem
            self.tree.selection_set(item)
            # Mostrar el menú
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_selected(self):
        """Edita el nodo seleccionado."""
        # Obtener el ítem seleccionado
        selected = self.tree.selection()
        if not selected:
            return
        
        # Obtener el ID del nodo
        item = self.tree.item(selected[0])
        node_id = item["values"][0]
        
        # Obtener el nodo
        nodo = self.service.obtener_por_id(node_id)
        if not nodo:
            messagebox.showerror("Error", f"No se encontró el nodo con ID {node_id}")
            return
        
        # Cambiar a modo edición
        self.editing_id = node_id
        self.title_label.config(text=f"Editar Nodo IPRAN")
        
        # Rellenar el formulario
        self.alias_entry.delete(0, tk.END)
        self.alias_entry.insert(0, nodo.alias_nodo)
        
        self.nombre_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, nodo.nombre_nodo)
        
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, nodo.ip_nodo)
    
    def delete_selected(self):
        """Elimina el nodo seleccionado."""
        # Obtener el ítem seleccionado
        selected = self.tree.selection()
        if not selected:
            return
        
        # Obtener el ID del nodo
        item = self.tree.item(selected[0])
        node_id = item["values"][0]
        
        # Confirmar la eliminación
        if not messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este nodo?"):
            return
        
        # Eliminar el nodo
        try:
            if self.service.eliminar(node_id):
                messagebox.showinfo("Éxito", "Nodo eliminado correctamente")
                self.load_data()  # Recargar la tabla
            else:
                messagebox.showerror("Error", "No se pudo eliminar el nodo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el nodo: {str(e)}")
    
    def save_node(self):
        """Guarda el nodo (crea uno nuevo o actualiza uno existente)."""
        # Obtener los datos del formulario
        alias = self.alias_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        ip = self.ip_entry.get().strip()
        
        # Validar los datos
        if not alias or not nombre or not ip:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Validar la IP
        import re
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
            messagebox.showerror("Error", "La IP no tiene un formato válido")
            return
        
        try:
            if self.editing_id:
                # Actualizar nodo existente
                nodo = self.service.actualizar(self.editing_id, alias, nombre, ip)
                messagebox.showinfo("Éxito", "Nodo actualizado correctamente")
            else:
                # Crear nuevo nodo
                nodo = self.service.crear(alias, nombre, ip)
                messagebox.showinfo("Éxito", "Nodo creado correctamente")
            
            # Limpiar el formulario
            self.cancel_edit()
            
            # Recargar la tabla
            self.load_data()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el nodo: {str(e)}")
    
    def cancel_edit(self):
        """Cancela la edición y limpia el formulario."""
        self.editing_id = None
        self.title_label.config(text="Nuevo Nodo IPRAN")
        
        # Limpiar los campos
        self.alias_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.ip_entry.delete(0, tk.END)