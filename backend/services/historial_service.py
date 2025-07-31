import logging
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from decimal import Decimal

from ..models.historial import HistorialClinico, Tratamiento
from ..config.database import DatabaseConfig
from ..utils.exceptions import DatabaseError, ValidationError
from ..utils.validators import HistorialValidator

logger = logging.getLogger(__name__)

class HistorialService:
    """Servicio para gestionar historiales clínicos"""
    
    def __init__(self):
        self.validator = HistorialValidator()
    
    def get_all_historiales(self) -> List[HistorialClinico]:
        """
        Obtiene todos los historiales clínicos
        
        Returns:
            Lista de historiales clínicos
            
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
                    hc.id,
                    hc.id_mascota,
                    hc.fecha,
                    hc.motivo_consulta,
                    hc.sintomas,
                    hc.antecedentes,
                    hc.diagnostico,
                    hc.observaciones,
                    hc.peso,
                    m.nombre AS mascota_nombre,
                    m.raza AS mascota_raza,
                    m.sexo AS mascota_sexo,
                    ud.nombres AS dueño_nombre
                FROM historial_clinico hc
                JOIN mascotas m ON hc.id_mascota = m.id
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                ORDER BY hc.fecha DESC, hc.id DESC
            """
            cursor.execute(query)
            historiales_data = cursor.fetchall()
            cursor.close()
            connection.close()
            
            historiales = []
            for data in historiales_data:
                historial = HistorialClinico(
                    id=data['id'],
                    id_mascota=data['id_mascota'],
                    fecha=data['fecha'],
                    motivo_consulta=data['motivo_consulta'],
                    sintomas=data['sintomas'],
                    antecedentes=data['antecedentes'],
                    diagnostico=data['diagnostico'],
                    observaciones=data['observaciones'],
                    peso=data['peso'],
                    mascota_nombre=data['mascota_nombre'],
                    mascota_raza=data['mascota_raza'],
                    mascota_sexo=data['mascota_sexo'],
                    dueño_nombre=data['dueño_nombre']
                )
                
                # Obtener tratamientos del historial
                historial.tratamientos = self._get_tratamientos_by_historial_id(data['id'])
                historiales.append(historial)
            
            return historiales
            
        except Exception as e:
            logger.error(f"Error obteniendo historiales: {e}")
            raise DatabaseError(f"Error obteniendo historiales: {str(e)}")
    
    def get_historial_by_id(self, historial_id: int) -> Optional[HistorialClinico]:
        """
        Obtiene un historial clínico por ID
        
        Args:
            historial_id: ID del historial
            
        Returns:
            Historial clínico o None si no existe
            
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
                    hc.id,
                    hc.id_mascota,
                    hc.fecha,
                    hc.motivo_consulta,
                    hc.sintomas,
                    hc.antecedentes,
                    hc.diagnostico,
                    hc.observaciones,
                    hc.peso,
                    m.nombre AS mascota_nombre,
                    m.raza AS mascota_raza,
                    m.sexo AS mascota_sexo,
                    ud.nombres AS dueño_nombre
                FROM historial_clinico hc
                JOIN mascotas m ON hc.id_mascota = m.id
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                WHERE hc.id = %s
            """
            cursor.execute(query, (historial_id,))
            data = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if not data:
                return None
            
            historial = HistorialClinico(
                id=data['id'],
                id_mascota=data['id_mascota'],
                fecha=data['fecha'],
                motivo_consulta=data['motivo_consulta'],
                sintomas=data['sintomas'],
                antecedentes=data['antecedentes'],
                diagnostico=data['diagnostico'],
                observaciones=data['observaciones'],
                peso=data['peso'],
                mascota_nombre=data['mascota_nombre'],
                mascota_raza=data['mascota_raza'],
                mascota_sexo=data['mascota_sexo'],
                dueño_nombre=data['dueño_nombre']
            )
            
            # Obtener tratamientos
            historial.tratamientos = self._get_tratamientos_by_historial_id(data['id'])
            
            return historial
            
        except Exception as e:
            logger.error(f"Error obteniendo historial {historial_id}: {e}")
            raise DatabaseError(f"Error obteniendo historial: {str(e)}")
    
    def get_historiales_by_mascota(self, mascota_id: int) -> List[HistorialClinico]:
        """
        Obtiene todos los historiales de una mascota
        
        Args:
            mascota_id: ID de la mascota
            
        Returns:
            Lista de historiales de la mascota
            
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
                    hc.id,
                    hc.id_mascota,
                    hc.fecha,
                    hc.motivo_consulta,
                    hc.sintomas,
                    hc.antecedentes,
                    hc.diagnostico,
                    hc.observaciones,
                    hc.peso,
                    m.nombre AS mascota_nombre,
                    m.raza AS mascota_raza,
                    m.sexo AS mascota_sexo,
                    ud.nombres AS dueño_nombre
                FROM historial_clinico hc
                JOIN mascotas m ON hc.id_mascota = m.id
                JOIN usuarios_detalle ud ON m.id_dueño = ud.usuario_id
                WHERE hc.id_mascota = %s
                ORDER BY hc.fecha DESC, hc.id DESC
            """
            cursor.execute(query, (mascota_id,))
            historiales_data = cursor.fetchall()
            cursor.close()
            connection.close()
            
            historiales = []
            for data in historiales_data:
                historial = HistorialClinico(
                    id=data['id'],
                    id_mascota=data['id_mascota'],
                    fecha=data['fecha'],
                    motivo_consulta=data['motivo_consulta'],
                    sintomas=data['sintomas'],
                    antecedentes=data['antecedentes'],
                    diagnostico=data['diagnostico'],
                    observaciones=data['observaciones'],
                    peso=data['peso'],
                    mascota_nombre=data['mascota_nombre'],
                    mascota_raza=data['mascota_raza'],
                    mascota_sexo=data['mascota_sexo'],
                    dueño_nombre=data['dueño_nombre']
                )
                
                # Obtener tratamientos
                historial.tratamientos = self._get_tratamientos_by_historial_id(data['id'])
                historiales.append(historial)
            
            return historiales
            
        except Exception as e:
            logger.error(f"Error obteniendo historiales de mascota {mascota_id}: {e}")
            raise DatabaseError(f"Error obteniendo historiales de mascota: {str(e)}")
    
    def create_historial(self, historial_data: Dict[str, Any]) -> HistorialClinico:
        """
        Crea un nuevo historial clínico
        
        Args:
            historial_data: Datos del historial a crear
            
        Returns:
            Historial clínico creado
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_historial_data(historial_data)
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Insertar historial clínico
            query = """
                INSERT INTO historial_clinico 
                (id_mascota, fecha, motivo_consulta, sintomas, antecedentes, diagnostico, observaciones, peso)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                historial_data['id_mascota'],
                historial_data['fecha'],
                historial_data['motivo_consulta'],
                historial_data.get('sintomas', ''),
                historial_data.get('antecedentes', ''),
                historial_data.get('diagnostico', ''),
                historial_data.get('observaciones', ''),
                historial_data.get('peso')
            ))
            historial_id = cursor.lastrowid
            
            # Insertar tratamientos si existen
            tratamientos = historial_data.get('tratamientos', [])
            for tratamiento_data in tratamientos:
                self._create_tratamiento(historial_id, tratamiento_data, cursor)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener el historial creado
            return self.get_historial_by_id(historial_id)
            
        except Exception as e:
            logger.error(f"Error creando historial: {e}")
            raise DatabaseError(f"Error creando historial: {str(e)}")
    
    def update_historial(self, historial_id: int, historial_data: Dict[str, Any]) -> HistorialClinico:
        """
        Actualiza un historial clínico
        
        Args:
            historial_id: ID del historial a actualizar
            historial_data: Datos actualizados
            
        Returns:
            Historial clínico actualizado
            
        Raises:
            ValidationError: Si los datos no son válidos
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            # Validar datos
            self.validator.validate_historial_data(historial_data, is_update=True)
            
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Actualizar historial clínico
            query = """
                UPDATE historial_clinico 
                SET id_mascota=%s, fecha=%s, motivo_consulta=%s, sintomas=%s, 
                    antecedentes=%s, diagnostico=%s, observaciones=%s, peso=%s
                WHERE id=%s
            """
            cursor.execute(query, (
                historial_data['id_mascota'],
                historial_data['fecha'],
                historial_data['motivo_consulta'],
                historial_data.get('sintomas', ''),
                historial_data.get('antecedentes', ''),
                historial_data.get('diagnostico', ''),
                historial_data.get('observaciones', ''),
                historial_data.get('peso'),
                historial_id
            ))
            
            # Eliminar tratamientos anteriores
            cursor.execute("DELETE FROM tratamientos WHERE id_historial=%s", (historial_id,))
            
            # Insertar nuevos tratamientos
            tratamientos = historial_data.get('tratamientos', [])
            for tratamiento_data in tratamientos:
                self._create_tratamiento(historial_id, tratamiento_data, cursor)
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Obtener el historial actualizado
            return self.get_historial_by_id(historial_id)
            
        except Exception as e:
            logger.error(f"Error actualizando historial {historial_id}: {e}")
            raise DatabaseError(f"Error actualizando historial: {str(e)}")
    
    def delete_historial(self, historial_id: int) -> bool:
        """
        Elimina un historial clínico
        
        Args:
            historial_id: ID del historial a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            DatabaseError: Si hay un error en la base de datos
        """
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                raise DatabaseError("Error de conexión a la base de datos")
            
            cursor = connection.cursor()
            
            # Eliminar tratamientos primero (por la FK)
            cursor.execute("DELETE FROM tratamientos WHERE id_historial=%s", (historial_id,))
            
            # Eliminar historial
            cursor.execute("DELETE FROM historial_clinico WHERE id=%s", (historial_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Error eliminando historial {historial_id}: {e}")
            raise DatabaseError(f"Error eliminando historial: {str(e)}")
    
    def _get_tratamientos_by_historial_id(self, historial_id: int) -> List[Tratamiento]:
        """Obtiene los tratamientos de un historial"""
        try:
            connection = DatabaseConfig.get_connection()
            if not connection:
                return []
            
            cursor = connection.cursor(dictionary=True)
            
            query = """
                SELECT id, nombre_tratamiento, dosis, frecuencia, duracion, observaciones, fecha_inicio, fecha_fin
                FROM tratamientos
                WHERE id_historial = %s
                ORDER BY fecha_inicio
            """
            cursor.execute(query, (historial_id,))
            tratamientos_data = cursor.fetchall()
            cursor.close()
            connection.close()
            
            tratamientos = []
            for data in tratamientos_data:
                tratamiento = Tratamiento(
                    id=data['id'],
                    id_historial=historial_id,
                    nombre=data['nombre_tratamiento'],
                    dosis=data['dosis'],
                    frecuencia=data['frecuencia'],
                    duracion_dias=0,  # Campo requerido por la nueva clase
                    observaciones=data['observaciones'],
                    fecha_inicio=data['fecha_inicio'],
                    fecha_fin=data['fecha_fin']
                )
                tratamientos.append(tratamiento)
            
            return tratamientos
            
        except Exception as e:
            logger.error(f"Error obteniendo tratamientos del historial {historial_id}: {e}")
            return []
    
    def _create_tratamiento(self, historial_id: int, tratamiento_data: Dict[str, Any], cursor) -> None:
        """Crea un tratamiento para un historial"""
        query = """
            INSERT INTO tratamientos 
            (id_historial, nombre_tratamiento, dosis, frecuencia, duracion, observaciones, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            historial_id,
            tratamiento_data['nombre_tratamiento'],
            tratamiento_data.get('dosis', ''),
            tratamiento_data.get('frecuencia', ''),
            tratamiento_data.get('duracion', ''),
            tratamiento_data.get('observaciones', ''),
            tratamiento_data.get('fecha_inicio'),
            tratamiento_data.get('fecha_fin')
        )) 