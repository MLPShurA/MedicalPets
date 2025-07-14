import os
from typing import Dict, Any

class Settings:
    """Configuraciones generales de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME = "Medical Pets"
    APP_VERSION = "1.0.0"
    DEBUG = True
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "medical_pets_secret_key_2024")
    PASSWORD_SALT_ROUNDS = 12
    
    # Configuración de sesiones
    SESSION_TIMEOUT = 3600  # 1 hora en segundos
    
    # Configuración de roles
    ROLES = {
        'admin': 'Administrador',
        'veterinario': 'Veterinario', 
        'doctor': 'Doctor',
        'secretaria': 'Secretaria',
        'paciente': 'Paciente'
    }
    
    # Configuración de permisos por rol
    PERMISSIONS = {
        'admin': ['all'],
        'veterinario': ['usuarios', 'mascotas', 'citas', 'historial', 'tratamientos', 'prediccion'],
        'doctor': ['usuarios', 'mascotas', 'citas', 'historial', 'tratamientos', 'prediccion'],
        'secretaria': ['usuarios', 'mascotas', 'citas'],
        'paciente': ['mascotas', 'citas', 'historial', 'tratamientos']
    }
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Configuración de validaciones
    VALIDATION_RULES = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\+?[\d\s\-\(\)]{7,15}$',
        'cedula': r'^\d{10}$',
        'password_min_length': 6
    }
    
    # Configuración de archivos
    UPLOAD_FOLDER = "uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'}
    
    @classmethod
    def get_role_display_name(cls, role: str) -> str:
        """Obtiene el nombre de visualización de un rol"""
        return cls.ROLES.get(role, role.capitalize())
    
    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        """Verifica si un rol tiene un permiso específico"""
        if role not in cls.PERMISSIONS:
            return False
        return 'all' in cls.PERMISSIONS[role] or permission in cls.PERMISSIONS[role]
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Retorna todas las configuraciones como diccionario"""
        return {
            'app_name': cls.APP_NAME,
            'app_version': cls.APP_VERSION,
            'debug': cls.DEBUG,
            'roles': cls.ROLES,
            'permissions': cls.PERMISSIONS,
            'validation_rules': cls.VALIDATION_RULES
        }
