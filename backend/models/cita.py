from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoCita(Enum):
    """Estados posibles de una cita"""
    PROGRAMADA = "programada"
    CONFIRMADA = "confirmada"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    NO_ASISTIO = "no_asistio"

class TipoCita(Enum):
    """Tipos de cita"""
    CONSULTA_GENERAL = "consulta_general"
    VACUNACION = "vacunacion"
    ESTERILIZACION = "esterilizacion"
    URGENCIA = "urgencia"
    REVISION = "revision"
    CIRUGIA = "cirugia"

@dataclass
class Cita:
    """Modelo de datos para Cita"""
    
    id: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    duracion_minutos: int = 30
    tipo: str = TipoCita.CONSULTA_GENERAL.value
    estado: str = EstadoCita.PROGRAMADA.value
    motivo: str = ""
    observaciones: str = ""
    
    # Relaciones
    id_mascota: Optional[int] = None
    id_veterinario: Optional[int] = None
    id_dueño: Optional[int] = None
    
    # Campos relacionados
    mascota_nombre: str = ""
    veterinario_nombre: str = ""
    dueño_nombre: str = ""
    
    # Campos adicionales
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    @property
    def es_programada(self) -> bool:
        """Verifica si la cita está programada"""
        return self.estado == EstadoCita.PROGRAMADA.value
    
    @property
    def es_confirmada(self) -> bool:
        """Verifica si la cita está confirmada"""
        return self.estado == EstadoCita.CONFIRMADA.value
    
    @property
    def es_completada(self) -> bool:
        """Verifica si la cita está completada"""
        return self.estado == EstadoCita.COMPLETADA.value
    
    @property
    def es_cancelada(self) -> bool:
        """Verifica si la cita está cancelada"""
        return self.estado == EstadoCita.CANCELADA.value
    
    @property
    def fecha_formateada(self) -> str:
        """Retorna la fecha formateada"""
        if self.fecha_hora:
            return self.fecha_hora.strftime("%d/%m/%Y %H:%M")
        return ""
    
    @property
    def hora_formateada(self) -> str:
        """Retorna solo la hora formateada"""
        if self.fecha_hora:
            return self.fecha_hora.strftime("%H:%M")
        return ""
    
    @property
    def fecha_solo(self) -> str:
        """Retorna solo la fecha formateada"""
        if self.fecha_hora:
            return self.fecha_hora.strftime("%d/%m/%Y")
        return ""
    
    @property
    def puede_cancelar(self) -> bool:
        """Verifica si la cita se puede cancelar"""
        return self.estado in [
            EstadoCita.PROGRAMADA.value,
            EstadoCita.CONFIRMADA.value
        ]
    
    @property
    def puede_confirmar(self) -> bool:
        """Verifica si la cita se puede confirmar"""
        return self.estado == EstadoCita.PROGRAMADA.value
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'fecha_formateada': self.fecha_formateada,
            'hora_formateada': self.hora_formateada,
            'fecha_solo': self.fecha_solo,
            'duracion_minutos': self.duracion_minutos,
            'tipo': self.tipo,
            'estado': self.estado,
            'motivo': self.motivo,
            'observaciones': self.observaciones,
            'id_mascota': self.id_mascota,
            'id_veterinario': self.id_veterinario,
            'id_dueño': self.id_dueño,
            'mascota_nombre': self.mascota_nombre,
            'veterinario_nombre': self.veterinario_nombre,
            'dueño_nombre': self.dueño_nombre,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'puede_cancelar': self.puede_cancelar,
            'puede_confirmar': self.puede_confirmar
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cita':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            fecha_hora=datetime.fromisoformat(data['fecha_hora']) if data.get('fecha_hora') else None,
            duracion_minutos=data.get('duracion_minutos', 30),
            tipo=data.get('tipo', TipoCita.CONSULTA_GENERAL.value),
            estado=data.get('estado', EstadoCita.PROGRAMADA.value),
            motivo=data.get('motivo', ''),
            observaciones=data.get('observaciones', ''),
            id_mascota=data.get('id_mascota'),
            id_veterinario=data.get('id_veterinario'),
            id_dueño=data.get('id_dueño'),
            mascota_nombre=data.get('mascota_nombre', ''),
            veterinario_nombre=data.get('veterinario_nombre', ''),
            dueño_nombre=data.get('dueño_nombre', ''),
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None,
            fecha_actualizacion=datetime.fromisoformat(data['fecha_actualizacion']) if data.get('fecha_actualizacion') else None
        )
    
    def __str__(self) -> str:
        return f"Cita(id={self.id}, fecha='{self.fecha_formateada}', mascota='{self.mascota_nombre}', estado='{self.estado}')"
    
    def __repr__(self) -> str:
        return self.__str__()
