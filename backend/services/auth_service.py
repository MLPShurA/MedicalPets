import bcrypt
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt

from ..config.database import DatabaseConfig
from ..config.settings import Settings
from ..models.usuario import Usuario
from ..utils.exceptions import AuthenticationError, ValidationError

logger = logging.getLogger(__name__)

class AuthService:
    """Servicio de autenticación y autorización"""
    
    def __init__(self):
        self.settings = Settings()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario con nombre de usuario y contraseña
        
        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            Usuario autenticado o None si falla la autenticación
            
        Raises:
            AuthenticationError: Si hay un error en la autenticación
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise AuthenticationError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            # Buscar usuario por nombre de usuario
            query = """
                SELECT u.*, ud.* 
                FROM usuarios u 
                LEFT JOIN usuarios_detalle ud ON u.id = ud.usuario_id 
                WHERE u.nombre_usuario = %s
            """
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not user_data:
                logger.warning(f"Intento de login fallido: usuario '{username}' no encontrado")
                return None
            
            # Verificar contraseña
            if not self._verify_password(password, user_data):
                logger.warning(f"Intento de login fallido: contraseña incorrecta para usuario '{username}'")
                return None
            
            # Crear objeto Usuario
            usuario = Usuario(
                id=user_data['id'],
                nombre_usuario=user_data['nombre_usuario'],
                rol=user_data['rol'],
                detalle_id=user_data.get('detalle_id'),
                nombres=user_data.get('nombres', ''),
                apellidos=user_data.get('apellidos', ''),
                cedula=user_data.get('cedula', ''),
                telefono=user_data.get('telefono', ''),
                correo_electronico=user_data.get('correo_electronico', ''),
                direccion=user_data.get('direccion', '')
            )
            
            logger.info(f"Usuario '{username}' autenticado exitosamente")
            return usuario
            
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            raise AuthenticationError(f"Error en autenticación: {str(e)}")
    
    def _verify_password(self, password: str, user_data: Dict[str, Any]) -> bool:
        """
        Verifica la contraseña del usuario
        
        Args:
            password: Contraseña en texto plano
            user_data: Datos del usuario de la base de datos
            
        Returns:
            True si la contraseña es correcta, False en caso contrario
        """
        try:
            # Verificar contraseña hasheada (nuevo sistema)
            if user_data.get('contrasena_hash'):
                return bcrypt.checkpw(
                    password.encode('utf-8'), 
                    user_data['contrasena_hash'].encode('utf-8')
                )
            
            # Verificar contraseña en texto plano (sistema antiguo)
            elif user_data.get('contrasena'):
                return password == user_data['contrasena']
            
            return False
            
        except Exception as e:
            logger.error(f"Error verificando contraseña: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """
        Genera un hash de la contraseña
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def generate_password(self, nombres: str, apellidos: str, cedula: str) -> str:
        """
        Genera una contraseña automática basada en los datos del usuario
        
        Args:
            nombres: Nombres del usuario
            apellidos: Apellidos del usuario
            cedula: Cédula del usuario
            
        Returns:
            Contraseña generada
        """
        parte_nombre = nombres[:3].lower()
        parte_apellido = apellidos[:3].lower()
        parte_cedula = cedula[-3:]
        return parte_nombre + parte_apellido + parte_cedula
    
    def validate_password(self, password: str) -> bool:
        """
        Valida que la contraseña cumpla con los requisitos mínimos
        
        Args:
            password: Contraseña a validar
            
        Returns:
            True si la contraseña es válida
        """
        if not password:
            return False
        
        min_length = self.settings.VALIDATION_RULES.get('password_min_length', 6)
        return len(password) >= min_length
    
    def has_permission(self, user: Usuario, permission: str) -> bool:
        """
        Verifica si un usuario tiene un permiso específico
        
        Args:
            user: Usuario a verificar
            permission: Permiso a verificar
            
        Returns:
            True si el usuario tiene el permiso
        """
        return self.settings.has_permission(user.rol, permission)
    
    def get_user_permissions(self, user: Usuario) -> list:
        """
        Obtiene todos los permisos de un usuario
        
        Args:
            user: Usuario del cual obtener los permisos
            
        Returns:
            Lista de permisos del usuario
        """
        return self.settings.PERMISSIONS.get(user.rol, [])
    
    def create_session_token(self, user: Usuario) -> str:
        """
        Crea un token de sesión para el usuario
        
        Args:
            user: Usuario para el cual crear el token
            
        Returns:
            Token JWT
        """
        payload = {
            'user_id': user.id,
            'username': user.nombre_usuario,
            'role': user.rol,
            'exp': datetime.utcnow() + timedelta(seconds=self.settings.SESSION_TIMEOUT)
        }
        
        return jwt.encode(payload, self.settings.SECRET_KEY, algorithm='HS256')
    
    def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica y decodifica un token de sesión
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Payload del token o None si es inválido
        """
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token de sesión expirado")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Token de sesión inválido")
            return None
