# src/infrastructure/database/init_db.py
"""
Inicialización de la base de datos.
Este módulo se encarga de crear las tablas en la base de datos si no existen.
"""
from infrastructure.database.config import engine
from domain.models import BaseModel, NodoIPRAN, NodoGPON, Usuario, CorreoCliente

def init_db():
    """
    Función para inicializar la base de datos.
    Crea todas las tablas definidas en los modelos.
    """
    # Crear todas las tablas
    BaseModel.metadata.create_all(bind=engine)
    
    # Aquí podríamos añadir datos iniciales si fuera necesario
    # Por ejemplo, un usuario administrador predeterminado, etc.
    
    print("🗄️ Base de datos inicializada correctamente")

if __name__ == "__main__":
    # Si ejecutamos este archivo directamente, inicializamos la base de datos
    init_db()