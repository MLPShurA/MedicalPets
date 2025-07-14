import re
from typing import Dict, Any
from ..config.settings import Settings
from .exceptions import ValidationError
from datetime import date

class UsuarioValidator:
    """Validador para datos de usuario"""
    
    def __init__(self):
        self.settings = Settings()
    
    def validate_usuario_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """
        Valida los datos de un usuario
        
        Args:
            data: Datos del usuario a validar
            is_update: Si es una actualización (algunos campos pueden ser opcionales)
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = []
        
        # Validar campos obligatorios
        required_fields = ['nombres', 'apellidos', 'cedula', 'correo_electronico', 'rol']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"El campo '{field}' es obligatorio")
        
        # Validar nombres y apellidos
        if data.get('nombres') and len(data['nombres'].strip()) < 2:
            errors.append("Los nombres deben tener al menos 2 caracteres")
        
        if data.get('apellidos') and len(data['apellidos'].strip()) < 2:
            errors.append("Los apellidos deben tener al menos 2 caracteres")
        
        # Validar cédula
        if data.get('cedula'):
            cedula_pattern = self.settings.VALIDATION_RULES.get('cedula', r'^\d{10}$')
            if not re.match(cedula_pattern, data['cedula']):
                errors.append("La cédula debe tener 10 dígitos numéricos")
        
        # Validar correo electrónico
        if data.get('correo_electronico'):
            email_pattern = self.settings.VALIDATION_RULES.get('email', r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not re.match(email_pattern, data['correo_electronico']):
                errors.append("El correo electrónico no tiene un formato válido")
        
        # Validar teléfono
        if data.get('telefono'):
            phone_pattern = self.settings.VALIDATION_RULES.get('phone', r'^\+?[\d\s\-\(\)]{7,15}$')
            if not re.match(phone_pattern, data['telefono']):
                errors.append("El teléfono no tiene un formato válido")
        
        # Validar rol
        if data.get('rol') and data['rol'] not in self.settings.ROLES:
            valid_roles = ', '.join(self.settings.ROLES.keys())
            errors.append(f"El rol debe ser uno de: {valid_roles}")
        
        if errors:
            raise ValidationError("; ".join(errors))

class MascotaValidator:
    """Validador para datos de mascota"""
    
    def __init__(self):
        self.settings = Settings()
    
    def validate_mascota_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """
        Valida los datos de una mascota
        
        Args:
            data: Datos de la mascota a validar
            is_update: Si es una actualización
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = []
        
        # Validar campos obligatorios
        required_fields = ['nombre', 'sexo', 'raza', 'id_dueño']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"El campo '{field}' es obligatorio")
        
        # Validar nombre
        if data.get('nombre') and len(data['nombre'].strip()) < 2:
            errors.append("El nombre debe tener al menos 2 caracteres")
        
        # Validar sexo
        if data.get('sexo') and data['sexo'] not in ['Macho', 'Hembra']:
            errors.append("El sexo debe ser 'Macho' o 'Hembra'")
        
        # Validar edad
        if data.get('edad') is not None:
            if not isinstance(data['edad'], int) or data['edad'] < 0:
                errors.append("La edad debe ser un número entero positivo")
        
        # Validar raza
        if data.get('raza') and len(data['raza'].strip()) < 2:
            errors.append("La raza debe tener al menos 2 caracteres")
        
        # Validar ID del dueño
        if data.get('id_dueño') and not isinstance(data['id_dueño'], int):
            errors.append("El ID del dueño debe ser un número entero")
        
        if errors:
            raise ValidationError("; ".join(errors))

