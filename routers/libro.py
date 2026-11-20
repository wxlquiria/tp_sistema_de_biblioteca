from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from dependencies import LibroServiceDep
from models.biblioteca import LibroBase
from routers.model.libro import LibroConAutoresResponse, LibroRequest, LibroResponse
from services.exceptions import (
    AutorNoEncontradoError,
    LibroIsbnDuplicadoError,
    LibroNoEncontradoError,
)

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.get("", response_model=list[LibroResponse])
def listar_libros(
    service: LibroServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    return service.get_libros(offset, limit)

@router.get("/buscar", response_model=list[LibroResponse])
def buscar_libros(titulo: str, service: LibroServiceDep):
    return service.search_libros(titulo)


@router.get("/{libro_id}", response_model=LibroConAutoresResponse)
def obtener_libro(libro_id: int, service: LibroServiceDep):
    libro = service.get_libro_by_id(libro_id)
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.post("", response_model=LibroResponse, status_code=201)
def crear_libro(req: LibroRequest, service: LibroServiceDep):
    try:
        return service.create_libro(LibroBase(**req.model_dump()))
    except LibroIsbnDuplicadoError:
        raise HTTPException(status_code=409,detail="Ya existe un libro con ese ISBN")



@router.put("/{libro_id}", response_model=LibroResponse)
def actualizar_libro(libro_id: int, req: LibroRequest, service: LibroServiceDep):
    try:
        return service.update_libro(libro_id,LibroBase(**req.model_dump()))

    except LibroNoEncontradoError:
        raise HTTPException(status_code=404,detail="Libro no encontrado")

    except LibroIsbnDuplicadoError:
        raise HTTPException(status_code=409,detail="Ya existe un libro con ese ISBN")


@router.delete("/{libro_id}", status_code=204)
def borrar_libro(libro_id: int, service: LibroServiceDep):
    try:
        service.delete_libro(libro_id)
    except LibroNoEncontradoError:
        raise HTTPException(status_code=404,detail="Libro no encontrado")


@router.post("/{libro_id}/autores/{autor_id}", response_model=LibroConAutoresResponse)
def agregar_autor_a_libro(libro_id: int, autor_id: int, service: LibroServiceDep):
    try:
        return service.agregar_autor(libro_id,autor_id,)
    except LibroNoEncontradoError:
        raise HTTPException(status_code=404,detail="Libro no encontrado")
    
    except AutorNoEncontradoError:
        raise HTTPException(status_code=404,)





    