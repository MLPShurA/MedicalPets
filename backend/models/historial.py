from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal

@dataclass
class Tratamiento:
    """Modelo de datos para Tratamiento"""
    
    id: Optional[int] = None
    id_historial: Optional[int] = None
    nombre_tratamiento: str = ""
    dosis: str = ""
    frecuencia: str = ""
    duracion: str = ""
    observaciones: str = ""
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'id_historial': self.id_historial,
            'nombre_tratamiento': self.nombre_tratamiento,
            'dosis': self.dosis,
            'frecuencia': self.frecuencia,
            'duracion': self.duracion,
            'observaciones': self.observaciones,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tratamiento':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            id_historial=data.get('id_historial'),
            nombre_tratamiento=data.get('nombre_tratamiento', ''),
            dosis=data.get('dosis', ''),
            frecuencia=data.get('frecuencia', ''),
            duracion=data.get('duracion', ''),
            observaciones=data.get('observaciones', ''),
            fecha_inicio=date.fromisoformat(data['fecha_inicio']) if data.get('fecha_inicio') else None,
            fecha_fin=date.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None
        )

@dataclass
class HistorialClinico:
    """Modelo de datos para Historial Clínico"""
    
    id: Optional[int] = None
    id_mascota: Optional[int] = None
    fecha: Optional[date] = None
    motivo_consulta: str = ""
    sintomas: str = ""
    antecedentes: str = ""
    diagnostico: str = ""
    observaciones: str = ""
    peso: Optional[Decimal] = None
    
    # Campos relacionados
    mascota_nombre: str = ""
    mascota_raza: str = ""
    mascota_sexo: str = ""
    dueño_nombre: str = ""
    
    # Lista de tratamientos
    tratamientos: Optional[List[Tratamiento]] = None
    
    def __post_init__(self):
        """Inicializa la lista de tratamientos si es None"""
        if self.tratamientos is None:
            self.tratamientos = []
    
    @property
    def fecha_formateada(self) -> str:
        """Retorna la fecha formateada"""
        if self.fecha:
            return self.fecha.strftime("%d/%m/%Y")
        return ""
    
    @property
    def peso_formateado(self) -> str:
        """Retorna el peso formateado"""
        if self.peso:
            return f"{self.peso} kg"
        return "No registrado"
    
    @property
    def tiene_diagnostico(self) -> bool:
        """Verifica si tiene diagnóstico"""
        return bool(self.diagnostico.strip())
    
    @property
    def tiene_tratamientos(self) -> bool:
        """Verifica si tiene tratamientos"""
        return len(self.tratamientos or []) > 0
    
    @property
    def tiene_peso(self) -> bool:
        """Verifica si tiene peso registrado"""
        return self.peso is not None
    
    def agregar_tratamiento(self, tratamiento: Tratamiento):
        """Agrega un tratamiento al historial"""
        tratamiento.id_historial = self.id
        if self.tratamientos is None:
            self.tratamientos = []
        self.tratamientos.append(tratamiento)
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'id_mascota': self.id_mascota,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'fecha_formateada': self.fecha_formateada,
            'motivo_consulta': self.motivo_consulta,
            'sintomas': self.sintomas,
            'antecedentes': self.antecedentes,
            'diagnostico': self.diagnostico,
            'observaciones': self.observaciones,
            'peso': float(self.peso) if self.peso else None,
            'peso_formateado': self.peso_formateado,
            'mascota_nombre': self.mascota_nombre,
            'mascota_raza': self.mascota_raza,
            'mascota_sexo': self.mascota_sexo,
            'dueño_nombre': self.dueño_nombre,
            'tiene_diagnostico': self.tiene_diagnostico,
            'tiene_tratamientos': self.tiene_tratamientos,
            'tiene_peso': self.tiene_peso,
            'tratamientos': [t.to_dict() for t in (self.tratamientos or [])]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'HistorialClinico':
        """Crea una instancia desde un diccionario"""
        tratamientos = []
        if data.get('tratamientos'):
            tratamientos = [Tratamiento.from_dict(t) for t in data['tratamientos']]
        
        return cls(
            id=data.get('id'),
            id_mascota=data.get('id_mascota'),
            fecha=date.fromisoformat(data['fecha']) if data.get('fecha') else None,
            motivo_consulta=data.get('motivo_consulta', ''),
            sintomas=data.get('sintomas', ''),
            antecedentes=data.get('antecedentes', ''),
            diagnostico=data.get('diagnostico', ''),
            observaciones=data.get('observaciones', ''),
            peso=Decimal(str(data['peso'])) if data.get('peso') else None,
            mascota_nombre=data.get('mascota_nombre', ''),
            mascota_raza=data.get('mascota_raza', ''),
            mascota_sexo=data.get('mascota_sexo', ''),
            dueño_nombre=data.get('dueño_nombre', ''),
            tratamientos=tratamientos
        )
    
    def __str__(self) -> str:
        return f"HistorialClinico(id={self.id}, fecha='{self.fecha_formateada}', mascota='{self.mascota_nombre}')"
    
    def __repr__(self) -> str:
        return self.__str__()
