from sqlmodel import SQLModel


# Nivel API: lo que entra y lo que sale por los endpoints de autores
class AutorRequest(SQLModel):
    nombre: str
    nacionalidad: str


class AutorResponse(SQLModel):
    id: int
    nombre: str
    nacionalidad: str