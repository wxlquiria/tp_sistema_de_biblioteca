from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from dependencies import PrestamoServiceDep
from routers.model.prestamo import PrestamoRequest, PrestamoResponse
from services.exceptions import (
    LibroNoEncontradoError,
    LibroSinStockError,
    MaxPrestamosActivosError,
    PrestamoNoEncontradoError,
    PrestamoYaDevueltoError,
    SocioInactivoError,
    SocioNoEncontradoError,
)

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])

@router.get("", response_model=list[PrestamoResponse])
def listar_prestamos(
    service: PrestamoServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return service.get_prestamos(offset, limit)


@router.get("/vencidos", response_model=list[PrestamoResponse])
def listar_vencidos(service: PrestamoServiceDep):
    return service.get_vencidos()


@router.get("/{prestamo_id}", response_model=PrestamoResponse)
def obtener_prestamo(prestamo_id: int, service: PrestamoServiceDep):
    try:
        prestamo = service.get_prestamo_by_id(prestamo_id)

        if prestamo is None:
            raise PrestamoNoEncontradoError()
        return prestamo

    except PrestamoNoEncontradoError:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
@router.post("", response_model=PrestamoResponse, status_code=201)
def prestar_libro(req: PrestamoRequest, service: PrestamoServiceDep):
    try:
        return service.prestar_libro(req.socio_id, req.libro_id)

    except SocioNoEncontradoError:
            raise HTTPException(status_code=404, detail="Socio no encontrado")

    except SocioInactivoError: 
        raise HTTPException(status_code=403,detail="El socio no está activo")
    
    except MaxPrestamosActivosError:
        raise HTTPException(status_code=409, detail="El socio alcanzó el máximo de préstamos activos")

    except LibroNoEncontradoError:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    except LibroSinStockError:
        raise HTTPException(status_code=409, detail="No hay stock disponible de este libro")
    

@router.post("/{prestamo_id}/devolucion", response_model=PrestamoResponse)
def devolver_libro(prestamo_id: int, service: PrestamoServiceDep):
    try:
        return service.devolver_libro(prestamo_id)
    except PrestamoNoEncontradoError:
        raise HTTPException(status_code=404,detail="Préstamo no encontrado")

    except PrestamoYaDevueltoError:
        raise HTTPException(status_code=409,detail="Este préstamo ya fue devuelto")

    except LibroNoEncontradoError:
        raise HTTPException(status_code=404,detail="Libro no encontrado")