# src/presentation/utils/tk_styles.py
"""
Módulo para personalizar el estilo de la interfaz de usuario con Tkinter.
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

def aplicar_tema(root):
    """
    Aplica un tema personalizado a la aplicación Tkinter.
    
    Args:
        root: Ventana principal de la aplicación
    """
    # Crear un estilo personalizado
    style = ttk.Style()
    
    # Configurar el tema
    try:
        style.theme_use('clam')  # Usar un tema base más moderno
    except tk.TclError:
        pass  # El tema 'clam' puede no estar disponible en todas las plataformas
    
    # Colores principales
    PRIMARY_COLOR = "#3498db"  # Azul
    SECONDARY_COLOR = "#2c3e50"  # Azul oscuro
    BG_COLOR = "#f5f5f5"  # Gris claro
    FG_COLOR = "#333333"  # Gris oscuro
    ACCENT_COLOR = "#e74c3c"  # Rojo
    SUCCESS_COLOR = "#2ecc71"  # Verde
    
    # Fuentes
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    heading_font = tkfont.Font(family=default_font.cget("family"), size=12, weight="bold")
    
    # Configurar el estilo de los widgets
    style.configure(".", 
                    background=BG_COLOR, 
                    foreground=FG_COLOR, 
                    font=default_font)
    
    # Botones
    style.configure("TButton", 
                    background=PRIMARY_COLOR, 
                    foreground="white", 
                    padding=(10, 5), 
                    font=default_font)
    style.map("TButton",
              background=[("active", SECONDARY_COLOR), ("disabled", "#cccccc")],
              foreground=[("disabled", "#999999")])
    
    # Botón de acción principal
    style.configure("Primary.TButton", 
                    background=PRIMARY_COLOR, 
                    foreground="white",
                    padding=(10, 5),
                    font=default_font)
    
    # Botón de acción secundaria
    style.configure("Secondary.TButton", 
                    background=SECONDARY_COLOR, 
                    foreground="white",
                    padding=(10, 5),
                    font=default_font)
    
    # Botón de acción peligrosa (eliminar, etc.)
    style.configure("Danger.TButton", 
                    background=ACCENT_COLOR, 
                    foreground="white",
                    padding=(10, 5),
                    font=default_font)
    
    # Botón de acción exitosa (guardar, confirmar, etc.)
    style.configure("Success.TButton", 
                    background=SUCCESS_COLOR, 
                    foreground="white",
                    padding=(10, 5),
                    font=default_font)
    
   # Entradas de texto
    style.configure("TEntry", 
                    background="white", 
                    foreground=FG_COLOR,
                    fieldbackground="white",
                    padding=(5, 2))
    
    # Etiquetas
    style.configure("TLabel", 
                    background=BG_COLOR, 
                    foreground=FG_COLOR,
                    padding=(5, 2))
    
    # Frames
    style.configure("TFrame", 
                    background=BG_COLOR, 
                    borderwidth=0)
    
    # Frame con borde
    style.configure("Card.TFrame", 
                    background="white", 
                    borderwidth=1, 
                    relief="solid",
                    padding=10)
    
    # Comboboxes
    style.configure("TCombobox", 
                    background="white", 
                    fieldbackground="white",
                    foreground=FG_COLOR,
                    padding=(5, 2))
    
    # Pestañas (Notebook)
    style.configure("TNotebook", 
                    background=BG_COLOR, 
                    tabmargins=[2, 5, 2, 0])
    style.configure("TNotebook.Tab", 
                    background="#dfdfdf", 
                    foreground=FG_COLOR,
                    padding=[10, 4], 
                    font=default_font)
    style.map("TNotebook.Tab",
              background=[("selected", PRIMARY_COLOR)],
              foreground=[("selected", "white")])
    
    # Barras de desplazamiento
    style.configure("Vertical.TScrollbar", 
                    gripcount=0, 
                    background=BG_COLOR, 
                    troughcolor="#e1e1e1",
                    borderwidth=0,
                    arrowsize=14)
    style.map("Vertical.TScrollbar",
              background=[("pressed", SECONDARY_COLOR), ("active", PRIMARY_COLOR)])
    
    # Configuración para Treeview (tablas)
    style.configure("Treeview", 
                    background="white", 
                    foreground=FG_COLOR,
                    fieldbackground="white",
                    borderwidth=1,
                    rowheight=25)
    style.configure("Treeview.Heading", 
                    background=SECONDARY_COLOR, 
                    foreground="white",
                    font=heading_font)
    style.map("Treeview",
              background=[("selected", PRIMARY_COLOR)],
              foreground=[("selected", "white")])
    
    # Aplicar algunos estilos directamente a la ventana principal
    root.configure(background=BG_COLOR)
    
    return style  # Devolver el objeto style por si se necesita personalizar más cosas