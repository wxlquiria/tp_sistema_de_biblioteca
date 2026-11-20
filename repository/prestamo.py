from collections.abc import Sequence
from datetime import date

from sqlmodel import col, func, select

from dependencies import SessionDep
from models.biblioteca import Libro, Prestamo


class PrestamoRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_prestamos(self, offset: int, limit: int) -> Sequence[Prestamo]:
        return self.session.exec(select(Prestamo).offset(offset).limit(limit)).all()

    def get_by_id(self, prestamo_id: int) -> Prestamo | None:
        return self.session.get(Prestamo, prestamo_id)

    def count_activos_by_socio(self, socio_id: int) -> int:
        consulta = (
            select(func.count())
            .select_from(Prestamo)
            .where(Prestamo.socio_id == socio_id, col(Prestamo.fecha_devolucion).is_(None))
        )
        return self.session.exec(consulta).one()

    def fetch_vencidos(self, hoy: date) -> Sequence[Prestamo]:
        consulta = select(Prestamo).where(
            col(Prestamo.fecha_devolucion).is_(None),
            Prestamo.fecha_vencimiento < hoy,
        )
        return self.session.exec(consulta).all()

    def registrar_prestamo(self, prestamo: Prestamo, libro: Libro) -> Prestamo:
        libro.stock -= 1
        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo

    def registrar_devolucion(
        self, prestamo: Prestamo, libro: Libro, fecha: date, multa: float
    ) -> Prestamo:
        prestamo.fecha_devolucion = fecha
        prestamo.multa = multa
        libro.stock += 1
        self.session.add(prestamo)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo