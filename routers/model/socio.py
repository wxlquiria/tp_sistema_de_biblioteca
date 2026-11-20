from pydantic import EmailStr
from sqlmodel import SQLModel


class SocioRequest(SQLModel):
    nombre: str
    email: EmailStr
    activo: bool = True


class SocioResponse(SQLModel):
    id: int
    nombre: str
    email: str
    activo: bool