from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Mascota:
    """Modelo de datos para Mascota"""
    
    id: Optional[int] = None
    nombre: str = ""
    sexo: str = "Macho"  # Macho, Hembra
    edad: int = 0  # Edad en meses
    raza: str = ""
    id_dueño: Optional[int] = None
    
    # Campos relacionados
    dueño_nombre: str = ""
    dueño_apellidos: str = ""
    
    # Campos adicionales
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    estado: str = "activo"  # activo, inactivo, fallecido
    
    @property
    def edad_anos(self) -> int:
        """Retorna la edad en años"""
        return self.edad // 12
    
    @property
    def edad_meses(self) -> int:
        """Retorna la edad en meses (resto)"""
        return self.edad % 12
    
    @property
    def edad_formateada(self) -> str:
        """Retorna la edad formateada como string"""
        if self.edad_anos > 0:
            if self.edad_meses > 0:
                return f"{self.edad_anos} año{'s' if self.edad_anos != 1 else ''} y {self.edad_meses} mes{'es' if self.edad_meses != 1 else ''}"
            else:
                return f"{self.edad_anos} año{'s' if self.edad_anos != 1 else ''}"
        else:
            return f"{self.edad_meses} mes{'es' if self.edad_meses != 1 else ''}"
    
    @property
    def es_macho(self) -> bool:
        """Verifica si la mascota es macho"""
        return self.sexo.lower() == "macho"
    
    @property
    def es_hembra(self) -> bool:
        """Verifica si la mascota es hembra"""
        return self.sexo.lower() == "hembra"
    
    @property
    def nombre_completo_dueño(self) -> str:
        """Retorna el nombre completo del dueño"""
        if self.dueño_nombre and self.dueño_apellidos:
            return f"{self.dueño_nombre} {self.dueño_apellidos}".strip()
        return self.dueño_nombre or self.dueño_apellidos or ""
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'sexo': self.sexo,
            'edad': self.edad,
            'edad_anos': self.edad_anos,
            'edad_meses': self.edad_meses,
            'edad_formateada': self.edad_formateada,
            'raza': self.raza,
            'id_dueño': self.id_dueño,
            'dueño_nombre': self.dueño_nombre,
            'dueño_apellidos': self.dueño_apellidos,
            'nombre_completo_dueño': self.nombre_completo_dueño,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'estado': self.estado
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Mascota':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre', ''),
            sexo=data.get('sexo', 'Macho'),
            edad=data.get('edad', 0),
            raza=data.get('raza', ''),
            id_dueño=data.get('id_dueño'),
            dueño_nombre=data.get('dueño_nombre', ''),
            dueño_apellidos=data.get('dueño_apellidos', ''),
            fecha_registro=datetime.fromisoformat(data['fecha_registro']) if data.get('fecha_registro') else None,
            fecha_actualizacion=datetime.fromisoformat(data['fecha_actualizacion']) if data.get('fecha_actualizacion') else None,
            estado=data.get('estado', 'activo')
        )
    
    def __str__(self) -> str:
        return f"Mascota(id={self.id}, nombre='{self.nombre}', raza='{self.raza}', edad='{self.edad_formateada}')"
    
    def __repr__(self) -> str:
        return self.__str__()
