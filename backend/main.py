"""
Backend principal de Medical Pets
Sistema de gestión veterinaria con arquitectura modular
"""

import logging
import sys
from typing import Dict, Any
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('medical_pets.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Importar configuraciones y servicios
from config.database import DatabaseConfig
from config.settings import Settings
from services.auth_service import AuthService
from services.usuario_service import UsuarioService
from services.mascota_service import MascotaService
from services.cita_service import CitaService
from services.historial_service import HistorialService
from utils.exceptions import MedicalPetsException, DatabaseError, ValidationError

class MedicalPetsBackend:
    """Clase principal del backend de Medical Pets"""
    
    def __init__(self):
        """Inicializa el backend con todos los servicios"""
        self.settings = Settings()
        self.auth_service = AuthService()
        self.usuario_service = UsuarioService()
        self.mascota_service = MascotaService()
        self.cita_service = CitaService()
        self.historial_service = HistorialService()
        
        # Verificar conexión a la base de datos
        self._check_database_connection()
        
        logger.info("Backend de Medical Pets inicializado correctamente")
    
    def _check_database_connection(self) -> None:
        """Verifica la conexión a la base de datos"""
        try:
            if not DatabaseConfig.test_connection():
                raise DatabaseError("No se pudo conectar a la base de datos")
            logger.info("Conexión a la base de datos establecida correctamente")
        except Exception as e:
            logger.error(f"Error verificando conexión a la base de datos: {e}")
            raise DatabaseError(f"Error de conexión a la base de datos: {str(e)}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema"""
        return {
            'app_name': self.settings.APP_NAME,
            'version': self.settings.APP_VERSION,
            'debug': self.settings.DEBUG,
            'database_connected': DatabaseConfig.test_connection(),
            'timestamp': datetime.now().isoformat()
        }
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autentica un usuario
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Información del usuario autenticado
        """
        try:
            usuario = self.auth_service.authenticate_user(username, password)
            if not usuario:
                return {'success': False, 'message': 'Credenciales inválidas'}
            
            # Generar token de sesión
            token = self.auth_service.create_session_token(usuario)
            
            return {
                'success': True,
                'user': usuario.to_dict(),
                'token': token,
                'permissions': self.auth_service.get_user_permissions(usuario)
            }
        except Exception as e:
            logger.error(f"Error en autenticación: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_usuarios(self, user_id: int = None) -> Dict[str, Any]:
        """
        Obtiene usuarios del sistema
        
        Args:
            user_id: ID específico del usuario (opcional)
            
        Returns:
            Lista de usuarios o usuario específico
        """
        try:
            if user_id:
                usuario = self.usuario_service.get_usuario_by_id(user_id)
                if not usuario:
                    return {'success': False, 'message': 'Usuario no encontrado'}
                return {'success': True, 'usuario': usuario.to_dict()}
            else:
                usuarios = self.usuario_service.get_all_usuarios()
                return {'success': True, 'usuarios': [u.to_dict() for u in usuarios]}
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {e}")
            return {'success': False, 'message': str(e)}
    
    def create_usuario(self, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario
        
        Args:
            usuario_data: Datos del usuario
            
        Returns:
            Usuario creado
        """
        try:
            usuario = self.usuario_service.create_usuario(usuario_data)
            return {'success': True, 'usuario': usuario.to_dict()}
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            return {'success': False, 'message': str(e)}
    
    def update_usuario(self, user_id: int, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario
        
        Args:
            user_id: ID del usuario
            usuario_data: Nuevos datos
            
        Returns:
            Usuario actualizado
        """
        try:
            usuario = self.usuario_service.update_usuario(user_id, usuario_data)
            return {'success': True, 'usuario': usuario.to_dict()}
        except Exception as e:
            logger.error(f"Error actualizando usuario: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_usuario(self, user_id: int) -> Dict[str, Any]:
        """
        Elimina un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Resultado de la eliminación
        """
        try:
            success = self.usuario_service.delete_usuario(user_id)
            return {'success': success, 'message': 'Usuario eliminado correctamente'}
        except Exception as e:
            logger.error(f"Error eliminando usuario: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_mascotas(self, mascota_id: int = None, dueno_id: int = None) -> Dict[str, Any]:
        """
        Obtiene mascotas
        
        Args:
            mascota_id: ID específico de la mascota (opcional)
            dueno_id: ID del dueño para filtrar (opcional)
            
        Returns:
            Lista de mascotas o mascota específica
        """
        try:
            if mascota_id:
                mascota = self.mascota_service.get_mascota_by_id(mascota_id)
                if not mascota:
                    return {'success': False, 'message': 'Mascota no encontrada'}
                return {'success': True, 'mascota': mascota.to_dict()}
            elif dueno_id:
                mascotas = self.mascota_service.get_mascotas_by_dueno(dueno_id)
                return {'success': True, 'mascotas': [m.to_dict() for m in mascotas]}
            else:
                mascotas = self.mascota_service.get_all_mascotas()
                return {'success': True, 'mascotas': [m.to_dict() for m in mascotas]}
        except Exception as e:
            logger.error(f"Error obteniendo mascotas: {e}")
            return {'success': False, 'message': str(e)}
    
    def create_mascota(self, mascota_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva mascota
        
        Args:
            mascota_data: Datos de la mascota
            
        Returns:
            Mascota creada
        """
        try:
            mascota = self.mascota_service.create_mascota(mascota_data)
            return {'success': True, 'mascota': mascota.to_dict()}
        except Exception as e:
            logger.error(f"Error creando mascota: {e}")
            return {'success': False, 'message': str(e)}
    
    def update_mascota(self, mascota_id: int, mascota_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una mascota
        
        Args:
            mascota_id: ID de la mascota
            mascota_data: Nuevos datos
            
        Returns:
            Mascota actualizada
        """
        try:
            mascota = self.mascota_service.update_mascota(mascota_id, mascota_data)
            return {'success': True, 'mascota': mascota.to_dict()}
        except Exception as e:
            logger.error(f"Error actualizando mascota: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_mascota(self, mascota_id: int) -> Dict[str, Any]:
        """
        Elimina una mascota
        
        Args:
            mascota_id: ID de la mascota
            
        Returns:
            Resultado de la eliminación
        """
        try:
            success = self.mascota_service.delete_mascota(mascota_id)
            return {'success': success, 'message': 'Mascota eliminada correctamente'}
        except Exception as e:
            logger.error(f"Error eliminando mascota: {e}")
            return {'success': False, 'message': str(e)}
    
    def get_citas(self, cita_id: int = None, veterinario_id: int = None, 
                  dueno_id: int = None, estado: str = None) -> Dict[str, Any]:
        """
        Obtiene citas
        
        Args:
            cita_id: ID específico de la cita (opcional)
            veterinario_id: ID del veterinario para filtrar (opcional)
            dueno_id: ID del dueño para filtrar (opcional)
            estado: Estado para filtrar (opcional)
            
        Returns:
            Lista de citas o cita específica
        """
        try:
            if cita_id:
                cita = self.cita_service.get_cita_by_id(cita_id)
                if not cita:
                    return {'success': False, 'message': 'Cita no encontrada'}
                return {'success': True, 'cita': cita.to_dict()}
            elif veterinario_id:
                citas = self.cita_service.get_citas_by_veterinario(veterinario_id)
                return {'success': True, 'citas': [c.to_dict() for c in citas]}
            elif dueno_id:
                citas = self.cita_service.get_citas_by_dueno(dueno_id)
                return {'success': True, 'citas': [c.to_dict() for c in citas]}
            elif estado:
                citas = self.cita_service.get_citas_by_estado(estado)
                return {'success': True, 'citas': [c.to_dict() for c in citas]}
            else:
                citas = self.cita_service.get_all_citas()
                return {'success': True, 'citas': [c.to_dict() for c in citas]}
        except Exception as e:
            logger.error(f"Error obteniendo citas: {e}")
            return {'success': False, 'message': str(e)}
    
    def create_cita(self, cita_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva cita
        
        Args:
            cita_data: Datos de la cita
            
        Returns:
            Cita creada
        """
        try:
            cita = self.cita_service.create_cita(cita_data)
            return {'success': True, 'cita': cita.to_dict()}
        except Exception as e:
            logger.error(f"Error creando cita: {e}")
            return {'success': False, 'message': str(e)}
    
    def update_cita(self, cita_id: int, cita_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una cita
        
        Args:
            cita_id: ID de la cita
            cita_data: Nuevos datos
            
        Returns:
            Cita actualizada
        """
        try:
            cita = self.cita_service.update_cita(cita_id, cita_data)
            return {'success': True, 'cita': cita.to_dict()}
        except Exception as e:
            logger.error(f"Error actualizando cita: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_cita(self, cita_id: int) -> Dict[str, Any]:
        """
        Elimina una cita
        
        Args:
            cita_id: ID de la cita
            
        Returns:
            Resultado de la eliminación
        """
        try:
            success = self.cita_service.delete_cita(cita_id)
            return {'success': success, 'message': 'Cita eliminada correctamente'}
        except Exception as e:
            logger.error(f"Error eliminando cita: {e}")
            return {'success': False, 'message': str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica el estado del sistema
        
        Returns:
            Estado del sistema
        """
        try:
            db_connected = DatabaseConfig.test_connection()
            
            return {
                'status': 'healthy' if db_connected else 'unhealthy',
                'database': 'connected' if db_connected else 'disconnected',
                'timestamp': datetime.now().isoformat(),
                'version': self.settings.APP_VERSION
            }
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    # Métodos para historial clínico
    def get_historiales(self, historial_id: int = None, mascota_id: int = None) -> Dict[str, Any]:
        """
        Obtiene historiales clínicos
        
        Args:
            historial_id: ID específico del historial (opcional)
            mascota_id: ID de la mascota para filtrar (opcional)
            
        Returns:
            Lista de historiales o historial específico
        """
        try:
            if historial_id:
                historial = self.historial_service.get_historial_by_id(historial_id)
                if not historial:
                    return {'success': False, 'message': 'Historial no encontrado'}
                return {'success': True, 'historial': historial.to_dict()}
            elif mascota_id:
                historiales = self.historial_service.get_historiales_by_mascota(mascota_id)
                return {'success': True, 'historiales': [h.to_dict() for h in historiales]}
            else:
                historiales = self.historial_service.get_all_historiales()
                return {'success': True, 'historiales': [h.to_dict() for h in historiales]}
        except Exception as e:
            logger.error(f"Error obteniendo historiales: {e}")
            return {'success': False, 'message': str(e)}
    
    def create_historial(self, historial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo historial clínico
        
        Args:
            historial_data: Datos del historial
            
        Returns:
            Historial creado
        """
        try:
            historial = self.historial_service.create_historial(historial_data)
            return {'success': True, 'historial': historial.to_dict()}
        except Exception as e:
            logger.error(f"Error creando historial: {e}")
            return {'success': False, 'message': str(e)}
    
    def update_historial(self, historial_id: int, historial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un historial clínico
        
        Args:
            historial_id: ID del historial
            historial_data: Nuevos datos
            
        Returns:
            Historial actualizado
        """
        try:
            historial = self.historial_service.update_historial(historial_id, historial_data)
            return {'success': True, 'historial': historial.to_dict()}
        except Exception as e:
            logger.error(f"Error actualizando historial: {e}")
            return {'success': False, 'message': str(e)}
    
    def delete_historial(self, historial_id: int) -> Dict[str, Any]:
        """
        Elimina un historial clínico
        
        Args:
            historial_id: ID del historial
            
        Returns:
            Resultado de la eliminación
        """
        try:
            success = self.historial_service.delete_historial(historial_id)
            return {'success': success, 'message': 'Historial eliminado correctamente'}
        except Exception as e:
            logger.error(f"Error eliminando historial: {e}")
            return {'success': False, 'message': str(e)}

# Instancia global del backend
backend = MedicalPetsBackend()

def get_backend() -> MedicalPetsBackend:
    """Retorna la instancia global del backend"""
    return backend

if __name__ == "__main__":
    # Ejecutar health check
    health = backend.health_check()
    print(f"Estado del sistema: {health}") 