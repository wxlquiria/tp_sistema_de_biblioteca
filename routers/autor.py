from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from dependencies import AutorServiceDep
from models.biblioteca import AutorBase
from routers.model.autor import AutorRequest, AutorResponse
from services.exceptions import AutorNoEncontradoError

router = APIRouter(prefix="/autores", tags=["Autores"])


@router.get("", response_model=list[AutorResponse])
def listar_autores(
    service: AutorServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return service.get_autores(offset, limit)


@router.get("/buscar", response_model=list[AutorResponse])
def buscar_autores(nombre: str, service: AutorServiceDep):
    return service.search_autores(nombre)


@router.get("/{autor_id}", response_model=AutorResponse)
def obtener_autor(autor_id: int, service: AutorServiceDep):
    autor = service.get_autor_by_id(autor_id)
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@router.post("", response_model=AutorResponse, status_code=201)
def crear_autor(req: AutorRequest, service: AutorServiceDep):
    return service.create_autor(AutorBase(**req.model_dump()))


@router.put("/{autor_id}", response_model=AutorResponse)
def actualizar_autor(autor_id: int, req: AutorRequest, service: AutorServiceDep):
    try:
        return service.update_autor(autor_id,AutorBase(**req.model_dump()))

    except AutorNoEncontradoError:
        raise HTTPException(status_code=404, detail="Autor no encontrado")


@router.delete("/{autor_id}", status_code=204)
def borrar_autor(autor_id: int, service: AutorServiceDep):
    try:
        service.delete_autor(autor_id)

    except AutorNoEncontradoError:
        raise HTTPException(status_code=404,detail="Autor no encontrado")
