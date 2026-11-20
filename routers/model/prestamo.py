from datetime import date

from sqlmodel import SQLModel


# Para prestar solo hacen falta los ids; el resto lo calcula el service
class PrestamoRequest(SQLModel):
    socio_id: int
    libro_id: int


class PrestamoResponse(SQLModel):
    id: int
    socio_id: int
    libro_id: int
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: date | None = None
    multa: float