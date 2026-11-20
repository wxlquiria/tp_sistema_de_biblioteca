from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from dependencies import SocioServiceDep
from models.biblioteca import SocioBase
from routers.model.socio import SocioRequest, SocioResponse
from services.exceptions import (
    EmailDuplicadoError,
    SocioNoEncontradoError,
)

router = APIRouter(prefix="/socios", tags=["Socios"])


@router.get("", response_model=list[SocioResponse])
def listar_socios(service: SocioServiceDep,offset: int = 0,limit: Annotated[int, Query(le=100)] = 100):
    return service.get_socios(offset, limit)


@router.get("/{socio_id}", response_model=SocioResponse)
def obtener_socio(socio_id: int, service: SocioServiceDep):
    socio = service.get_socio_by_id(socio_id)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    return socio


@router.post("", response_model=SocioResponse, status_code=201)
def crear_socio(req: SocioRequest, service: SocioServiceDep):
    try:
        return service.create_socio(SocioBase(**req.model_dump()))
    except EmailDuplicadoError:
        raise HTTPException(status_code=409, detail="Ya existe un socio con ese email")
    
@router.put("/{socio_id}", response_model=SocioResponse)
def actualizar_socio(socio_id: int, req: SocioRequest, service: SocioServiceDep):
    try: 
        return service.update_socio(socio_id, SocioBase(**req.model_dump()))
    except SocioNoEncontradoError:
        raise HTTPException(status_code=404,detail="Socio no encontrado")

    except EmailDuplicadoError:
        raise HTTPException(status_code=409, detail="Ya existe un socio con ese email")


@router.patch("/{socio_id}/activo", response_model=SocioResponse)
def cambiar_estado_socio(socio_id: int, activo: bool, service: SocioServiceDep):
    try:
        return service.set_activo(socio_id, activo)
    except SocioNoEncontradoError:
        raise HTTPException(status_code=404,detail="Socio no encontrado")


@router.delete("/{socio_id}", status_code=204)
def borrar_socio(socio_id: int, service: SocioServiceDep):
    try:
        service.delete_socio(socio_id)
    except SocioNoEncontradoError:
        raise HTTPException(status_code=404,detail="Socio no encontrado",)