class CitaValidator:
    """Validador para datos de cita"""
    
    def __init__(self):
        self.settings = Settings()
    
    def validate_cita_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """
        Valida los datos de una cita
        
        Args:
            data: Datos de la cita a validar
            is_update: Si es una actualización
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = []
        
        # Validar campos obligatorios
        required_fields = ['fecha_hora', 'id_mascota', 'id_veterinario']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"El campo '{field}' es obligatorio")
        
        # Validar fecha y hora
        if data.get('fecha_hora'):
            from datetime import datetime
            try:
                if isinstance(data['fecha_hora'], str):
                    datetime.fromisoformat(data['fecha_hora'])
            except ValueError:
                errors.append("La fecha y hora no tiene un formato válido")
        
        # Validar duración
        if data.get('duracion_minutos'):
            if not isinstance(data['duracion_minutos'], int) or data['duracion_minutos'] <= 0:
                errors.append("La duración debe ser un número entero positivo")
        
        # Validar tipo de cita
        valid_types = ['consulta_general', 'vacunacion', 'esterilizacion', 'urgencia', 'revision', 'cirugia']
        if data.get('tipo') and data['tipo'] not in valid_types:
            errors.append(f"El tipo de cita debe ser uno de: {', '.join(valid_types)}")
        
        # Validar estado
        valid_states = ['programada', 'confirmada', 'en_progreso', 'completada', 'cancelada', 'no_asistio']
        if data.get('estado') and data['estado'] not in valid_states:
            errors.append(f"El estado debe ser uno de: {', '.join(valid_states)}")
        
        if errors:
            raise ValidationError("; ".join(errors))

class HistorialValidator:
    """Validador para datos de historial clínico"""
    
    def __init__(self):
        self.settings = Settings()
    
    def validate_historial_data(self, data: Dict[str, Any], is_update: bool = False) -> None:
        """
        Valida los datos de un historial clínico
        
        Args:
            data: Datos del historial a validar
            is_update: Si es una actualización
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = []
        
        # Validar campos obligatorios
        required_fields = ['id_mascota', 'fecha', 'motivo_consulta']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"El campo '{field}' es obligatorio")
        
        # Validar ID de mascota
        if data.get('id_mascota') and not isinstance(data['id_mascota'], int):
            errors.append("El ID de la mascota debe ser un número entero")
        
        # Validar fecha
        if data.get('fecha'):
            if not isinstance(data['fecha'], date):
                errors.append("La fecha debe ser una fecha válida")
        
        # Validar motivo de consulta
        if data.get('motivo_consulta') and len(data['motivo_consulta'].strip()) < 5:
            errors.append("El motivo de consulta debe tener al menos 5 caracteres")
        
        # Validar peso
        if data.get('peso') is not None:
            try:
                peso = float(data['peso'])
                if peso <= 0 or peso > 999.99:
                    errors.append("El peso debe estar entre 0.01 y 999.99 kg")
            except (ValueError, TypeError):
                errors.append("El peso debe ser un número válido")
        
        # Validar tratamientos si existen
        if data.get('tratamientos'):
            if not isinstance(data['tratamientos'], list):
                errors.append("Los tratamientos deben ser una lista")
            else:
                for i, tratamiento in enumerate(data['tratamientos']):
                    if not isinstance(tratamiento, dict):
                        errors.append(f"El tratamiento {i+1} debe ser un diccionario")
                        continue
                    
                    if not tratamiento.get('nombre_tratamiento'):
                        errors.append(f"El tratamiento {i+1} debe tener un nombre")
                    
                    # Validar fechas del tratamiento
                    if tratamiento.get('fecha_inicio') and not isinstance(tratamiento['fecha_inicio'], date):
                        errors.append(f"La fecha de inicio del tratamiento {i+1} debe ser una fecha válida")
                    
                    if tratamiento.get('fecha_fin') and not isinstance(tratamiento['fecha_fin'], date):
                        errors.append(f"La fecha de fin del tratamiento {i+1} debe ser una fecha válida")
                    
                    # Validar que fecha_fin no sea anterior a fecha_inicio
                    if (tratamiento.get('fecha_inicio') and tratamiento.get('fecha_fin') and 
                        tratamiento['fecha_fin'] < tratamiento['fecha_inicio']):
                        errors.append(f"La fecha de fin del tratamiento {i+1} no puede ser anterior a la fecha de inicio")
        
        if errors:
            raise ValidationError("; ".join(errors))
    
    def validate_tratamiento_data(self, data: Dict[str, Any]) -> None:
        """
        Valida los datos de un tratamiento
        
        Args:
            data: Datos del tratamiento a validar
            
        Raises:
            ValidationError: Si los datos no son válidos
        """
        errors = []
        
        # Validar campos obligatorios
        if not data.get('nombre_tratamiento'):
            errors.append("El nombre del tratamiento es obligatorio")
        
        # Validar nombre del tratamiento
        if data.get('nombre_tratamiento') and len(data['nombre_tratamiento'].strip()) < 2:
            errors.append("El nombre del tratamiento debe tener al menos 2 caracteres")
        
        # Validar fechas
        if data.get('fecha_inicio') and not isinstance(data['fecha_inicio'], date):
            errors.append("La fecha de inicio debe ser una fecha válida")
        
        if data.get('fecha_fin') and not isinstance(data['fecha_fin'], date):
            errors.append("La fecha de fin debe ser una fecha válida")
        
        # Validar que fecha_fin no sea anterior a fecha_inicio
        if (data.get('fecha_inicio') and data.get('fecha_fin') and 
            data['fecha_fin'] < data['fecha_inicio']):
            errors.append("La fecha de fin no puede ser anterior a la fecha de inicio")
        
        if errors:
            raise ValidationError("; ".join(errors))
