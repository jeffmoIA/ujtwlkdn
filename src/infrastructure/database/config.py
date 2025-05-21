# src/infrastructure/database/config.py
"""
Configuración de la base de datos SQLAlchemy.
Este módulo establece la conexión con la base de datos y define la clase Base.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definimos la URL de conexión a la base de datos SQLite
# El archivo se guardará en la raíz del proyecto con el nombre 'network_app.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///network_app.db"

# Creamos el motor de SQLAlchemy
# El parámetro connect_args={"check_same_thread": False} es necesario solo para SQLite
# Permite que SQLite sea utilizado con hilos, lo cual es necesario para aplicaciones web
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creamos la clase SessionLocal que será nuestra fábrica de sesiones de base de datos
# Cada instancia de esta clase será una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos la clase Base que utilizarán nuestros modelos
# Todos los modelos serán creados como clases que heredan de esta clase Base
Base = declarative_base()

# Función para obtener una sesión de base de datos
def get_db():
    """
    Función para obtener una sesión de base de datos.
    Utiliza el patrón contextual para asegurar que la sesión se cierra después de usarla.
    """
    db = SessionLocal()
    try:
        yield db  # Devuelve la sesión para ser utilizada
    finally:
        db.close()  # Cierra la sesión cuando se termina de usar