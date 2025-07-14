from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Usuario:
    """Modelo de datos para Usuario"""
    
    # Campos de la tabla usuarios
    id: Optional[int] = None
    nombre_usuario: str = ""
    contrasena: str = ""
    contrasena_hash: str = ""
    rol: str = "paciente"
    
    # Campos de la tabla usuarios_detalle
    detalle_id: Optional[int] = None
    nombres: str = ""
    apellidos: str = ""
    cedula: str = ""
    telefono: str = ""
    correo_electronico: str = ""
    direccion: str = ""
    
    # Campos calculados
    nombre_completo: str = ""
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicializa campos calculados después de la creación"""
        if self.nombres and self.apellidos:
            self.nombre_completo = f"{self.nombres} {self.apellidos}".strip()
    
    @property
    def es_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.rol == 'admin'
    
    @property
    def es_veterinario(self) -> bool:
        """Verifica si el usuario es veterinario"""
        return self.rol == 'veterinario'
    
    @property
    def es_doctor(self) -> bool:
        """Verifica si el usuario es doctor"""
        return self.rol == 'doctor'
    
    @property
    def es_secretaria(self) -> bool:
        """Verifica si el usuario es secretaria"""
        return self.rol == 'secretaria'
    
    @property
    def es_paciente(self) -> bool:
        """Verifica si el usuario es paciente"""
        return self.rol == 'paciente'
    
    def to_dict(self) -> dict:
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'rol': self.rol,
            'detalle_id': self.detalle_id,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'cedula': self.cedula,
            'telefono': self.telefono,
            'correo_electronico': self.correo_electronico,
            'direccion': self.direccion,
            'nombre_completo': self.nombre_completo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        """Crea una instancia desde un diccionario"""
        return cls(
            id=data.get('id'),
            nombre_usuario=data.get('nombre_usuario', ''),
            contrasena=data.get('contrasena', ''),
            contrasena_hash=data.get('contrasena_hash', ''),
            rol=data.get('rol', 'paciente'),
            detalle_id=data.get('detalle_id'),
            nombres=data.get('nombres', ''),
            apellidos=data.get('apellidos', ''),
            cedula=data.get('cedula', ''),
            telefono=data.get('telefono', ''),
            correo_electronico=data.get('correo_electronico', ''),
            direccion=data.get('direccion', ''),
            fecha_creacion=datetime.fromisoformat(data['fecha_creacion']) if data.get('fecha_creacion') else None,
            fecha_actualizacion=datetime.fromisoformat(data['fecha_actualizacion']) if data.get('fecha_actualizacion') else None
        )
    
    def __str__(self) -> str:
        return f"Usuario(id={self.id}, nombre='{self.nombre_completo}', rol='{self.rol}')"
    
    def __repr__(self) -> str:
        return self.__str__()
