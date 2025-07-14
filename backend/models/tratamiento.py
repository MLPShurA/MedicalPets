from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoTratamiento(Enum):
    """Estados posibles de un tratamiento"""
    PRESCRITO = "prescrito"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    SUSPENDIDO = "suspendido"
    CANCELADO = "cancelado"

class TipoTratamiento(Enum):
    """Tipos de tratamiento"""
    MEDICAMENTO = "medicamento"
    TERAPIA = "terapia"
    CIRUGIA = "cirugia"
    VACUNA = "vacuna"
    DIETA = "dieta"
    EJERCICIO = "ejercicio"
    OTRO = "otro"

@dataclass
class Tratamiento:
    """Modelo de datos para Tratamiento"""
    
    id: Optional[int] = None
    nombre: str = ""
    tipo: str = TipoTratamiento.MEDICAMENTO.value
    descripcion: str = ""
    dosis: str = ""
    frecuencia: str = ""
    duracion_dias: int = 0
    estado: str = EstadoTratamiento.PRESCRITO.value
    
    # Fechas
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    # Relaciones
    id_mascota: Optional[int] = None
    id_veterinario: Optional[int] = None
    id_historial: Optional[int] = None
    
    # Campos relacionados
    mascota_nombre: str = ""
    veterinario_nombre: str = ""
    
    # Campos adicionales
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    observaciones: str = ""
    costo: float = 0.0
    
    @property
    def fecha_inicio_formateada(self) -> str:
        """Retorna la fecha de inicio formateada"""
        if self.fecha_inicio:
            return self.fecha_inicio.strftime("%d/%m/%Y")
        return ""
    
    @property
    def fecha_fin_formateada(self) -> str:
        """Retorna la fecha de fin formateada"""
        if self.fecha_fin:
            return self.fecha_fin.strftime("%d/%m/%Y")
        return ""
    
    @property
    def es_medicamento(self) -> bool:
        """Verifica si es un medicamento"""
        return self.tipo == TipoTratamiento.MEDICAMENTO.value
    
    @property
    def es_terapia(self) -> bool:
        """Verifica si es una terapia"""
        return self.tipo == TipoTratamiento.TERAPIA.value
    
    @property
    def es_cirugia(self) -> bool:
        """Verifica si es una cirugía"""
        return self.tipo == TipoTratamiento.CIRUGIA.value
    
    @property
    def es_vacuna(self) -> bool:
        """Verifica si es una vacuna"""
        return self.tipo == TipoTratamiento.VACUNA.value
    
    @property
    def es_prescrito(self) -> bool:
        """Verifica si está prescrito"""
        return self.estado == EstadoTratamiento.PRESCRITO.value
    
    @property
    def es_en_progreso(self) -> bool:
        """Verifica si está en progreso"""
        return self.estado == EstadoTratamiento.EN_PROGRESO.value
    
    @property
    def es_completado(self) -> bool:
        """Verifica si está completado"""
        return self.estado == EstadoTratamiento.COMPLETADO.value
    
    @property
    def es_suspendido(self) -> bool:
        """Verifica si está suspendido"""
        return self.estado == EstadoTratamiento.SUSPENDIDO.value
    
    @property
    def puede_iniciar(self) -> bool:
        """Verifica si se puede iniciar el tratamiento"""
        return self.estado == EstadoTratamiento.PRESCRITO.value
    
    @property
    def puede_completar(self) -> bool:
        """Verifica si se puede completar el tratamiento"""
        return self.estado in [
            EstadoTratamiento.PRESCRITO.value,
            EstadoTratamiento.EN_PROGRESO.value
        ]
    
    @property
    def puede_suspender(self) -> bool:
        """Verifica si se puede suspender el tratamiento"""
        return self.estado in [
            EstadoTratamiento.PRESCRITO.value,
            EstadoTratamiento.EN_PROGRESO.value
        ]
    
    @property
    def duracion_formateada(self) -> str:
        """Retorna la duración formateada"""
        if self.duracion_dias == 1:
            return "1 día"
        elif self.duracion_dias > 1:
            return f"{self.duracion_dias} días"
        else:
            return "Sin duración específica"
    
    @property
    def costo_formateado(self) -> str:
        """Retorna el costo formateado"""
        return f"${self.costo:.2f}"
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'dosis': self.dosis,
            'frecuencia': self.frecuencia,
            'duracion_dias': self.duracion_dias,
            'duracion_formateada': self.duracion_formateada,
            'estado': self.estado,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'fecha_inicio_formateada': self.fecha_inicio_formateada,
            'fecha_fin_formateada': self.fecha_fin_formateada,
            'id_mascota': self.id_mascota,
            'id_veterinario': self.id_veterinario,
            'id_historial': self.id_historial,
            'mascota_nombre': self.mascota_nombre,
            'veterinario_nombre': self.veterinario_nombre,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'observaciones': self.observaciones,
            'costo': self.costo,
            'costo_formateado': self.costo_formateado,
            'puede_iniciar': self.puede_iniciar,
            'puede_completar': self.puede_completar,
            'puede_suspender': self.puede_suspender
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tratamiento':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            tipo=data.get('tipo', TipoTratamiento.MEDICAMENTO.value),
            descripcion=data.get('descripcion', ''),
            dosis=data.get('dosis', ''),
            frecuencia=data.get('frecuencia', ''),
            duracion_dias=data.get('duracion_dias', 0),
            estado=data.get('estado', EstadoTratamiento.PRESCRITO.value),
            fecha_inicio=datetime.fromisoformat(data['fecha_inicio']) if data.get('fecha_inicio') else None,
            fecha_fin=datetime.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None,
            id_mascota=data.get('id_mascota'),
            id_veterinario=data.get('id_veterinario'),
            id_historial=data.get('id_historial'),
            mascota_nombre=data.get('mascota_nombre', ''),
            veterinario_nombre=data.get('veterinario_nombre', ''),
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None,
            fecha_actualizacion=datetime.fromisoformat(data['fecha_actualizacion']) if data.get('fecha_actualizacion') else None,
            observaciones=data.get('observaciones', ''),
            costo=data.get('costo', 0.0)
        )
    
    def __str__(self) -> str:
        return f"Tratamiento(id={self.id}, nombre='{self.nombre}', mascota='{self.mascota_nombre}', estado='{self.estado}')"
    
    def __repr__(self) -> str:
        return self.__str__()
