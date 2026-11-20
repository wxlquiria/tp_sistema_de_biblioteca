from collections.abc import Sequence
from datetime import date, timedelta

from dependencies import LibroRepositoryDep, PrestamoRepositoryDep, SocioRepositoryDep
from models.biblioteca import Prestamo
from services.exceptions import (
    LibroNoEncontradoError,
    LibroSinStockError,
    MaxPrestamosActivosError,
    PrestamoNoEncontradoError,
    PrestamoYaDevueltoError,
    SocioInactivoError,
    SocioNoEncontradoError,
)

DIAS_PRESTAMO = 14
MULTA_POR_DIA = 100.0
MAX_PRESTAMOS_ACTIVOS = 3


class PrestamoService:
    def __init__(self, repo: PrestamoRepositoryDep, libro_repo: LibroRepositoryDep,socio_repo: SocioRepositoryDep):
        self.repo = repo
        self.libro_repo = libro_repo
        self.socio_repo = socio_repo

    def get_prestamos(self, offset: int = 0, limit: int = 100) -> Sequence[Prestamo]:
        return self.repo.fetch_prestamos(offset, limit)

    def get_prestamo_by_id(self, prestamo_id: int) -> Prestamo | None:
        prestamo = self.repo.get_by_id(prestamo_id)
        if prestamo is None:
            return None
        return prestamo

    def get_vencidos(self) -> Sequence[Prestamo]:
        return self.repo.fetch_vencidos(date.today())

    def prestar_libro(self, socio_id: int, libro_id: int) -> Prestamo | None:
        socio = self.socio_repo.get_by_id(socio_id)

        if socio is None:
            raise SocioNoEncontradoError()
        if not socio.activo:
            raise SocioInactivoError()
        if self.repo.count_activos_by_socio(socio_id) >= MAX_PRESTAMOS_ACTIVOS:
            raise MaxPrestamosActivosError()
        
        libro = self.libro_repo.get_by_id(libro_id)
        if libro is None:
            raise LibroNoEncontradoError()
        if libro.stock <= 0:
            raise LibroSinStockError()
        
        hoy = date.today()
        prestamo = Prestamo(socio_id=socio_id,libro_id=libro_id,fecha_prestamo=hoy,fecha_vencimiento=hoy + timedelta(days=DIAS_PRESTAMO))  # noqa: E501
        return self.repo.registrar_prestamo(prestamo, libro)

    def devolver_libro(self, prestamo_id: int) -> Prestamo | None:
        prestamo = self.get_prestamo_by_id(prestamo_id)

        if prestamo is None:
            raise PrestamoNoEncontradoError()

        if prestamo.fecha_devolucion is not None:
            raise PrestamoYaDevueltoError()

        libro = self.libro_repo.get_by_id(prestamo.libro_id)
        if libro is None:
            raise LibroNoEncontradoError()
        hoy = date.today()
        dias_atraso = max(0, (hoy - prestamo.fecha_vencimiento).days)
        multa = dias_atraso * MULTA_POR_DIA
        return self.repo.registrar_devolucion(prestamo, libro, hoy, multa)
