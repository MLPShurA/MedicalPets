from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import date
from decimal import Decimal

from ..models.historial import HistorialClinico, Tratamiento
from ..services.historial_service import HistorialService
from ..utils.exceptions import DatabaseError, ValidationError

router = APIRouter(prefix="/historiales", tags=["historiales"])

def get_historial_service():
    """Dependency para obtener el servicio de historiales"""
    return HistorialService()

@router.get("/", response_model=List[dict])
async def get_historiales(
    service: HistorialService = Depends(get_historial_service)
):
    """
    Obtiene todos los historiales clínicos
    """
    try:
        historiales = service.get_all_historiales()
        return [historial.to_dict() for historial in historiales]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/{historial_id}", response_model=dict)
async def get_historial(
    historial_id: int,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Obtiene un historial clínico por ID
    """
    try:
        historial = service.get_historial_by_id(historial_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")
        return historial.to_dict()
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/mascota/{mascota_id}", response_model=List[dict])
async def get_historiales_by_mascota(
    mascota_id: int,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Obtiene todos los historiales de una mascota
    """
    try:
        historiales = service.get_historiales_by_mascota(mascota_id)
        return [historial.to_dict() for historial in historiales]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/", response_model=dict)
async def create_historial(
    historial_data: dict,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Crea un nuevo historial clínico
    """
    try:
        # Convertir fechas si vienen como strings
        if 'fecha' in historial_data and isinstance(historial_data['fecha'], str):
            historial_data['fecha'] = date.fromisoformat(historial_data['fecha'])
        
        # Convertir peso si viene como string
        if 'peso' in historial_data and historial_data['peso'] is not None:
            if isinstance(historial_data['peso'], str):
                historial_data['peso'] = Decimal(historial_data['peso'])
            else:
                historial_data['peso'] = Decimal(str(historial_data['peso']))
        
        # Convertir fechas de tratamientos
        if 'tratamientos' in historial_data:
            for tratamiento in historial_data['tratamientos']:
                if 'fecha_inicio' in tratamiento and isinstance(tratamiento['fecha_inicio'], str):
                    tratamiento['fecha_inicio'] = date.fromisoformat(tratamiento['fecha_inicio'])
                if 'fecha_fin' in tratamiento and isinstance(tratamiento['fecha_fin'], str):
                    tratamiento['fecha_fin'] = date.fromisoformat(tratamiento['fecha_fin'])
        
        historial = service.create_historial(historial_data)
        return historial.to_dict()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/{historial_id}", response_model=dict)
async def update_historial(
    historial_id: int,
    historial_data: dict,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Actualiza un historial clínico
    """
    try:
        # Verificar que el historial existe
        existing_historial = service.get_historial_by_id(historial_id)
        if not existing_historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")
        
        # Convertir fechas si vienen como strings
        if 'fecha' in historial_data and isinstance(historial_data['fecha'], str):
            historial_data['fecha'] = date.fromisoformat(historial_data['fecha'])
        
        # Convertir peso si viene como string
        if 'peso' in historial_data and historial_data['peso'] is not None:
            if isinstance(historial_data['peso'], str):
                historial_data['peso'] = Decimal(historial_data['peso'])
            else:
                historial_data['peso'] = Decimal(str(historial_data['peso']))
        
        # Convertir fechas de tratamientos
        if 'tratamientos' in historial_data:
            for tratamiento in historial_data['tratamientos']:
                if 'fecha_inicio' in tratamiento and isinstance(tratamiento['fecha_inicio'], str):
                    tratamiento['fecha_inicio'] = date.fromisoformat(tratamiento['fecha_inicio'])
                if 'fecha_fin' in tratamiento and isinstance(tratamiento['fecha_fin'], str):
                    tratamiento['fecha_fin'] = date.fromisoformat(tratamiento['fecha_fin'])
        
        historial = service.update_historial(historial_id, historial_data)
        return historial.to_dict()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/{historial_id}")
async def delete_historial(
    historial_id: int,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Elimina un historial clínico
    """
    try:
        # Verificar que el historial existe
        existing_historial = service.get_historial_by_id(historial_id)
        if not existing_historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")
        
        success = service.delete_historial(historial_id)
        if success:
            return {"message": "Historial eliminado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error al eliminar el historial")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

# Endpoints adicionales para tratamientos

@router.get("/{historial_id}/tratamientos", response_model=List[dict])
async def get_tratamientos_by_historial(
    historial_id: int,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Obtiene todos los tratamientos de un historial
    """
    try:
        historial = service.get_historial_by_id(historial_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")
        
        return [tratamiento.to_dict() for tratamiento in historial.tratamientos]
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/{historial_id}/tratamientos", response_model=dict)
async def add_tratamiento_to_historial(
    historial_id: int,
    tratamiento_data: dict,
    service: HistorialService = Depends(get_historial_service)
):
    """
    Agrega un tratamiento a un historial existente
    """
    try:
        # Verificar que el historial existe
        historial = service.get_historial_by_id(historial_id)
        if not historial:
            raise HTTPException(status_code=404, detail="Historial no encontrado")
        
        # Convertir fechas si vienen como strings
        if 'fecha_inicio' in tratamiento_data and isinstance(tratamiento_data['fecha_inicio'], str):
            tratamiento_data['fecha_inicio'] = date.fromisoformat(tratamiento_data['fecha_inicio'])
        if 'fecha_fin' in tratamiento_data and isinstance(tratamiento_data['fecha_fin'], str):
            tratamiento_data['fecha_fin'] = date.fromisoformat(tratamiento_data['fecha_fin'])
        
        # Crear el tratamiento
        tratamiento = Tratamiento(
            id_historial=historial_id,
            nombre_tratamiento=tratamiento_data['nombre_tratamiento'],
            dosis=tratamiento_data.get('dosis', ''),
            frecuencia=tratamiento_data.get('frecuencia', ''),
            duracion=tratamiento_data.get('duracion', ''),
            observaciones=tratamiento_data.get('observaciones', ''),
            fecha_inicio=tratamiento_data.get('fecha_inicio'),
            fecha_fin=tratamiento_data.get('fecha_fin')
        )
        
        # Agregar el tratamiento al historial
        historial.agregar_tratamiento(tratamiento)
        
        # Actualizar el historial en la base de datos
        historial_dict = historial.to_dict()
        historial_dict['tratamientos'] = [t.to_dict() for t in historial.tratamientos]
        
        updated_historial = service.update_historial(historial_id, historial_dict)
        return updated_historial.to_dict()
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}") 