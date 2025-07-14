import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..config.database import DatabaseConfig
from ..config.settings import Settings
from ..models.cita import Cita
from ..utils.exceptions import ValidationError, DatabaseError
from ..utils.validators import CitaValidator

logger = logging.getLogger(__name__)

class CitaService:
    """Servicio de lógica de negocio para citas"""
    
    def __init__(self):
        self.settings = Settings()
        self.validator = CitaValidator()
    
    def get_all_citas(self) -> List[Cita]:
        """
        Obtiene todas las citas con información relacionada
        
        Returns:
            Lista de citas
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                ORDER BY c.fecha_hora DESC
            """
            cursor.execute(query)
            citas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            citas = []
            for data in citas_data:
                cita = Cita(
                    id=data['id'],
                    fecha_hora=data['fecha_hora'],
                    duracion_minutos=data['duracion_minutos'],
                    tipo=data['tipo'],
                    estado=data['estado'],
                    motivo=data['motivo'],
                    observaciones=data['observaciones'],
                    id_mascota=data['id_mascota'],
                    id_veterinario=data['id_veterinario'],
                    id_dueño=data['id_dueño'],
                    mascota_nombre=data['mascota_nombre'],
                    veterinario_nombre=data['veterinario_nombre'],
                    dueño_nombre=data['dueño_nombre'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            logger.error(f"Error obteniendo citas: {e}")
            raise DatabaseError(f"Error obteniendo citas: {str(e)}")
    
    def get_cita_by_id(self, cita_id: int) -> Optional[Cita]:
        """
        Obtiene una cita por su ID
        
        Args:
            cita_id: ID de la cita
            
        Returns:
            Cita encontrada o None
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                WHERE c.id = %s
            """
            cursor.execute(query, (cita_id,))
            data = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if not data:
                return None
            
            return Cita(
                id=data['id'],
                fecha_hora=data['fecha_hora'],
                duracion_minutos=data['duracion_minutos'],
                tipo=data['tipo'],
                estado=data['estado'],
                motivo=data['motivo'],
                observaciones=data['observaciones'],
                id_mascota=data['id_mascota'],
                id_veterinario=data['id_veterinario'],
                id_dueño=data['id_dueño'],
                mascota_nombre=data['mascota_nombre'],
                veterinario_nombre=data['veterinario_nombre'],
                dueño_nombre=data['dueño_nombre'],
                fecha_creacion=data.get('fecha_creacion'),
                fecha_actualizacion=data.get('fecha_actualizacion')
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo cita {cita_id}: {e}")
            raise DatabaseError(f"Error obteniendo cita: {str(e)}")
    
    def get_citas_by_veterinario(self, veterinario_id: int) -> List[Cita]:
        """
        Obtiene las citas de un veterinario específico
        
        Args:
            veterinario_id: ID del veterinario
            
        Returns:
            Lista de citas del veterinario
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                WHERE c.id_veterinario = %s
                ORDER BY c.fecha_hora
            """
            cursor.execute(query, (veterinario_id,))
            citas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            citas = []
            for data in citas_data:
                cita = Cita(
                    id=data['id'],
                    fecha_hora=data['fecha_hora'],
                    duracion_minutos=data['duracion_minutos'],
                    tipo=data['tipo'],
                    estado=data['estado'],
                    motivo=data['motivo'],
                    observaciones=data['observaciones'],
                    id_mascota=data['id_mascota'],
                    id_veterinario=data['id_veterinario'],
                    id_dueño=data['id_dueño'],
                    mascota_nombre=data['mascota_nombre'],
                    veterinario_nombre=data['veterinario_nombre'],
                    dueño_nombre=data['dueño_nombre'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            logger.error(f"Error obteniendo citas del veterinario {veterinario_id}: {e}")
            raise DatabaseError(f"Error obteniendo citas del veterinario: {str(e)}")
    
    def get_citas_by_dueno(self, dueno_id: int) -> List[Cita]:
        """
        Obtiene las citas de un dueño específico
        
        Args:
            dueno_id: ID del dueño
            
        Returns:
            Lista de citas del dueño
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                WHERE c.id_dueño = %s
                ORDER BY c.fecha_hora
            """
            cursor.execute(query, (dueno_id,))
            citas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            citas = []
            for data in citas_data:
                cita = Cita(
                    id=data['id'],
                    fecha_hora=data['fecha_hora'],
                    duracion_minutos=data['duracion_minutos'],
                    tipo=data['tipo'],
                    estado=data['estado'],
                    motivo=data['motivo'],
                    observaciones=data['observaciones'],
                    id_mascota=data['id_mascota'],
                    id_veterinario=data['id_veterinario'],
                    id_dueño=data['id_dueño'],
                    mascota_nombre=data['mascota_nombre'],
                    veterinario_nombre=data['veterinario_nombre'],
                    dueño_nombre=data['dueño_nombre'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            logger.error(f"Error obteniendo citas del dueño {dueno_id}: {e}")
            raise DatabaseError(f"Error obteniendo citas del dueño: {str(e)}")
    
    def get_citas_by_estado(self, estado: str) -> List[Cita]:
        """
        Obtiene citas por estado
        
        Args:
            estado: Estado de las citas a buscar
            
        Returns:
            Lista de citas con el estado especificado
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                WHERE c.estado = %s
                ORDER BY c.fecha_hora
            """
            cursor.execute(query, (estado,))
            citas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            citas = []
            for data in citas_data:
                cita = Cita(
                    id=data['id'],
                    fecha_hora=data['fecha_hora'],
                    duracion_minutos=data['duracion_minutos'],
                    tipo=data['tipo'],
                    estado=data['estado'],
                    motivo=data['motivo'],
                    observaciones=data['observaciones'],
                    id_mascota=data['id_mascota'],
                    id_veterinario=data['id_veterinario'],
                    id_dueño=data['id_dueño'],
                    mascota_nombre=data['mascota_nombre'],
                    veterinario_nombre=data['veterinario_nombre'],
                    dueño_nombre=data['dueño_nombre'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            logger.error(f"Error obteniendo citas por estado {estado}: {e}")
            raise DatabaseError(f"Error obteniendo citas por estado: {str(e)}")
    
    def get_citas_by_fecha(self, fecha: datetime) -> List[Cita]:
        """
        Obtiene citas por fecha
        
        Args:
            fecha: Fecha para buscar citas
            
        Returns:
            Lista de citas en la fecha especificada
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor(dictionary=True)
            
            # Buscar citas en la fecha especificada
            fecha_inicio = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = fecha_inicio + timedelta(days=1)
            
            query = """
                SELECT c.id, c.fecha_hora, c.duracion_minutos, c.tipo, c.estado,
                       c.motivo, c.observaciones, c.id_mascota, c.id_veterinario, c.id_dueño,
                       m.nombre AS mascota_nombre,
                       CONCAT(ud_vet.nombres, ' ', ud_vet.apellidos) AS veterinario_nombre,
                       CONCAT(ud_dueño.nombres, ' ', ud_dueño.apellidos) AS dueño_nombre,
                       c.fecha_creacion, c.fecha_actualizacion
                FROM citas c
                JOIN mascotas m ON c.id_mascota = m.id
                JOIN usuarios_detalle ud_vet ON c.id_veterinario = ud_vet.usuario_id
                JOIN usuarios_detalle ud_dueño ON c.id_dueño = ud_dueño.usuario_id
                WHERE c.fecha_hora >= %s AND c.fecha_hora < %s
                ORDER BY c.fecha_hora
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
            citas_data = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            citas = []
            for data in citas_data:
                cita = Cita(
                    id=data['id'],
                    fecha_hora=data['fecha_hora'],
                    duracion_minutos=data['duracion_minutos'],
                    tipo=data['tipo'],
                    estado=data['estado'],
                    motivo=data['motivo'],
                    observaciones=data['observaciones'],
                    id_mascota=data['id_mascota'],
                    id_veterinario=data['id_veterinario'],
                    id_dueño=data['id_dueño'],
                    mascota_nombre=data['mascota_nombre'],
                    veterinario_nombre=data['veterinario_nombre'],
                    dueño_nombre=data['dueño_nombre'],
                    fecha_creacion=data.get('fecha_creacion'),
                    fecha_actualizacion=data.get('fecha_actualizacion')
                )
                citas.append(cita)
            
            return citas
            
        except Exception as e:
            logger.error(f"Error obteniendo citas por fecha {fecha}: {e}")
            raise DatabaseError(f"Error obteniendo citas por fecha: {str(e)}")
    
    def create_cita(self, cita_data: Dict[str, Any]) -> Cita:
        """
        Crea una nueva cita
        
        Args:
            cita_data: Datos de la cita a crear
            
        Returns:
            Cita creada
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_cita_data(cita_data)
            
            # Verificar disponibilidad del veterinario
            if not self._verificar_disponibilidad_veterinario(
                cita_data['id_veterinario'], 
                cita_data['fecha_hora'], 
                cita_data['duracion_minutos']
            ):
                raise ValidationError("El veterinario no está disponible en ese horario")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            query = """
                INSERT INTO citas (fecha_hora, duracion_minutos, tipo, estado, motivo, 
                                  observaciones, id_mascota, id_veterinario, id_dueño, 
                                  fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                cita_data['fecha_hora'],
                cita_data.get('duracion_minutos', 30),
                cita_data.get('tipo', 'consulta_general'),
                cita_data.get('estado', 'programada'),
                cita_data.get('motivo', ''),
                cita_data.get('observaciones', ''),
                cita_data['id_mascota'],
                cita_data['id_veterinario'],
                cita_data['id_dueño'],
                datetime.now()
            ))
            cita_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener la cita creada
            cita = self.get_cita_by_id(cita_id)
            
            logger.info(f"Cita creada exitosamente: {cita.fecha_formateada}")
            return cita
            
        except Exception as e:
            logger.error(f"Error creando cita: {e}")
            raise DatabaseError(f"Error creando cita: {str(e)}")
    
    def update_cita(self, cita_id: int, cita_data: Dict[str, Any]) -> Cita:
        """
        Actualiza una cita existente
        
        Args:
            cita_id: ID de la cita a actualizar
            cita_data: Nuevos datos de la cita
            
        Returns:
            Cita actualizada
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_cita_data(cita_data, is_update=True)
            
            # Obtener cita actual
            cita_actual = self.get_cita_by_id(cita_id)
            if not cita_actual:
                raise ValidationError(f"Cita con ID {cita_id} no encontrada")
            
            # Verificar disponibilidad si se cambia la fecha/hora
            if 'fecha_hora' in cita_data and cita_data['fecha_hora'] != cita_actual.fecha_hora:
                if not self._verificar_disponibilidad_veterinario(
                    cita_data.get('id_veterinario', cita_actual.id_veterinario),
                    cita_data['fecha_hora'],
                    cita_data.get('duracion_minutos', cita_actual.duracion_minutos),
                    exclude_cita_id=cita_id
                ):
                    raise ValidationError("El veterinario no está disponible en ese horario")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            query = """
                UPDATE citas 
                SET fecha_hora=%s, duracion_minutos=%s, tipo=%s, estado=%s, 
                    motivo=%s, observaciones=%s, id_mascota=%s, id_veterinario=%s, 
                    id_dueño=%s, fecha_actualizacion=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                cita_data.get('fecha_hora', cita_actual.fecha_hora),
                cita_data.get('duracion_minutos', cita_actual.duracion_minutos),
                cita_data.get('tipo', cita_actual.tipo),
                cita_data.get('estado', cita_actual.estado),
                cita_data.get('motivo', cita_actual.motivo),
                cita_data.get('observaciones', cita_actual.observaciones),
                cita_data.get('id_mascota', cita_actual.id_mascota),
                cita_data.get('id_veterinario', cita_actual.id_veterinario),
                cita_data.get('id_dueño', cita_actual.id_dueño),
                datetime.now(),
                cita_id
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener la cita actualizada
            cita_actualizada = self.get_cita_by_id(cita_id)
            
            logger.info(f"Cita actualizada exitosamente: {cita_actualizada.fecha_formateada}")
            return cita_actualizada
            
        except Exception as e:
            logger.error(f"Error actualizando cita {cita_id}: {e}")
            raise DatabaseError(f"Error actualizando cita: {str(e)}")
    
    def delete_cita(self, cita_id: int) -> bool:
        """
        Elimina una cita
        
        Args:
            cita_id: ID de la cita a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Obtener cita para verificar que existe
            cita = self.get_cita_by_id(cita_id)
            if not cita:
                raise ValidationError(f"Cita con ID {cita_id} no encontrada")
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Eliminar cita
            cursor.execute("DELETE FROM citas WHERE id = %s", (cita_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            logger.info(f"Cita eliminada exitosamente: {cita.fecha_formateada}")
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando cita {cita_id}: {e}")
            raise DatabaseError(f"Error eliminando cita: {str(e)}")
    
    def _verificar_disponibilidad_veterinario(self, veterinario_id: int, fecha_hora: datetime, 
                                            duracion_minutos: int, exclude_cita_id: int = None) -> bool:
        """
        Verifica si un veterinario está disponible en un horario específico
        
        Args:
            veterinario_id: ID del veterinario
            fecha_hora: Fecha y hora de la cita
            duracion_minutos: Duración de la cita en minutos
            exclude_cita_id: ID de cita a excluir (para actualizaciones)
            
        Returns:
            True si está disponible, False en caso contrario
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                return False
            
            cursor = connection.cursor(dictionary=True)
            
            # Calcular fin de la cita
            fin_cita = fecha_hora + timedelta(minutes=duracion_minutos)
            
            # Buscar citas que se solapan
            query = """
                SELECT id FROM citas 
                WHERE id_veterinario = %s 
                AND estado NOT IN ('cancelada', 'no_asistio')
                AND (
                    (fecha_hora <= %s AND DATE_ADD(fecha_hora, INTERVAL duracion_minutos MINUTE) > %s)
                    OR (fecha_hora < %s AND DATE_ADD(fecha_hora, INTERVAL duracion_minutos MINUTE) >= %s)
                    OR (fecha_hora >= %s AND fecha_hora < %s)
                )
            """
            
            if exclude_cita_id:
                query += " AND id != %s"
                cursor.execute(query, (
                    veterinario_id, fecha_hora, fecha_hora, fin_cita, fin_cita, 
                    fecha_hora, fin_cita, exclude_cita_id
                ))
            else:
                cursor.execute(query, (
                    veterinario_id, fecha_hora, fecha_hora, fin_cita, fin_cita, 
                    fecha_hora, fin_cita
                ))
            
            citas_solapadas = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return len(citas_solapadas) == 0
            
        except Exception as e:
            logger.error(f"Error verificando disponibilidad del veterinario: {e}")
            return False
