# src/presentation/views/documento_view.py (continuación)
"""
Vista para la gestión de documentos.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import io
import json
from PIL import Image, ImageTk
from datetime import datetime
import pyperclip  # Para copiar texto al portapapeles

from application.services.documento_service import DocumentoService
from application.services.documento_export_service import DocumentoExportService
from application.services.nodo_ipran_service import NodoIPRANService

class DocumentoView(ttk.Frame):
    """Clase que representa la vista para gestionar documentos."""
    
    def __init__(self, parent):
        """
        Constructor de la vista de documentos.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        # Inicializar servicios
        self.documento_service = DocumentoService()
        self.export_service = DocumentoExportService()
        self.nodo_service = NodoIPRANService()
        
        # Variables para almacenar datos temporales del documento
        self.documento_actual = {
            "titulo": "",
            "cliente_id": "",
            "cliente_nombre": "",
            "cliente_direccion": "",
            "ancho_banda": "",
            "tipo_transaccion": "UPGRADE",  # Valor predeterminado
            "tipo_topologia": "IPRAN+MIKROTIK",  # Valor predeterminado
            "ingeniero": "",
            "nodo_id": None,
            "mikrotik_ip": "",
            "contenido": {
                "ip_switch": "",
                "puerto": "",
                "vlan": "",
                "ip_publica": "",
                "mikrotik_export": "",
                "link_solarwinds": "",
                "observaciones": [],
                "correo": "",
                "imagenes": {}  # Diccionario para almacenar imágenes
            }
        }
        
        # Variable para controlar el paso actual del asistente
        self.paso_actual = 0
        
        # Configurar la interfaz
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Panel principal dividido en dos secciones
        self.paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo (lista de documentos)
        self.lista_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        # Panel derecho (contenido del documento)
        self.contenido_frame = ttk.Frame(self.paned, style="Card.TFrame")
        
        self.paned.add(self.lista_frame, weight=1)
        self.paned.add(self.contenido_frame, weight=3)
        
        # Configurar el panel de lista de documentos
        self.setup_lista_documentos()
        
        # Configurar el panel de contenido (inicialmente muestra el botón para crear nuevo documento)
        self.setup_panel_contenido()
    
    def setup_lista_documentos(self):
        """Configura el panel de lista de documentos."""
        # Título del panel
        self.lista_titulo = ttk.Label(
            self.lista_frame, 
            text="Documentos", 
            font=("Arial", 12, "bold"),
            padding=(0, 10)
        )
        self.lista_titulo.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Botones de acción
        self.botones_frame = ttk.Frame(self.lista_frame)
        self.botones_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.nuevo_btn = ttk.Button(
            self.botones_frame, 
            text="Nuevo", 
            style="Primary.TButton",
            command=self.iniciar_nuevo_documento
        )
        self.nuevo_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.eliminar_btn = ttk.Button(
            self.botones_frame, 
            text="Eliminar", 
            style="Danger.TButton",
            command=self.eliminar_documento,
            state=tk.DISABLED  # Inicialmente deshabilitado
        )
        self.eliminar_btn.pack(side=tk.LEFT)
        
        # Filtro de búsqueda
        self.filtro_frame = ttk.Frame(self.lista_frame)
        self.filtro_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.filtro_lbl = ttk.Label(self.filtro_frame, text="Buscar:")
        self.filtro_lbl.pack(side=tk.LEFT, padx=(0, 5))
        
        self.filtro_var = tk.StringVar()
        self.filtro_var.trace("w", self.filtrar_documentos)
        
        self.filtro_entry = ttk.Entry(
            self.filtro_frame,
            textvariable=self.filtro_var,
            width=20
        )
        self.filtro_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Lista de documentos con scrollbar
        self.lista_frame_scroll = ttk.Frame(self.lista_frame)
        self.lista_frame_scroll.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.lista_frame_scroll)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista (Treeview)
        self.lista = ttk.Treeview(
            self.lista_frame_scroll,
            columns=("id", "fecha", "cliente", "transaccion"),
            show="headings",
            yscrollcommand=self.scrollbar.set
        )
        
        # Configurar columnas
        self.lista.column("id", width=50, anchor=tk.CENTER)
        self.lista.column("fecha", width=80)
        self.lista.column("cliente", width=150)
        self.lista.column("transaccion", width=80)
        
        # Configurar encabezados
        self.lista.heading("id", text="ID")
        self.lista.heading("fecha", text="Fecha")
        self.lista.heading("cliente", text="Cliente")
        self.lista.heading("transaccion", text="Tipo")
        
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Conectar scrollbar
        self.scrollbar.config(command=self.lista.yview)
        
        # Evento al seleccionar un documento
        self.lista.bind("<<TreeviewSelect>>", self.seleccionar_documento)
        
        # Cargar documentos
        self.cargar_documentos()
    
    def setup_panel_contenido(self):
        """Configura el panel de contenido del documento."""
        # Limpiar el contenido anterior
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        # Panel de bienvenida
        self.bienvenida_frame = ttk.Frame(self.contenido_frame)
        self.bienvenida_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Mensaje de bienvenida
        ttk.Label(
            self.bienvenida_frame,
            text="Gestión de Documentos",
            font=("Arial", 16, "bold"),
            padding=(0, 0, 0, 10)
        ).pack()
        
        ttk.Label(
            self.bienvenida_frame,
            text="Seleccione un documento de la lista o cree uno nuevo.",
            padding=(0, 0, 0, 20)
        ).pack()
        
        # Botón grande para crear nuevo documento
        ttk.Button(
            self.bienvenida_frame,
            text="Crear Nuevo Documento",
            style="Primary.TButton",
            command=self.iniciar_nuevo_documento,
            padding=(20, 10)
        ).pack()
    
    def cargar_documentos(self):
        """Carga la lista de documentos desde la base de datos."""
        # Limpiar la lista
        for item in self.lista.get_children():
            self.lista.delete(item)
        
        # Obtener todos los documentos
        documentos = self.documento_service.obtener_todos()
        
        # Insertar en la lista
        for doc in documentos:
            fecha_str = doc.fecha_creacion.strftime("%d/%m/%Y")
            self.lista.insert("", tk.END, values=(
                doc.id,
                fecha_str,
                doc.cliente_nombre,
                doc.tipo_transaccion
            ))
    
    def filtrar_documentos(self, *args):
        """Filtra la lista de documentos según el texto de búsqueda."""
        # Texto de búsqueda
        filtro = self.filtro_var.get().lower()
        
        # Limpiar la lista
        for item in self.lista.get_children():
            self.lista.delete(item)
        
        # Obtener todos los documentos
        documentos = self.documento_service.obtener_todos()
        
        # Filtrar e insertar en la lista
        for doc in documentos:
            # Comprobar si el filtro coincide con algún campo
            if (filtro in str(doc.id).lower() or 
                filtro in doc.cliente_nombre.lower() or 
                filtro in doc.cliente_id.lower() or 
                filtro in doc.tipo_transaccion.lower()):
                
                fecha_str = doc.fecha_creacion.strftime("%d/%m/%Y")
                self.lista.insert("", tk.END, values=(
                    doc.id,
                    fecha_str,
                    doc.cliente_nombre,
                    doc.tipo_transaccion
                ))
    
    def seleccionar_documento(self, event):
        """Evento al seleccionar un documento de la lista."""
        # Obtener el ítem seleccionado
        seleccion = self.lista.selection()
        if not seleccion:
            return
        
        # Obtener el ID del documento
        item = self.lista.item(seleccion[0])
        doc_id = item["values"][0]
        
        # Habilitar el botón de eliminar
        self.eliminar_btn.config(state=tk.NORMAL)
        
        # Cargar el documento
        self.cargar_documento(doc_id)
    
    def cargar_documento(self, doc_id):
        """
        Carga un documento para visualizarlo o editarlo.
        
        Args:
            doc_id: ID del documento a cargar
        """
        # Obtener el documento
        documento = self.documento_service.obtener_por_id(doc_id)
        if not documento:
            messagebox.showerror("Error", f"No se encontró el documento con ID {doc_id}")
            return
        
        # Limpiar el panel de contenido
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para mostrar el documento
        frame = ttk.Frame(self.contenido_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Encabezado
        ttk.Label(
            frame,
            text=f"{documento.tipo_transaccion} - {documento.cliente_nombre}",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))
        
        # Información del documento
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(info_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"{documento.cliente_id} - {documento.cliente_nombre}").grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Dirección
        ttk.Label(info_frame, text="Dirección:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=documento.cliente_direccion or "-").grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Ancho de banda
        ttk.Label(info_frame, text="Ancho de banda:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=documento.ancho_banda).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Tipo
        ttk.Label(info_frame, text="Tipo:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=f"{documento.tipo_transaccion} - {documento.tipo_topologia}").grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Fecha
        ttk.Label(info_frame, text="Fecha:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=documento.fecha_creacion.strftime("%d/%m/%Y %H:%M")).grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Ingeniero
        ttk.Label(info_frame, text="Ingeniero:").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text=documento.ingeniero).grid(row=5, column=1, sticky=tk.W, pady=2)
        
        # Nodo IPRAN
        if documento.nodo_id:
            nodo = self.nodo_service.obtener_por_id(documento.nodo_id)
            if nodo:
                ttk.Label(info_frame, text="Nodo IPRAN:").grid(row=6, column=0, sticky=tk.W, pady=2)
                ttk.Label(info_frame, text=f"{nodo.alias_nodo} - {nodo.nombre_nodo}").grid(row=6, column=1, sticky=tk.W, pady=2)
        
        # Botones de acción
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Exportar a Word",
            style="Primary.TButton",
            command=lambda: self.exportar_documento(documento.id)
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Generar Correo",
            style="Secondary.TButton",
            command=lambda: self.mostrar_correo(documento)
        ).pack(side=tk.RIGHT, padx=5)
    
    def iniciar_nuevo_documento(self):
        """Inicia el asistente para crear un nuevo documento."""
        # Reiniciar los datos del documento
        self.documento_actual = {
            "titulo": "",
            "cliente_id": "",
            "cliente_nombre": "",
            "cliente_direccion": "",
            "ancho_banda": "",
            "tipo_transaccion": "UPGRADE",  # Valor predeterminado
            "tipo_topologia": "IPRAN+MIKROTIK",  # Valor predeterminado
            "ingeniero": "",
            "nodo_id": None,
            "mikrotik_ip": "",
            "contenido": {
                "ip_switch": "",
                "puerto": "",
                "vlan": "",
                "ip_publica": "",
                "mikrotik_export": "",
                "link_solarwinds": "",
                "observaciones": [],
                "correo": "",
                "imagenes": {}  # Diccionario para almacenar imágenes
            }
        }
        
        # Reiniciar el paso actual
        self.paso_actual = 0
        
        # Mostrar el primer paso
        self.mostrar_paso_asistente()
    
    def mostrar_paso_asistente(self):
        """Muestra el paso actual del asistente para crear un documento."""
        # Limpiar el panel de contenido
        for widget in self.contenido_frame.winfo_children():
            widget.destroy()
        
        # Crear frame para el paso actual
        frame = ttk.Frame(self.contenido_frame, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título del paso
        titulos_pasos = [
            "Información del Cliente",  # Paso 0
            "Configuración de la Topología",  # Paso 1
            "Configuración del Nodo IPRAN",  # Paso 2
            "Configuración de Mikrotik",  # Paso 3
            "Gráficas de Consumo",  # Paso 4
            "Notas y Observaciones",  # Paso 5
            "Correo de Notificación",  # Paso 6
            "Resumen del Documento"  # Paso 7
        ]
        
        ttk.Label(
            frame,
            text=f"Paso {self.paso_actual + 1}/{len(titulos_pasos)}: {titulos_pasos[self.paso_actual]}",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Contenido específico del paso
        if self.paso_actual == 0:
            # Información del Cliente
            self.mostrar_paso_info_cliente(frame)
        elif self.paso_actual == 1:
            # Configuración de la Topología
            self.mostrar_paso_topologia(frame)
        elif self.paso_actual == 2:
            # Configuración del Nodo IPRAN
            self.mostrar_paso_nodo_ipran(frame)
        elif self.paso_actual == 3:
            # Configuración de Mikrotik
            self.mostrar_paso_mikrotik(frame)
        elif self.paso_actual == 4:
            # Gráficas de Consumo
            self.mostrar_paso_graficas(frame)
        elif self.paso_actual == 5:
            # Notas y Observaciones
            self.mostrar_paso_observaciones(frame)
        elif self.paso_actual == 6:
            # Correo de Notificación
            self.mostrar_paso_correo(frame)
        elif self.paso_actual == 7:
            # Resumen del Documento
            self.mostrar_paso_resumen(frame)
        
        # Botones de navegación
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón Anterior
        ttk.Button(
            btn_frame,
            text="Anterior",
            command=self.paso_anterior,
            state=tk.NORMAL if self.paso_actual > 0 else tk.DISABLED
        ).pack(side=tk.LEFT)
        
        # Botón Siguiente o Finalizar
        if self.paso_actual < 7:
            ttk.Button(
                btn_frame,
                text="Siguiente",
                style="Primary.TButton",
                command=self.paso_siguiente
            ).pack(side=tk.RIGHT)
        else:
            ttk.Button(
                btn_frame,
                text="Guardar Documento",
                style="Success.TButton",
                command=self.guardar_documento
            ).pack(side=tk.RIGHT)
    
    def mostrar_paso_info_cliente(self, parent):
        """
        Muestra el paso de información del cliente.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # ID Cliente
        ttk.Label(campos_frame, text="ID Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        id_entry = ttk.Entry(campos_frame, width=20)
        id_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        id_entry.insert(0, self.documento_actual["cliente_id"])
        
        # Nombre Cliente
        ttk.Label(campos_frame, text="Nombre Cliente:").grid(row=1, column=0, sticky=tk.W, pady=5)
        nombre_entry = ttk.Entry(campos_frame, width=40)
        nombre_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        nombre_entry.insert(0, self.documento_actual["cliente_nombre"])
        
        # Dirección Cliente
        ttk.Label(campos_frame, text="Dirección:").grid(row=2, column=0, sticky=tk.W, pady=5)
        direccion_entry = ttk.Entry(campos_frame, width=40)
        direccion_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        direccion_entry.insert(0, self.documento_actual["cliente_direccion"])
        
        # Ancho de Banda
        ttk.Label(campos_frame, text="Ancho de Banda:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ancho_frame = ttk.Frame(campos_frame)
        ancho_frame.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        ancho_entry = ttk.Entry(ancho_frame, width=10)
        ancho_entry.pack(side=tk.LEFT)
        if self.documento_actual["ancho_banda"]:
            # Extraer el valor numérico del ancho de banda
            try:
                valor = self.documento_actual["ancho_banda"].split()[0]
                ancho_entry.insert(0, valor)
            except:
                pass
        
        ttk.Label(ancho_frame, text="Mbps").pack(side=tk.LEFT, padx=5)
        
        # Tipo de Transacción
        ttk.Label(campos_frame, text="Tipo de Transacción:").grid(row=4, column=0, sticky=tk.W, pady=5)
        tipo_var = tk.StringVar(value=self.documento_actual["tipo_transaccion"])
        tipo_frame = ttk.Frame(campos_frame)
        tipo_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Radiobutton(
            tipo_frame, text="UPGRADE", variable=tipo_var, value="UPGRADE"
        ).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            tipo_frame, text="DOWNGRADE", variable=tipo_var, value="DOWNGRADE"
        ).pack(side=tk.LEFT)
        
        # Ingeniero
        ttk.Label(campos_frame, text="Ingeniero:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ingeniero_entry = ttk.Entry(campos_frame, width=30)
        ingeniero_entry.grid(row=5, column=1, sticky=tk.W, pady=5, padx=5)
        ingeniero_entry.insert(0, self.documento_actual["ingeniero"])
        
        # Etiqueta Cliente (generada automáticamente)
        ttk.Label(campos_frame, text="Etiqueta Generada:").grid(row=6, column=0, sticky=tk.W, pady=5)
        etiqueta_lbl = ttk.Label(campos_frame, text="", font=("Consolas", 10))
        etiqueta_lbl.grid(row=6, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Función para actualizar la etiqueta
        def actualizar_etiqueta(*args):
            id_cliente = id_entry.get().strip()
            nombre_cliente = nombre_entry.get().strip()
            ancho = ancho_entry.get().strip() + " Mbps"
            
            if id_cliente and nombre_cliente and ancho:
                etiqueta = self.documento_service.generar_etiqueta_cliente(id_cliente, nombre_cliente, ancho)
                etiqueta_lbl.config(text=etiqueta)
            else:
                etiqueta_lbl.config(text="")
        
        # Vincular eventos de cambio
        id_entry.bind("<KeyRelease>", actualizar_etiqueta)
        nombre_entry.bind("<KeyRelease>", actualizar_etiqueta)
        ancho_entry.bind("<KeyRelease>", actualizar_etiqueta)
        
        # Actualizar etiqueta al cargar
        actualizar_etiqueta()
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Validar campos obligatorios
            if not id_entry.get().strip():
                messagebox.showerror("Error", "El ID del cliente es obligatorio")
                return False
            
            if not nombre_entry.get().strip():
                messagebox.showerror("Error", "El nombre del cliente es obligatorio")
                return False
            
            if not ancho_entry.get().strip():
                messagebox.showerror("Error", "El ancho de banda es obligatorio")
                return False
            
            # Guardar datos en el documento actual
            self.documento_actual["cliente_id"] = id_entry.get().strip()
            self.documento_actual["cliente_nombre"] = nombre_entry.get().strip()
            self.documento_actual["cliente_direccion"] = direccion_entry.get().strip()
            self.documento_actual["ancho_banda"] = ancho_entry.get().strip() + " Mbps"
            self.documento_actual["tipo_transaccion"] = tipo_var.get()
            self.documento_actual["ingeniero"] = ingeniero_entry.get().strip()
            
            # Generar el título automáticamente
            self.documento_actual["titulo"] = f"{tipo_var.get()} de Enlace - {nombre_entry.get().strip()}"
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def mostrar_paso_topologia(self, parent):
        """
        Muestra el paso de configuración de topología.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Tipo de Topología
        ttk.Label(campos_frame, text="Tipo de Topología:").grid(row=0, column=0, sticky=tk.W, pady=10)
        
        # Variable para almacenar la topología seleccionada
        topologia_var = tk.StringVar(value=self.documento_actual["tipo_topologia"])
        
        # Opciones de topología
        opciones_frame = ttk.Frame(campos_frame)
        opciones_frame.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ttk.Radiobutton(
            opciones_frame, text="IPRAN + MIKROTIK", variable=topologia_var, value="IPRAN+MIKROTIK"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            opciones_frame, text="IPRAN + RADWIN", variable=topologia_var, value="IPRAN+RADWIN"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            opciones_frame, text="IPRAN + GPON", variable=topologia_var, value="IPRAN+GPON"
        ).pack(anchor=tk.W, pady=2)
        
        ttk.Radiobutton(
            opciones_frame, text="FIBERTEC", variable=topologia_var, value="FIBERTEC"
        ).pack(anchor=tk.W, pady=2)
        
        # Explicación de la topología seleccionada
        ttk.Label(campos_frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, pady=10)
        
        descripcion_label = ttk.Label(
            campos_frame, 
            text="", 
            wraplength=400, 
            justify=tk.LEFT
        )
        descripcion_label.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        # Función para actualizar la descripción según la topología seleccionada
        def actualizar_descripcion(*args):
            topo = topologia_var.get()
            if topo == "IPRAN+MIKROTIK":
                desc = "Esta topología utiliza un nodo IPRAN para la conexión a la red principal y un Mikrotik para la entrega del servicio al cliente."
            elif topo == "IPRAN+RADWIN":
                desc = "Esta topología utiliza un nodo IPRAN para la conexión a la red principal y un Radwin para la entrega inalámbrica del servicio."
            elif topo == "IPRAN+GPON":
                desc = "Esta topología utiliza un nodo IPRAN para la conexión a la red principal y una OLT GPON para la entrega del servicio por fibra óptica."
            else:  # FIBERTEC
                desc = "Esta topología utiliza la red de fibra de Fibertec para la entrega del servicio al cliente."
            
            descripcion_label.config(text=desc)
        
        # Vincular cambio de topología con actualización de descripción
        topologia_var.trace("w", actualizar_descripcion)
        
        # Actualizar al cargar
        actualizar_descripcion()
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Guardar datos en el documento actual
            self.documento_actual["tipo_topologia"] = topologia_var.get()
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
# src/presentation/views/documento_view.py (continuación)
    def mostrar_paso_nodo_ipran(self, parent):
        """
        Muestra el paso de configuración del nodo IPRAN.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Solo para topologías que incluyen IPRAN
        if not self.documento_actual["tipo_topologia"].startswith("IPRAN"):
            ttk.Label(
                parent,
                text="La topología seleccionada no requiere configuración de nodo IPRAN.",
                font=("Arial", 11),
                wraplength=400
            ).pack(pady=20)
            
            # Función para guardar los datos de este paso
            def guardar_paso():
                return True
            
            # Vincular la función de guardar al paso
            self.guardar_paso_actual = guardar_paso
            return
        
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Buscar nodo
        ttk.Label(campos_frame, text="Buscar Nodo:").grid(row=0, column=0, sticky=tk.W, pady=10)
        
        # Frame para búsqueda
        busqueda_frame = ttk.Frame(campos_frame)
        busqueda_frame.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        # Entrada para búsqueda
        busqueda_entry = ttk.Entry(busqueda_frame, width=15)
        busqueda_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Botón de búsqueda
        buscar_btn = ttk.Button(
            busqueda_frame,
            text="Buscar",
            command=lambda: buscar_nodo(busqueda_entry.get().strip())
        )
        buscar_btn.pack(side=tk.LEFT)
        
        # Frame para mostrar resultados
        resultados_frame = ttk.Frame(parent)
        resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Lista de resultados
        resultados_tree = ttk.Treeview(
            resultados_frame,
            columns=("id", "alias", "nombre", "ip"),
            show="headings",
            height=5
        )
        
        # Configurar columnas
        resultados_tree.column("id", width=50, anchor=tk.CENTER)
        resultados_tree.column("alias", width=100)
        resultados_tree.column("nombre", width=200)
        resultados_tree.column("ip", width=100)
        
        # Configurar encabezados
        resultados_tree.heading("id", text="ID")
        resultados_tree.heading("alias", text="Alias")
        resultados_tree.heading("nombre", text="Nombre")
        resultados_tree.heading("ip", text="IP")
        
        resultados_tree.pack(fill=tk.BOTH, expand=True)
        
        # Frame para información del nodo seleccionado
        info_nodo_frame = ttk.LabelFrame(parent, text="Información del Nodo Seleccionado")
        info_nodo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Etiquetas para información del nodo
        nodo_id_lbl = ttk.Label(info_nodo_frame, text="ID: -")
        nodo_id_lbl.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        nodo_alias_lbl = ttk.Label(info_nodo_frame, text="Alias: -")
        nodo_alias_lbl.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        nodo_nombre_lbl = ttk.Label(info_nodo_frame, text="Nombre: -")
        nodo_nombre_lbl.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        
        nodo_ip_lbl = ttk.Label(info_nodo_frame, text="IP: -")
        nodo_ip_lbl.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Campos adicionales para la configuración del nodo
        config_frame = ttk.LabelFrame(parent, text="Configuración Adicional")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(config_frame, text="IP Switch:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        ip_switch_entry = ttk.Entry(config_frame, width=20)
        ip_switch_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        ip_switch_entry.insert(0, self.documento_actual["contenido"].get("ip_switch", ""))
        
        ttk.Label(config_frame, text="Puerto:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        puerto_entry = ttk.Entry(config_frame, width=20)
        puerto_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        puerto_entry.insert(0, self.documento_actual["contenido"].get("puerto", ""))
        
        ttk.Label(config_frame, text="VLAN:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        vlan_entry = ttk.Entry(config_frame, width=20)
        vlan_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        vlan_entry.insert(0, self.documento_actual["contenido"].get("vlan", ""))
        
        ttk.Label(config_frame, text="IP Pública:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        ip_publica_entry = ttk.Entry(config_frame, width=20)
        ip_publica_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        ip_publica_entry.insert(0, self.documento_actual["contenido"].get("ip_publica", ""))
        
        # Variable para almacenar el nodo seleccionado
        nodo_seleccionado = {"id": None}
        
        # Función para buscar nodo
        def buscar_nodo(texto):
            # Limpiar resultados anteriores
            for item in resultados_tree.get_children():
                resultados_tree.delete(item)
            
            if not texto:
                return
            
            # Buscar nodos que coincidan con el texto
            nodos = self.nodo_service.buscar_por_nombre(texto)
            
            # Mostrar resultados
            for nodo in nodos:
                resultados_tree.insert("", tk.END, values=(
                    nodo.id,
                    nodo.alias_nodo,
                    nodo.nombre_nodo,
                    nodo.ip_nodo
                ))
        
        # Evento al seleccionar un nodo
        def seleccionar_nodo(event):
            seleccion = resultados_tree.selection()
            if not seleccion:
                return
            
            # Obtener datos del nodo seleccionado
            item = resultados_tree.item(seleccion[0])
            nodo_id = item["values"][0]
            
            # Buscar el nodo completo
            nodo = self.nodo_service.obtener_por_id(nodo_id)
            if not nodo:
                return
            
            # Actualizar información mostrada
            nodo_id_lbl.config(text=f"ID: {nodo.id}")
            nodo_alias_lbl.config(text=f"Alias: {nodo.alias_nodo}")
            nodo_nombre_lbl.config(text=f"Nombre: {nodo.nombre_nodo}")
            nodo_ip_lbl.config(text=f"IP: {nodo.ip_nodo}")
            
            # Guardar el nodo seleccionado
            nodo_seleccionado["id"] = nodo.id
        
        # Vincular evento
        resultados_tree.bind("<<TreeviewSelect>>", seleccionar_nodo)
        
        # Si ya hay un nodo seleccionado, mostrarlo
        if self.documento_actual["nodo_id"]:
            nodo = self.nodo_service.obtener_por_id(self.documento_actual["nodo_id"])
            if nodo:
                nodo_id_lbl.config(text=f"ID: {nodo.id}")
                nodo_alias_lbl.config(text=f"Alias: {nodo.alias_nodo}")
                nodo_nombre_lbl.config(text=f"Nombre: {nodo.nombre_nodo}")
                nodo_ip_lbl.config(text=f"IP: {nodo.ip_nodo}")
                nodo_seleccionado["id"] = nodo.id
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Validar que se haya seleccionado un nodo si es una topología IPRAN
            if self.documento_actual["tipo_topologia"].startswith("IPRAN") and not nodo_seleccionado["id"]:
                messagebox.showerror("Error", "Debe seleccionar un nodo IPRAN")
                return False
            
            # Guardar datos en el documento actual
            self.documento_actual["nodo_id"] = nodo_seleccionado["id"]
            self.documento_actual["contenido"]["ip_switch"] = ip_switch_entry.get().strip()
            self.documento_actual["contenido"]["puerto"] = puerto_entry.get().strip()
            self.documento_actual["contenido"]["vlan"] = vlan_entry.get().strip()
            self.documento_actual["contenido"]["ip_publica"] = ip_publica_entry.get().strip()
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def mostrar_paso_mikrotik(self, parent):
        """
        Muestra el paso de configuración de Mikrotik.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Solo para topología IPRAN+MIKROTIK
        if self.documento_actual["tipo_topologia"] != "IPRAN+MIKROTIK":
            ttk.Label(
                parent,
                text="La topología seleccionada no requiere configuración de Mikrotik.",
                font=("Arial", 11),
                wraplength=400
            ).pack(pady=20)
            
            # Función para guardar los datos de este paso
            def guardar_paso():
                return True
            
            # Vincular la función de guardar al paso
            self.guardar_paso_actual = guardar_paso
            return
        
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # IP del Mikrotik
        ttk.Label(campos_frame, text="IP del Mikrotik:").grid(row=0, column=0, sticky=tk.W, pady=10)
        
        # Frame para IP y ping
        ip_frame = ttk.Frame(campos_frame)
        ip_frame.grid(row=0, column=1, sticky=tk.W, pady=10)
        
        ip_entry = ttk.Entry(ip_frame, width=20)
        ip_entry.pack(side=tk.LEFT, padx=(0, 5))
        ip_entry.insert(0, self.documento_actual["mikrotik_ip"])
        
        ping_btn = ttk.Button(
            ip_frame,
            text="Probar Ping",
            command=lambda: self.probar_ping(ip_entry.get().strip())
        )
        ping_btn.pack(side=tk.LEFT)
        
        # Frame para export de configuración
        export_frame = ttk.LabelFrame(parent, text="Export de Configuración")
        export_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de texto para el export
        export_text = tk.Text(export_frame, height=10, width=60, font=("Consolas", 9))
        export_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Insertar export actual si existe
        if "mikrotik_export" in self.documento_actual["contenido"]:
            export_text.insert(tk.END, self.documento_actual["contenido"]["mikrotik_export"])
        
        # Botones para export
        btn_frame = ttk.Frame(export_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Limpiar",
            command=lambda: export_text.delete(1.0, tk.END)
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Pegar Portapapeles",
            command=lambda: export_text.insert(tk.END, self.root.clipboard_get())
        ).pack(side=tk.LEFT, padx=5)
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Validar IP
            ip = ip_entry.get().strip()
            if self.documento_actual["tipo_topologia"] == "IPRAN+MIKROTIK" and not ip:
                messagebox.showerror("Error", "Debe ingresar la IP del Mikrotik")
                return False
            
            # Guardar datos en el documento actual
            self.documento_actual["mikrotik_ip"] = ip
            self.documento_actual["contenido"]["mikrotik_export"] = export_text.get(1.0, tk.END).strip()
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def mostrar_paso_graficas(self, parent):
        """
        Muestra el paso para agregar gráficas de consumo.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Enlace a Solarwinds
        ttk.Label(campos_frame, text="Enlace a Solarwinds:").grid(row=0, column=0, sticky=tk.W, pady=10)
        
        link_entry = ttk.Entry(campos_frame, width=60)
        link_entry.grid(row=0, column=1, sticky=tk.W, pady=10)
        link_entry.insert(0, self.documento_actual["contenido"].get("link_solarwinds", ""))
        
        # Frame para la gráfica
        grafica_frame = ttk.LabelFrame(parent, text="Gráfica de Consumo")
        grafica_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Etiqueta para mostrar instrucciones
        instrucciones = "Para agregar una gráfica de consumo, tome una captura de pantalla y luego presione 'Pegar' para insertarla aquí."
        ttk.Label(grafica_frame, text=instrucciones, wraplength=400).pack(pady=10)
        
        # Frame para la imagen
        imagen_frame = ttk.Frame(grafica_frame)
        imagen_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Variable para almacenar la imagen
        imagen_var = {"imagen": None, "mostrada": None}
        
        # Etiqueta para mostrar la imagen
        imagen_lbl = ttk.Label(imagen_frame)
        imagen_lbl.pack(fill=tk.BOTH, expand=True)
        
        # Botones para la imagen
        btn_frame = ttk.Frame(grafica_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Pegar",
            command=lambda: pegar_imagen()
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Limpiar",
            command=lambda: limpiar_imagen()
        ).pack(side=tk.LEFT, padx=5)
        
        # Función para pegar imagen desde el portapapeles
        def pegar_imagen():
            try:
                # Intentar obtener imagen del portapapeles
                imagen = self.obtener_imagen_portapapeles()
                if imagen:
                    # Guardar la imagen
                    imagen_var["imagen"] = imagen
                    
                    # Mostrar la imagen (redimensionada)
                    ancho_max = 400
                    alto_max = 300
                    
                    ancho, alto = imagen.size
                    if ancho > ancho_max:
                        ratio = ancho_max / ancho
                        ancho = ancho_max
                        alto = int(alto * ratio)
                    
                    if alto > alto_max:
                        ratio = alto_max / alto
                        alto = alto_max
                        ancho = int(ancho * ratio)
                    
                    imagen_redimensionada = imagen.resize((ancho, alto), Image.LANCZOS)
                    tk_imagen = ImageTk.PhotoImage(imagen_redimensionada)
                    
                    # Guardar referencia para evitar que el recolector de basura la elimine
                    imagen_var["mostrada"] = tk_imagen
                    
                    # Mostrar en la etiqueta
                    imagen_lbl.config(image=tk_imagen)
                else:
                    messagebox.showwarning("Advertencia", "No hay una imagen en el portapapeles.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo pegar la imagen: {str(e)}")
        
        # Función para limpiar la imagen
        def limpiar_imagen():
            imagen_var["imagen"] = None
            imagen_var["mostrada"] = None
            imagen_lbl.config(image="")
        
        # Mostrar imagen existente si hay
        if "grafica_consumo" in self.documento_actual["contenido"]:
            try:
                bytes_imagen = self.documento_actual["contenido"]["grafica_consumo"]
                if bytes_imagen:
                    from io import BytesIO
                    stream = BytesIO(bytes_imagen)
                    imagen = Image.open(stream)
                    
                    # Guardar la imagen
                    imagen_var["imagen"] = imagen
                    
                    # Mostrar la imagen (redimensionada)
                    ancho_max = 400
                    alto_max = 300
                    
                    ancho, alto = imagen.size
                    if ancho > ancho_max:
                        ratio = ancho_max / ancho
                        ancho = ancho_max
                        alto = int(alto * ratio)
                    
                    if alto > alto_max:
                        ratio = alto_max / alto
                        alto = alto_max
                        ancho = int(ancho * ratio)
                    
                    imagen_redimensionada = imagen.resize((ancho, alto), Image.LANCZOS)
                    tk_imagen = ImageTk.PhotoImage(imagen_redimensionada)
                    
                    # Guardar referencia para evitar que el recolector de basura la elimine
                    imagen_var["mostrada"] = tk_imagen
                    
                    # Mostrar en la etiqueta
                    imagen_lbl.config(image=tk_imagen)
            except:
                pass
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Guardar link
            self.documento_actual["contenido"]["link_solarwinds"] = link_entry.get().strip()
            
            # Guardar imagen si existe
            if imagen_var["imagen"]:
                # Convertir imagen a bytes
                from io import BytesIO
                buffer = BytesIO()
                imagen_var["imagen"].save(buffer, format="PNG")
                bytes_imagen = buffer.getvalue()
                
                # Guardar en el documento
                self.documento_actual["contenido"]["grafica_consumo"] = bytes_imagen
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def mostrar_paso_observaciones(self, parent):
        """
        Muestra el paso para agregar notas y observaciones.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Lista de observaciones
        ttk.Label(campos_frame, text="Notas/Observaciones:").pack(anchor=tk.W, pady=(0, 5))
        
        # Lista de observaciones actuales
        obs_frame = ttk.Frame(campos_frame)
        obs_frame.pack(fill=tk.X, pady=5)
        
        # Lista con scrollbar
        scroll = ttk.Scrollbar(obs_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Lista
        obs_listbox = tk.Listbox(obs_frame, height=5, width=60, font=("Arial", 10), yscrollcommand=scroll.set)
        obs_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll.config(command=obs_listbox.yview)
        
        # Insertar observaciones actuales
        if "observaciones" in self.documento_actual["contenido"]:
            for obs in self.documento_actual["contenido"]["observaciones"]:
                obs_listbox.insert(tk.END, obs)
        
        # Frame para agregar observación
        agregar_frame = ttk.Frame(campos_frame)
        agregar_frame.pack(fill=tk.X, pady=5)
        
        # Casillas de selección para observaciones comunes
        check_frame = ttk.LabelFrame(campos_frame, text="Observaciones Comunes")
        check_frame.pack(fill=tk.X, pady=10)
        
        # Variables para casillas
        upgrade_var = tk.BooleanVar(value=False)
        no_modificar_var = tk.BooleanVar(value=False)
        
        # Casillas
        ttk.Checkbutton(
            check_frame,
            text="SE APLICA UPGRADE A 5MBPS",
            variable=upgrade_var
        ).pack(anchor=tk.W, pady=2, padx=10)
        
        ttk.Checkbutton(
            check_frame,
            text="NO SE REALIZAN MODIFICACIONES EN IPRAN",
            variable=no_modificar_var
        ).pack(anchor=tk.W, pady=2, padx=10)
        
        # Entrada para nueva observación
        ttk.Label(agregar_frame, text="Nueva observación:").pack(side=tk.LEFT, padx=(0, 5))
        
        obs_entry = ttk.Entry(agregar_frame, width=40)
        obs_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
        
        # Botón para agregar
        ttk.Button(
            agregar_frame,
            text="Agregar",
            command=lambda: agregar_observacion()
        ).pack(side=tk.LEFT)
        
        # Frame para botones de acción
        btn_frame = ttk.Frame(campos_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botones para gestionar observaciones
        ttk.Button(
            btn_frame,
            text="Eliminar Seleccionada",
            command=lambda: eliminar_observacion()
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            btn_frame,
            text="Limpiar Todas",
            command=lambda: obs_listbox.delete(0, tk.END)
        ).pack(side=tk.LEFT)
        
        # Botón para agregar observaciones comunes
        ttk.Button(
            btn_frame,
            text="Agregar Observaciones Seleccionadas",
            command=lambda: agregar_observaciones_comunes()
        ).pack(side=tk.RIGHT)
        
        # Función para agregar observación
        def agregar_observacion():
            texto = obs_entry.get().strip()
            if texto:
                obs_listbox.insert(tk.END, texto)
                obs_entry.delete(0, tk.END)
        
        # Función para eliminar observación seleccionada
        def eliminar_observacion():
            seleccion = obs_listbox.curselection()
            if seleccion:
                obs_listbox.delete(seleccion[0])
        
        # Función para agregar observaciones comunes
        def agregar_observaciones_comunes():
            # Limpiar lista actual
            obs_listbox.delete(0, tk.END)
            
            # Agregar observaciones según casillas seleccionadas
            if upgrade_var.get():
                obs_listbox.insert(tk.END, "SE APLICA UPGRADE A 5MBPS")
            
            if no_modificar_var.get():
                obs_listbox.insert(tk.END, "NO SE REALIZAN MODIFICACIONES EN IPRAN")
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Obtener todas las observaciones de la lista
            observaciones = []
            for i in range(obs_listbox.size()):
                observaciones.append(obs_listbox.get(i))
            
            # Guardar en el documento
            self.documento_actual["contenido"]["observaciones"] = observaciones
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def mostrar_paso_correo(self, parent):
        """
        Muestra el paso para generar el correo de notificación.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Generar texto del correo basado en la información del documento
        correo = self.documento_service.generar_texto_correo(
            self.documento_actual["cliente_id"],
            self.documento_actual["cliente_nombre"],
            self.documento_actual["cliente_direccion"],
            self.documento_actual["ancho_banda"],
            self.documento_actual["tipo_transaccion"]
        )
        
        # Mostrar el asunto
        ttk.Label(campos_frame, text="Asunto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        asunto_entry = ttk.Entry(campos_frame, width=60)
        asunto_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        asunto_entry.insert(0, correo["asunto"])
        
        # Botón para copiar el asunto
        ttk.Button(
            campos_frame,
            text="Copiar",
            command=lambda: self.copiar_al_portapapeles(asunto_entry.get())
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Mostrar el cuerpo del correo
        ttk.Label(campos_frame, text="Cuerpo del Correo:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        
        # Área de texto para el cuerpo del correo
        cuerpo_text = tk.Text(campos_frame, height=10, width=60)
        cuerpo_text.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        cuerpo_text.insert(tk.END, correo["cuerpo"])
        
        # Botón para copiar el cuerpo
        ttk.Button(
            campos_frame,
            text="Copiar",
            command=lambda: self.copiar_al_portapapeles(cuerpo_text.get(1.0, tk.END))
        ).grid(row=1, column=2, padx=5, pady=5)
        
        # Botones adicionales
        btn_frame = ttk.Frame(campos_frame)
        btn_frame.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Regenerar Correo",
            command=lambda: regenerar_correo()
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            btn_frame,
            text="Copiar Todo",
            command=lambda: self.copiar_al_portapapeles(f"Asunto: {asunto_entry.get()}\n\n{cuerpo_text.get(1.0, tk.END)}")
        ).pack(side=tk.LEFT)
        
        # Función para regenerar el correo
        def regenerar_correo():
            correo = self.documento_service.generar_texto_correo(
                self.documento_actual["cliente_id"],
                self.documento_actual["cliente_nombre"],
                self.documento_actual["cliente_direccion"],
                self.documento_actual["ancho_banda"],
                self.documento_actual["tipo_transaccion"]
            )
            
            asunto_entry.delete(0, tk.END)
            asunto_entry.insert(0, correo["asunto"])
            
            cuerpo_text.delete(1.0, tk.END)
            cuerpo_text.insert(tk.END, correo["cuerpo"])
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # Guardar correo en el documento
            correo_completo = f"Asunto: {asunto_entry.get()}\n\n{cuerpo_text.get(1.0, tk.END)}"
            self.documento_actual["contenido"]["correo"] = correo_completo
            
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
# src/presentation/views/documento_view.py (continuación)
    def mostrar_paso_resumen(self, parent):
        """
        Muestra el paso de resumen del documento.
        
        Args:
            parent: Widget padre donde mostrar el contenido
        """
        # Frame para los campos
        campos_frame = ttk.Frame(parent)
        campos_frame.pack(fill=tk.X, pady=5)
        
        # Título
        ttk.Label(
            campos_frame,
            text="Resumen del Documento",
            font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Crear frame para mostrar el resumen
        resumen_frame = ttk.Frame(campos_frame)
        resumen_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cliente
        ttk.Label(resumen_frame, text="Cliente:", width=15, anchor=tk.W).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(resumen_frame, text=f"{self.documento_actual['cliente_id']} - {self.documento_actual['cliente_nombre']}").grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Dirección
        ttk.Label(resumen_frame, text="Dirección:", width=15, anchor=tk.W).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(resumen_frame, text=self.documento_actual['cliente_direccion'] or "-").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Tipo de transacción
        ttk.Label(resumen_frame, text="Transacción:", width=15, anchor=tk.W).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(resumen_frame, text=f"{self.documento_actual['tipo_transaccion']} a {self.documento_actual['ancho_banda']}").grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Topología
        ttk.Label(resumen_frame, text="Topología:", width=15, anchor=tk.W).grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(resumen_frame, text=self.documento_actual['tipo_topologia']).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Nodo IPRAN (si aplica)
        if self.documento_actual['nodo_id']:
            nodo = self.nodo_service.obtener_por_id(self.documento_actual['nodo_id'])
            if nodo:
                ttk.Label(resumen_frame, text="Nodo IPRAN:", width=15, anchor=tk.W).grid(row=4, column=0, sticky=tk.W, pady=5)
                ttk.Label(resumen_frame, text=f"{nodo.alias_nodo} - {nodo.nombre_nodo}").grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Mikrotik IP (si aplica)
        if self.documento_actual['mikrotik_ip']:
            ttk.Label(resumen_frame, text="Mikrotik IP:", width=15, anchor=tk.W).grid(row=5, column=0, sticky=tk.W, pady=5)
            ttk.Label(resumen_frame, text=self.documento_actual['mikrotik_ip']).grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Contenido adicional
        ttk.Label(resumen_frame, text="Contenido:", width=15, anchor=tk.W).grid(row=6, column=0, sticky=tk.NW, pady=5)
        
        contenido_text = "- "
        if "grafica_consumo" in self.documento_actual["contenido"] and self.documento_actual["contenido"]["grafica_consumo"]:
            contenido_text += "Gráfica de consumo\n- "
        if "mikrotik_export" in self.documento_actual["contenido"] and self.documento_actual["contenido"]["mikrotik_export"]:
            contenido_text += "Export de Mikrotik\n- "
        if "observaciones" in self.documento_actual["contenido"] and self.documento_actual["contenido"]["observaciones"]:
            contenido_text += f"{len(self.documento_actual['contenido']['observaciones'])} observaciones\n- "
        if "correo" in self.documento_actual["contenido"] and self.documento_actual["contenido"]["correo"]:
            contenido_text += "Correo de notificación\n- "
        
        contenido_text = contenido_text.strip("- ")
        if not contenido_text:
            contenido_text = "No hay contenido adicional."
        
        ttk.Label(
            resumen_frame, 
            text=contenido_text,
            justify=tk.LEFT,
            wraplength=400
        ).grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Ingeniero
        ttk.Label(resumen_frame, text="Ingeniero:", width=15, anchor=tk.W).grid(row=7, column=0, sticky=tk.W, pady=5)
        ttk.Label(resumen_frame, text=self.documento_actual['ingeniero']).grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # Función para guardar los datos de este paso
        def guardar_paso():
            # No hay datos adicionales que guardar en este paso
            return True
        
        # Vincular la función de guardar al paso
        self.guardar_paso_actual = guardar_paso
    
    def paso_siguiente(self):
        """Avanza al siguiente paso del asistente."""
        # Guardar datos del paso actual
        if hasattr(self, 'guardar_paso_actual'):
            if not self.guardar_paso_actual():
                return  # No avanzar si hay errores
        
        # Avanzar al siguiente paso
        self.paso_actual += 1
        
        # Mostrar el nuevo paso
        self.mostrar_paso_asistente()
    
    def paso_anterior(self):
        """Retrocede al paso anterior del asistente."""
        # Retroceder al paso anterior
        if self.paso_actual > 0:
            self.paso_actual -= 1
        
        # Mostrar el nuevo paso
        self.mostrar_paso_asistente()
    
    def guardar_documento(self):
        """Guarda el documento en la base de datos."""
        # Guardar datos del último paso
        if hasattr(self, 'guardar_paso_actual'):
            if not self.guardar_paso_actual():
                return  # No guardar si hay errores
        
        try:
            # Crear el documento en la base de datos
            documento = self.documento_service.crear(
                titulo=self.documento_actual["titulo"],
                cliente_id=self.documento_actual["cliente_id"],
                cliente_nombre=self.documento_actual["cliente_nombre"],
                cliente_direccion=self.documento_actual["cliente_direccion"],
                ancho_banda=self.documento_actual["ancho_banda"],
                tipo_transaccion=self.documento_actual["tipo_transaccion"],
                tipo_topologia=self.documento_actual["tipo_topologia"],
                ingeniero=self.documento_actual["ingeniero"],
                nodo_id=self.documento_actual["nodo_id"],
                mikrotik_ip=self.documento_actual["mikrotik_ip"],
                contenido_json=self.documento_actual["contenido"]
            )
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Documento guardado correctamente")
            
            # Exportar a Word automáticamente
            if messagebox.askyesno("Exportar", "¿Desea exportar el documento a Word?"):
                self.exportar_documento(documento.id)
            
            # Recargar la lista de documentos
            self.cargar_documentos()
            
            # Volver a la vista principal
            self.setup_panel_contenido()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el documento: {str(e)}")
    
    def eliminar_documento(self):
        """Elimina el documento seleccionado."""
        # Obtener el ítem seleccionado
        seleccion = self.lista.selection()
        if not seleccion:
            return
        
        # Obtener el ID del documento
        item = self.lista.item(seleccion[0])
        doc_id = item["values"][0]
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este documento?"):
            return
        
        try:
            # Eliminar el documento
            if self.documento_service.eliminar(doc_id):
                messagebox.showinfo("Éxito", "Documento eliminado correctamente")
                
                # Recargar la lista de documentos
                self.cargar_documentos()
                
                # Volver a la vista principal
                self.setup_panel_contenido()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el documento")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el documento: {str(e)}")
    
    def exportar_documento(self, documento_id):
        """
        Exporta un documento a formato Word.
        
        Args:
            documento_id: ID del documento a exportar
        """
        try:
            # Exportar el documento
            ruta = self.export_service.exportar_a_word(documento_id)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Documento exportado correctamente a:\n{ruta}")
            
            # Preguntar si desea abrir el documento
            if messagebox.askyesno("Abrir", "¿Desea abrir el documento exportado?"):
                # Abrir el documento con la aplicación predeterminada
                import os
                import subprocess
                import platform
                
                if platform.system() == "Windows":
                    os.startfile(ruta)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.call(["open", ruta])
                else:  # Linux
                    subprocess.call(["xdg-open", ruta])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar el documento: {str(e)}")
    
    def mostrar_correo(self, documento):
        """
        Muestra una ventana con el correo de notificación para copiarlo.
        
        Args:
            documento: Documento del que generar el correo
        """
        # Obtener el texto del correo
        correo = None
        try:
            # Si hay datos de correo guardados, usar esos
            if documento.contenido_json:
                contenido = json.loads(documento.contenido_json)
                if "correo" in contenido:
                    correo = contenido["correo"]
            
            # Si no hay datos guardados, generar el correo
            if not correo:
                correo_dict = self.documento_service.generar_texto_correo(
                    documento.cliente_id,
                    documento.cliente_nombre,
                    documento.cliente_direccion,
                    documento.ancho_banda,
                    documento.tipo_transaccion
                )
                correo = f"Asunto: {correo_dict['asunto']}\n\n{correo_dict['cuerpo']}"
        except:
            correo = "No se pudo generar el correo de notificación."
        
        # Crear ventana emergente
        ventana = tk.Toplevel(self)
        ventana.title("Correo de Notificación")
        ventana.geometry("500x400")
        ventana.resizable(True, True)
        
        # Frame principal
        frame = ttk.Frame(ventana, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            frame,
            text="Correo de Notificación",
            font=("Arial", 12, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Área de texto para el correo
        texto = tk.Text(frame, height=15, width=60)
        texto.pack(fill=tk.BOTH, expand=True, pady=5)
        texto.insert(tk.END, correo)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Copiar al Portapapeles",
            command=lambda: self.copiar_al_portapapeles(texto.get(1.0, tk.END))
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            btn_frame,
            text="Cerrar",
            command=ventana.destroy
        ).pack(side=tk.RIGHT)
    
    def probar_ping(self, ip):
        """
        Prueba si se puede hacer ping a una IP.
        
        Args:
            ip: Dirección IP a probar
        """
        if not ip:
            messagebox.showwarning("Advertencia", "Debe ingresar una IP válida")
            return
        
        # Ejecutar el comando ping
        import platform
        import subprocess
        
        try:
            # Crear comando según el sistema operativo
            if platform.system() == "Windows":
                comando = ["ping", "-n", "4", ip]
            else:  # Linux/Mac
                comando = ["ping", "-c", "4", ip]
            
            # Ejecutar el comando
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            # Analizar el resultado
            if "Tiempo de espera agotado" in resultado.stdout or "Request timed out" in resultado.stdout:
                messagebox.showerror("Error", f"No se puede hacer ping a {ip}\n\n{resultado.stdout}")
            elif "Destino inaccesible" in resultado.stdout or "Destination Host Unreachable" in resultado.stdout:
                messagebox.showerror("Error", f"Destino inaccesible: {ip}\n\n{resultado.stdout}")
            elif "0 recibidos" in resultado.stdout or "0 received" in resultado.stdout:
                messagebox.showerror("Error", f"No se recibió respuesta de {ip}\n\n{resultado.stdout}")
            else:
                messagebox.showinfo("Éxito", f"Ping exitoso a {ip}\n\n{resultado.stdout}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar ping: {str(e)}")
    
    def obtener_imagen_portapapeles(self):
        """
        Obtiene una imagen desde el portapapeles.
        
        Returns:
            PIL.Image: Imagen obtenida o None si no hay imagen
        """
        try:
            from PIL import ImageGrab, Image
            imagen = ImageGrab.grabclipboard()
            
            # Verificar si se obtuvo una imagen
            if isinstance(imagen, Image.Image):
                return imagen
            elif isinstance(imagen, list) and len(imagen) > 0 and os.path.isfile(imagen[0]):
                # Es una lista de rutas de archivo
                return Image.open(imagen[0])
            
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener imagen del portapapeles: {str(e)}")
            return None
    
    def copiar_al_portapapeles(self, texto):
        """
        Copia un texto al portapapeles.
        
        Args:
            texto: Texto a copiar
        """
        try:
            pyperclip.copy(texto)
            messagebox.showinfo("Información", "Texto copiado al portapapeles")
        except Exception as e:
            messagebox.showerror("Error", f"Error al copiar al portapapeles: {str(e)}")