from datetime import date

from pydantic.networks import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Tabla intermedia entre Libro y Autor)
class LibroAutor(SQLModel, table=True):
    libro_id: int | None = Field(default=None, foreign_key="libro.id", primary_key=True)
    autor_id: int | None = Field(default=None, foreign_key="autor.id", primary_key=True)


# ---------- Autor ----------
class AutorBase(SQLModel):
    nombre: str = Field(index=True)
    nacionalidad: str

class Autor(AutorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    libros: list["Libro"] = Relationship(back_populates="autores", link_model=LibroAutor)


# ---------- Libro ----------
class LibroBase(SQLModel):
    titulo: str = Field(index=True)
    isbn: str = Field(unique=True, index=True)
    stock: int = Field(ge=0)
    anio: int


class Libro(LibroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    autores: list[Autor] = Relationship(back_populates="libros", link_model=LibroAutor)
    prestamos: list["Prestamo"] = Relationship(back_populates="libro")


# ---------- Socio ----------
class SocioBase(SQLModel):
    nombre: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    activo: bool = True


class Socio(SocioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    prestamos: list["Prestamo"] = Relationship(back_populates="socio")


# ---------- Préstamo ----------
class PrestamoBase(SQLModel):
    socio_id: int = Field(foreign_key="socio.id")
    libro_id: int = Field(foreign_key="libro.id")
    fecha_prestamo: date = Field(default_factory=date.today)
    fecha_vencimiento: date
    fecha_devolucion: date | None = None  
    multa: float = Field(default=0, ge=0)


class Prestamo(PrestamoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    socio: Socio | None = Relationship(back_populates="prestamos")
    libro: Libro | None = Relationship(back_populates="prestamos")