from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from repository.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

from repository.autor import AutorRepository  # noqa: E402
from repository.libros import LibroRepository  # noqa: E402
from repository.prestamo import PrestamoRepository  # noqa: E402
from repository.socio import SocioRepository  # noqa: E402

AutorRepositoryDep = Annotated[AutorRepository, Depends(AutorRepository)]
LibroRepositoryDep = Annotated[LibroRepository, Depends(LibroRepository)]
SocioRepositoryDep = Annotated[SocioRepository, Depends(SocioRepository)]
PrestamoRepositoryDep = Annotated[PrestamoRepository, Depends(PrestamoRepository)]

from services.autor_service import AutorService  # noqa: E402
from services.libro_service import LibroService  # noqa: E402
from services.prestamo_service import PrestamoService  # noqa: E402
from services.socio_service import SocioService  # noqa: E402

AutorServiceDep = Annotated[AutorService, Depends(AutorService)]
LibroServiceDep = Annotated[LibroService, Depends(LibroService)]
SocioServiceDep = Annotated[SocioService, Depends(SocioService)]
PrestamoServiceDep = Annotated[PrestamoService, Depends(PrestamoService)]