import bcrypt
import hashlib
import secrets
import string
from typing import Optional

class SecurityUtils:
    """Utilidades de seguridad"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash de la contraseña usando bcrypt
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verifica una contraseña contra su hash
        
        Args:
            password: Contraseña en texto plano
            hashed: Hash de la contraseña
            
        Returns:
            True si la contraseña es correcta
        """
        try:
            # bcrypt hashes start with $2b$, $2a$, or $2y$
            if hashed.startswith("$2"):
                return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
            else:
                # Comparación directa si es una contraseña antigua
                return password == hashed
        except Exception:
            return False
    
    @staticmethod
    def generate_secure_password(length: int = 12) -> str:
        """
        Genera una contraseña segura aleatoria
        
        Args:
            length: Longitud de la contraseña
            
        Returns:
            Contraseña generada
        """
        # Caracteres permitidos
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        
        # Asegurar que tenga al menos una mayúscula, minúscula, número y símbolo
        password = [
            secrets.choice(string.ascii_lowercase),  # minúscula
            secrets.choice(string.ascii_uppercase),  # mayúscula
            secrets.choice(string.digits),           # número
            secrets.choice("!@#$%^&*")               # símbolo
        ]
        
        # Completar el resto de la contraseña
        password.extend(secrets.choice(characters) for _ in range(length - 4))
        
        # Mezclar la contraseña
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        return ''.join(password_list)
    
    @staticmethod
    def generate_api_key(length: int = 32) -> str:
        """
        Genera una clave API segura
        
        Args:
            length: Longitud de la clave
            
        Returns:
            Clave API generada
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_token(length: int = 64) -> str:
        """
        Genera un token seguro
        
        Args:
            length: Longitud del token
            
        Returns:
            Token generado
        """
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_string(text: str, algorithm: str = 'sha256') -> str:
        """
        Genera un hash de una cadena de texto
        
        Args:
            text: Texto a hashear
            algorithm: Algoritmo de hash (md5, sha1, sha256, sha512)
            
        Returns:
            Hash del texto
        """
        hash_func = getattr(hashlib, algorithm, hashlib.sha256)
        return hash_func(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitiza una entrada de texto para prevenir inyección
        
        Args:
            text: Texto a sanitizar
            
        Returns:
            Texto sanitizado
        """
        if not text:
            return ""
        
        # Remover caracteres peligrosos
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        sanitized = text
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        return sanitized.strip()
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
            
        Returns:
            Diccionario con el resultado de la validación
        """
        result = {
            'valid': True,
            'score': 0,
            'issues': []
        }
        
        if not password:
            result['valid'] = False
            result['issues'].append("La contraseña no puede estar vacía")
            return result
        
        # Verificar longitud mínima
        if len(password) < 8:
            result['issues'].append("La contraseña debe tener al menos 8 caracteres")
            result['score'] -= 2
        
        # Verificar longitud recomendada
        if len(password) >= 12:
            result['score'] += 2
        
        # Verificar si tiene mayúsculas
        if not any(c.isupper() for c in password):
            result['issues'].append("La contraseña debe contener al menos una mayúscula")
            result['score'] -= 1
        
        # Verificar si tiene minúsculas
        if not any(c.islower() for c in password):
            result['issues'].append("La contraseña debe contener al menos una minúscula")
            result['score'] -= 1
        
        # Verificar si tiene números
        if not any(c.isdigit() for c in password):
            result['issues'].append("La contraseña debe contener al menos un número")
            result['score'] -= 1
        
        # Verificar si tiene símbolos
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in symbols for c in password):
            result['issues'].append("La contraseña debe contener al menos un símbolo")
            result['score'] -= 1
        
        # Verificar si tiene caracteres repetidos
        if len(set(password)) < len(password) * 0.8:
            result['issues'].append("La contraseña no debe tener muchos caracteres repetidos")
            result['score'] -= 1
        
        # Determinar si es válida
        if result['score'] < 0 or len(result['issues']) > 3:
            result['valid'] = False
        
        return result
