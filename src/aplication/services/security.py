# src/application/services/security.py
"""
Servicios de seguridad para la aplicación.
Este módulo contiene funciones para manejar la seguridad de la aplicación.
"""
from passlib.context import CryptContext

# Creamos un contexto de encriptación que utiliza bcrypt para el hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_contraseña(contraseña_plana, contraseña_hash):
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        contraseña_plana: La contraseña en texto plano a verificar
        contraseña_hash: El hash de la contraseña almacenado
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(contraseña_plana, contraseña_hash)

def obtener_hash_contraseña(contraseña):
    """
    Obtiene el hash de una contraseña.
    
    Args:
        contraseña: La contraseña en texto plano
        
    Returns:
        str: El hash de la contraseña
    """
    return pwd_context.hash(contraseña)