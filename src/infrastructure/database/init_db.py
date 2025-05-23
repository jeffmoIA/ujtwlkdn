# src/infrastructure/database/init_db.py
"""
Inicialización de la base de datos.
Este módulo se encarga de crear las tablas en la base de datos si no existen.
"""
from infrastructure.database.config import engine
from domain.models import BaseModel, NodoIPRAN, NodoGPON, Usuario, CorreoCliente, Documento, MikroTik  # ← NUEVO: Agregamos MikroTik

def init_db():
    """
    Función para inicializar la base de datos.
    Crea todas las tablas definidas en los modelos.
    """
    # Crear todas las tablas
    # Esto incluye automáticamente la nueva tabla 'mikrotiks'
    BaseModel.metadata.create_all(bind=engine)
    
    # Aquí podríamos añadir datos iniciales si fuera necesario
    # Por ejemplo, algunos MikroTiks de ejemplo
    
    print("🗄️ Base de datos inicializada correctamente")
    print("📋 Tablas creadas:")
    print("  ✅ usuarios")
    print("  ✅ nodos_ipran") 
    print("  ✅ nodos_gpon")
    print("  ✅ correo_cliente")
    print("  ✅ documentos")
    print("  ✅ mikrotiks")  # ← NUEVO: Confirmamos que se creó la tabla

if __name__ == "__main__":
    # Si ejecutamos este archivo directamente, inicializamos la base de datos
    init_db()