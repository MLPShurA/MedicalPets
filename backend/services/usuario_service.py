import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..config.database import DatabaseConfig
from ..config.settings import Settings
from ..models.usuario import Usuario
from ..utils.exceptions import ValidationError, DatabaseError
from ..utils.validators import UsuarioValidator

logger = logging.getLogger(__name__)

class UsuarioService:
    """Servicio de lógica de negocio para usuarios"""
    
    def __init__(self):
        self.settings = Settings()
        self.validator = UsuarioValidator()
    
    def get_all_usuarios(self) -> List[Usuario]:
        """
        Obtiene todos los usuarios con sus detalles
        
        Returns:
            Lista de usuarios
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    ud.id AS detalle_id,
                    ud.nombres,
                    ud.apellidos,
                    ud.cedula,
                    ud.telefono,
                    ud.correo_electronico,
                    ud.direccion,
                    ud.usuario_id,
                    u.rol,
                    u.nombre_usuario,
                    u.fecha_creacion,
                    u.fecha_actualizacion,
                    (
                        SELECT m.nombre 
                        FROM mascotas m 
                        WHERE m.id_dueño = u.id 
                        ORDER BY m.id ASC 
                        LIMIT 1
                    ) AS mascota
                FROM usuarios_detalle ud
                JOIN usuarios u ON ud.usuario_id = u.id
                ORDER BY ud.nombres, ud.apellidos
            """
            cursor.execute(query)
            usuarios_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            usuarios = []
            for data in usuarios_data:
                usuario = Usuario(
                    id=data['usuario_id'],
                    nombre_usuario=data['nombre_usuario'],
                    rol=data['rol'],
                    detalle_id=data['detalle_id'],
                    nombres=data['nombres'],
                    apellidos=data['apellidos'],
                    cedula=data['cedula'],
                    telefono=data['telefono'],
                    correo_electronico=data['correo_electronico'],
                    direccion=data['direccion'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                usuarios.append(usuario)
            
            return usuarios
            
        except Exception as e:
            logger.error(f"Error obteniendo usuarios: {e}")
            raise DatabaseError(f"Error obteniendo usuarios: {str(e)}")
    
    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Usuario encontrado o None
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    ud.id AS detalle_id,
                    ud.nombres,
                    ud.apellidos,
                    ud.cedula,
                    ud.telefono,
                    ud.correo_electronico,
                    ud.direccion,
                    ud.usuario_id,
                    u.rol,
                    u.nombre_usuario,
                    u.fecha_creacion,
                    u.fecha_actualizacion
                FROM usuarios_detalle ud
                JOIN usuarios u ON ud.usuario_id = u.id
                WHERE u.id = %s
            """
            cursor.execute(query, (usuario_id,))
            data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not data:
                return None
            
            return Usuario(
                id=data['usuario_id'],
                nombre_usuario=data['nombre_usuario'],
                rol=data['rol'],
                detalle_id=data['detalle_id'],
                nombres=data['nombres'],
                apellidos=data['apellidos'],
                cedula=data['cedula'],
                telefono=data['telefono'],
                correo_electronico=data['correo_electronico'],
                direccion=data['direccion'],
                fecha_creacion=data.get('fecha_creacion'),
                fecha_actualizacion=data.get('fecha_actualizacion')
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo usuario {usuario_id}: {e}")
            raise DatabaseError(f"Error obteniendo usuario: {str(e)}")
    
    def create_usuario(self, usuario_data: Dict[str, Any]) -> Usuario:
        """
        Crea un nuevo usuario
        
        Args:
            usuario_data: Datos del usuario a crear
            
        Returns:
            Usuario creado
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_usuario_data(usuario_data)
            
            # Generar contraseña automática
            from .auth_service import AuthService
            auth_service = AuthService()
            contrasena = auth_service.generate_password(
                usuario_data['nombres'],
                usuario_data['apellidos'],
                usuario_data['cedula']
            )
            contrasena_hash = auth_service.hash_password(contrasena)
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Insertar en tabla usuarios
            query_usuarios = """
                INSERT INTO usuarios (nombre_usuario, contrasena, contrasena_hash, rol, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_usuarios, (
                usuario_data['correo_electronico'],
                contrasena,
                contrasena_hash,
                usuario_data['rol'],
                datetime.now()
            ))
            usuario_id = cursor.lastrowid
            
            # Insertar en tabla usuarios_detalle
            query_detalle = """
                INSERT INTO usuarios_detalle 
                (nombres, apellidos, cedula, telefono, correo_electronico, direccion, usuario_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query_detalle, (
                usuario_data['nombres'],
                usuario_data['apellidos'],
                usuario_data['cedula'],
                usuario_data['telefono'],
                usuario_data['correo_electronico'],
                usuario_data['direccion'],
                usuario_id
            ))
            detalle_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Crear objeto Usuario
            usuario = Usuario(
                id=usuario_id,
                nombre_usuario=usuario_data['correo_electronico'],
                rol=usuario_data['rol'],
                detalle_id=detalle_id,
                nombres=usuario_data['nombres'],
                apellidos=usuario_data['apellidos'],
                cedula=usuario_data['cedula'],
                telefono=usuario_data['telefono'],
                correo_electronico=usuario_data['correo_electronico'],
                direccion=usuario_data['direccion'],
                fecha_creacion=datetime.now()
            )
            
            logger.info(f"Usuario creado exitosamente: {usuario.nombre_completo}")
            return usuario
            
        except Exception as e:
            logger.error(f"Error creando usuario: {e}")
            raise DatabaseError(f"Error creando usuario: {str(e)}")
    
    def update_usuario(self, usuario_id: int, usuario_data: Dict[str, Any]) -> Usuario:
        """
        Actualiza un usuario existente
        
        Args:
            usuario_id: ID del usuario a actualizar
            usuario_data: Nuevos datos del usuario
            
        Returns:
            Usuario actualizado
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_usuario_data(usuario_data, is_update=True)
            
            # Obtener usuario actual
            usuario_actual = self.get_usuario_by_id(usuario_id)
            if not usuario_actual:
                raise ValidationError(f"Usuario con ID {usuario_id} no encontrado")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Actualizar tabla usuarios_detalle
            query_update_detalle = """
                UPDATE usuarios_detalle 
                SET nombres=%s, apellidos=%s, cedula=%s, telefono=%s, 
                    correo_electronico=%s, direccion=%s 
                WHERE id=%s
            """
            cursor.execute(query_update_detalle, (
                usuario_data['nombres'],
                usuario_data['apellidos'],
                usuario_data['cedula'],
                usuario_data['telefono'],
                usuario_data['correo_electronico'],
                usuario_data['direccion'],
                usuario_actual.detalle_id
            ))
            
            # Actualizar tabla usuarios
            query_update_usuarios = """
                UPDATE usuarios 
                SET rol=%s, fecha_actualizacion=%s 
                WHERE id=%s
            """
            cursor.execute(query_update_usuarios, (
                usuario_data['rol'],
                datetime.now(),
                usuario_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Actualizar objeto Usuario
            usuario_actual.nombres = usuario_data['nombres']
            usuario_actual.apellidos = usuario_data['apellidos']
            usuario_actual.cedula = usuario_data['cedula']
            usuario_actual.telefono = usuario_data['telefono']
            usuario_actual.correo_electronico = usuario_data['correo_electronico']
            usuario_actual.direccion = usuario_data['direccion']
            usuario_actual.rol = usuario_data['rol']
            usuario_actual.fecha_actualizacion = datetime.now()
            
            logger.info(f"Usuario actualizado exitosamente: {usuario_actual.nombre_completo}")
            return usuario_actual
            
        except Exception as e:
            logger.error(f"Error actualizando usuario {usuario_id}: {e}")
            raise DatabaseError(f"Error actualizando usuario: {str(e)}")
    
    def delete_usuario(self, usuario_id: int) -> bool:
        """
        Elimina un usuario
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Obtener usuario para verificar que existe
            usuario = self.get_usuario_by_id(usuario_id)
            if not usuario:
                raise ValidationError(f"Usuario con ID {usuario_id} no encontrado")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Eliminar de usuarios_detalle primero (por la foreign key)
            cursor.execute("DELETE FROM usuarios_detalle WHERE id = %s", (usuario.detalle_id,))
            
            # Eliminar de usuarios
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Usuario eliminado exitosamente: {usuario.nombre_completo}")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando usuario {usuario_id}: {e}")
            raise DatabaseError(f"Error eliminando usuario: {str(e)}")
    
    def get_usuarios_by_rol(self, rol: str) -> List[Usuario]:
        """
        Obtiene usuarios por rol
        
        Args:
            rol: Rol de los usuarios a buscar
            
        Returns:
            Lista de usuarios con el rol especificado
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT 
                    ud.id AS detalle_id,
                    ud.nombres,
                    ud.apellidos,
                    ud.cedula,
                    ud.telefono,
                    ud.correo_electronico,
                    ud.direccion,
                    ud.usuario_id,
                    u.rol,
                    u.nombre_usuario,
                    u.fecha_creacion,
                    u.fecha_actualizacion
                FROM usuarios_detalle ud
                JOIN usuarios u ON ud.usuario_id = u.id
                WHERE u.rol = %s
                ORDER BY ud.nombres, ud.apellidos
            """
            cursor.execute(query, (rol,))
            usuarios_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            usuarios = []
            for data in usuarios_data:
                usuario = Usuario(
                    id=data['usuario_id'],
                    nombre_usuario=data['nombre_usuario'],
                    rol=data['rol'],
                    detalle_id=data['detalle_id'],
                    nombres=data['nombres'],
                    apellidos=data['apellidos'],
                    cedula=data['cedula'],
                    telefono=data['telefono'],
                    correo_electronico=data['correo_electronico'],
                    direccion=data['direccion'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                usuarios.append(usuario)
            
            return usuarios
            
        except Exception as e:
            logger.error(f"Error obteniendo usuarios por rol {rol}: {e}")
            raise DatabaseError(f"Error obteniendo usuarios por rol: {str(e)}")
