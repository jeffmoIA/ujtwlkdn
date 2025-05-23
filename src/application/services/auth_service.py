# src/application/services/auth_service.py
"""
Servicio para la autenticación de usuarios.
"""
from typing import Optional

from domain.models.usuario import Usuario
from infrastructure.repositories.usuario_repository import UsuarioRepository
from application.services.security import verificar_contraseña, obtener_hash_contraseña

class AuthService:
    """Servicio para manejar la autenticación y autorización de usuarios."""
    
    def __init__(self):
        """Constructor del servicio."""
        self.usuario_repository = UsuarioRepository()
    
    def autenticar(self, username: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario con su nombre de usuario y contraseña.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            Optional[Usuario]: El usuario autenticado o None si la autenticación falla
        """
        # Buscar el usuario por su nombre de usuario
        usuario = self.usuario_repository.get_by_username(username)
        
        # Verificar si el usuario existe y si la contraseña es correcta
        if usuario and verificar_contraseña(password, usuario.contraseña):
            return usuario
        
        return None
    
    def registrar(self, username: str, password: str, nombre: str) -> Usuario:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            nombre: Nombre completo del usuario
            
        Returns:
            Usuario: El usuario registrado
            
        Raises:
            ValueError: Si el nombre de usuario ya existe
        """
        # Verificar si el usuario ya existe
        if self.usuario_repository.get_by_username(username):
            raise ValueError(f"El nombre de usuario '{username}' ya está en uso")
        
        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            usuario=username,
            contraseña=obtener_hash_contraseña(password),
            nombre=nombre
        )
        
        # Guardar el usuario en la base de datos
        return self.usuario_repository.create(nuevo_usuario)