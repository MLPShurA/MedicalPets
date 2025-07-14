import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..config.database import DatabaseConfig
from ..config.settings import Settings
from ..models.mascota import Mascota
from ..utils.exceptions import ValidationError, DatabaseError
from ..utils.validators import MascotaValidator

logger = logging.getLogger(__name__)

class MascotaService:
    """Servicio de lógica de negocio para mascotas"""
    
    def __init__(self):
        self.settings = Settings()
        self.validator = MascotaValidator()
    
    def get_all_mascotas(self) -> List[Mascota]:
        """
        Obtiene todas las mascotas con información del dueño
        
        Returns:
            Lista de mascotas
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT m.id, m.nombre, m.sexo, m.edad, m.raza, m.id_dueño,
                       ud.nombres AS dueño_nombre, ud.apellidos AS dueño_apellidos,
                       m.fecha_registro, m.fecha_actualizacion, m.estado
                FROM mascotas m
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                ORDER BY m.nombre
            """
            cursor.execute(query)
            mascotas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            mascotas = []
            for data in mascotas_data:
                mascota = Mascota(
                    id=data['id'],
                    nombre=data['nombre'],
                    sexo=data['sexo'],
                    edad=data['edad'],
                    raza=data['raza'],
                    id_dueño=data['id_dueño'],
                    dueño_nombre=data['dueño_nombre'],
                    dueño_apellidos=data['dueño_apellidos'],
                    fecha_registro=data.get('fecha_registro'),
                    fecha_actualizacion=data.get('fecha_actualizacion'),
                    estado=data.get('estado', 'activo')
                )
                mascotas.append(mascota)
            
            return mascotas
            
        except Exception as e:
            logger.error(f"Error obteniendo mascotas: {e}")
            raise DatabaseError(f"Error obteniendo mascotas: {str(e)}")
    
    def get_mascota_by_id(self, mascota_id: int) -> Optional[Mascota]:
        """
        Obtiene una mascota por su ID
        
        Args:
            mascota_id: ID de la mascota
            
        Returns:
            Mascota encontrada o None
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT m.id, m.nombre, m.sexo, m.edad, m.raza, m.id_dueño,
                       ud.nombres AS dueño_nombre, ud.apellidos AS dueño_apellidos,
                       m.fecha_registro, m.fecha_actualizacion, m.estado
                FROM mascotas m
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                WHERE m.id = %s
            """
            cursor.execute(query, (mascota_id,))
            data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not data:
                return None
            
            return Mascota(
                id=data['id'],
                nombre=data['nombre'],
                sexo=data['sexo'],
                edad=data['edad'],
                raza=data['raza'],
                id_dueño=data['id_dueño'],
                dueño_nombre=data['dueño_nombre'],
                dueño_apellidos=data['dueño_apellidos'],
                fecha_registro=data.get('fecha_registro'),
                fecha_actualizacion=data.get('fecha_actualizacion'),
                estado=data.get('estado', 'activo')
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo mascota {mascota_id}: {e}")
            raise DatabaseError(f"Error obteniendo mascota: {str(e)}")
    
    def get_mascotas_by_dueno(self, dueno_id: int) -> List[Mascota]:
        """
        Obtiene las mascotas de un dueño específico
        
        Args:
            dueno_id: ID del dueño
            
        Returns:
            Lista de mascotas del dueño
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT m.id, m.nombre, m.sexo, m.edad, m.raza, m.id_dueño,
                       ud.nombres AS dueño_nombre, ud.apellidos AS dueño_apellidos,
                       m.fecha_registro, m.fecha_actualizacion, m.estado
                FROM mascotas m
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                WHERE m.id_dueño = %s
                ORDER BY m.nombre
            """
            cursor.execute(query, (dueno_id,))
            mascotas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            mascotas = []
            for data in mascotas_data:
                mascota = Mascota(
                    id=data['id'],
                    nombre=data['nombre'],
                    sexo=data['sexo'],
                    edad=data['edad'],
                    raza=data['raza'],
                    id_dueño=data['id_dueño'],
                    dueño_nombre=data['dueño_nombre'],
                    dueño_apellidos=data['dueño_apellidos'],
                    fecha_registro=data.get('fecha_registro'),
                    fecha_actualizacion=data.get('fecha_actualizacion'),
                    estado=data.get('estado', 'activo')
                )
                mascotas.append(mascota)
            
            return mascotas
            
        except Exception as e:
            logger.error(f"Error obteniendo mascotas del dueño {dueno_id}: {e}")
            raise DatabaseError(f"Error obteniendo mascotas del dueño: {str(e)}")
    
    def create_mascota(self, mascota_data: Dict[str, Any]) -> Mascota:
        """
        Crea una nueva mascota
        
        Args:
            mascota_data: Datos de la mascota a crear
            
        Returns:
            Mascota creada
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_mascota_data(mascota_data)
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Calcular edad en meses
            edad_anos = mascota_data.get('edad_anos', 0)
            edad_meses = mascota_data.get('edad_meses', 0)
            edad_total = edad_anos * 12 + edad_meses
            
            query = """
                INSERT INTO mascotas (nombre, sexo, edad, raza, id_dueño, fecha_registro)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                mascota_data['nombre'],
                mascota_data['sexo'],
                edad_total,
                mascota_data['raza'],
                mascota_data['id_dueño'],
                datetime.now()
            ))
            mascota_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener la mascota creada con información del dueño
            mascota = self.get_mascota_by_id(mascota_id)
            
            logger.info(f"Mascota creada exitosamente: {mascota.nombre}")
            return mascota
            
        except Exception as e:
            logger.error(f"Error creando mascota: {e}")
            raise DatabaseError(f"Error creando mascota: {str(e)}")
    
    def update_mascota(self, mascota_id: int, mascota_data: Dict[str, Any]) -> Mascota:
        """
        Actualiza una mascota existente
        
        Args:
            mascota_id: ID de la mascota a actualizar
            mascota_data: Nuevos datos de la mascota
            
        Returns:
            Mascota actualizada
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_mascota_data(mascota_data, is_update=True)
            
            # Obtener mascota actual
            mascota_actual = self.get_mascota_by_id(mascota_id)
            if not mascota_actual:
                raise ValidationError(f"Mascota con ID {mascota_id} no encontrada")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Calcular edad en meses
            edad_anos = mascota_data.get('edad_anos', 0)
            edad_meses = mascota_data.get('edad_meses', 0)
            edad_total = edad_anos * 12 + edad_meses
            
            query = """
                UPDATE mascotas 
                SET nombre=%s, sexo=%s, edad=%s, raza=%s, id_dueño=%s, fecha_actualizacion=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                mascota_data['nombre'],
                mascota_data['sexo'],
                edad_total,
                mascota_data['raza'],
                mascota_data['id_dueño'],
                datetime.now(),
                mascota_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener la mascota actualizada
            mascota_actualizada = self.get_mascota_by_id(mascota_id)
            
            logger.info(f"Mascota actualizada exitosamente: {mascota_actualizada.nombre}")
            return mascota_actualizada
            
        except Exception as e:
            logger.error(f"Error actualizando mascota {mascota_id}: {e}")
            raise DatabaseError(f"Error actualizando mascota: {str(e)}")
    
    def delete_mascota(self, mascota_id: int) -> bool:
        """
        Elimina una mascota
        
        Args:
            mascota_id: ID de la mascota a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Obtener mascota para verificar que existe
            mascota = self.get_mascota_by_id(mascota_id)
            if not mascota:
                raise ValidationError(f"Mascota con ID {mascota_id} no encontrada")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Eliminar mascota
            cursor.execute("DELETE FROM mascotas WHERE id = %s", (mascota_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Mascota eliminada exitosamente: {mascota.nombre}")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando mascota {mascota_id}: {e}")
            raise DatabaseError(f"Error eliminando mascota: {str(e)}")
    
    def get_mascotas_by_estado(self, estado: str) -> List[Mascota]:
        """
        Obtiene mascotas por estado
        
        Args:
            estado: Estado de las mascotas a buscar
            
        Returns:
            Lista de mascotas con el estado especificado
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT m.id, m.nombre, m.sexo, m.edad, m.raza, m.id_dueño,
                       ud.nombres AS dueño_nombre, ud.apellidos AS dueño_apellidos,
                       m.fecha_registro, m.fecha_actualizacion, m.estado
                FROM mascotas m
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                WHERE m.estado = %s
                ORDER BY m.nombre
            """
            cursor.execute(query, (estado,))
            mascotas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            mascotas = []
            for data in mascotas_data:
                mascota = Mascota(
                    id=data['id'],
                    nombre=data['nombre'],
                    sexo=data['sexo'],
                    edad=data['edad'],
                    raza=data['raza'],
                    id_dueño=data['id_dueño'],
                    dueño_nombre=data['dueño_nombre'],
                    dueño_apellidos=data['dueño_apellidos'],
                    fecha_registro=data.get('fecha_registro'),
                    fecha_actualizacion=data.get('fecha_actualizacion'),
                    estado=data.get('estado', 'activo')
                )
                mascotas.append(mascota)
            
            return mascotas
            
        except Exception as e:
            logger.error(f"Error obteniendo mascotas por estado {estado}: {e}")
            raise DatabaseError(f"Error obteniendo mascotas por estado: {str(e)}")
