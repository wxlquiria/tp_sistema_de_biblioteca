from sqlmodel import Field, SQLModel

from routers.model.autor import AutorResponse


class LibroRequest(SQLModel):
    titulo: str
    isbn: str
    stock: int = Field(ge=0)
    anio: int


class LibroResponse(SQLModel):
    id: int
    titulo: str
    isbn: str
    stock: int
    anio: int


class LibroConAutoresResponse(LibroResponse):
    autores: list[AutorResponse] = []