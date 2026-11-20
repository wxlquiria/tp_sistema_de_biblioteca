from collections.abc import Sequence

from dependencies import SocioRepositoryDep
from models.biblioteca import Socio, SocioBase
from services.exceptions import (
    EmailDuplicadoError,
    SocioNoEncontradoError,
)


class SocioService:
    def __init__(self, repo: SocioRepositoryDep):
        self.repo = repo

    def get_socios(self, offset: int = 0, limit: int = 100,) -> Sequence[Socio]:
        return self.repo.fetch_socios(offset, limit)

    def get_socio_by_id(self, socio_id: int) -> Socio | None:
        return self.repo.get_by_id(socio_id)

    def create_socio(self, datos: SocioBase) -> Socio:
        if self.repo.get_by_email(datos.email):
            raise EmailDuplicadoError()

        return self.repo.create_socio(Socio.model_validate(datos))

    def update_socio(self, socio_id: int, datos: SocioBase,) -> Socio:

        socio = self.get_socio_by_id(socio_id)

        if socio is None:
            raise SocioNoEncontradoError()

        otro = self.repo.get_by_email(datos.email)

        if otro and otro.id != socio_id:
            raise EmailDuplicadoError()

        return self.repo.update_socio(socio, datos)

    def set_activo(self, socio_id: int, activo: bool) -> Socio:
        socio = self.get_socio_by_id(socio_id)
        if socio is None:
            raise SocioNoEncontradoError()
        return self.repo.set_activo(socio, activo)

    def delete_socio(self, socio_id: int) -> None:
        socio = self.get_socio_by_id(socio_id)
        if socio is None:
            raise SocioNoEncontradoError()
        self.repo.delete_socio(socio)
