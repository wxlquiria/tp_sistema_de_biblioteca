from collections.abc import Sequence

from sqlmodel import select

from dependencies import SessionDep
from models.biblioteca import Socio, SocioBase


class SocioRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_socios(self, offset: int, limit: int) -> Sequence[Socio]:
        return self.session.exec(select(Socio).offset(offset).limit(limit)).all()

    def get_by_id(self, socio_id: int) -> Socio | None:
        return self.session.get(Socio, socio_id)

    def get_by_email(self, email: str) -> Socio | None:
        return self.session.exec(select(Socio).where(Socio.email == email)).first()

    def create_socio(self, socio: Socio) -> Socio:
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def update_socio(self, socio: Socio, datos: SocioBase) -> Socio:
        socio.sqlmodel_update(datos.model_dump())
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def set_activo(self, socio: Socio, activo: bool) -> Socio:
        socio.activo = activo
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def delete_socio(self, socio: Socio) -> None:
        self.session.delete(socio)
        self.session.commit()