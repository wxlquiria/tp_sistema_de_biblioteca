from collections.abc import Sequence

from sqlmodel import col, select

from dependencies import SessionDep
from models.biblioteca import Autor, AutorBase


class AutorRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_autores(self, offset: int, limit: int) -> Sequence[Autor]:
        return self.session.exec(select(Autor).offset(offset).limit(limit)).all()

    def get_by_id(self, autor_id: int) -> Autor | None:
        return self.session.get(Autor, autor_id)

    def search_by_name(self, nombre: str) -> Sequence[Autor]:
        consulta = select(Autor).where(col(Autor.nombre).contains(nombre))
        return self.session.exec(consulta).all()

    def create_autor(self, autor: Autor) -> Autor:
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def update_autor(self, autor: Autor, datos: AutorBase) -> Autor:
        autor.sqlmodel_update(datos.model_dump())
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def delete_autor(self, autor: Autor) -> None:
        self.session.delete(autor)
        self.session.commit()