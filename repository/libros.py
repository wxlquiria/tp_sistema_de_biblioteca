from collections.abc import Sequence

from sqlmodel import col, select

from dependencies import SessionDep
from models.biblioteca import Autor, Libro, LibroBase


class LibroRepository:

    def __init__(self, session: SessionDep):
        self.session = session

    def fetch_libros(self, offset: int, limit: int) -> Sequence[Libro]:
        return self.session.exec(select(Libro).offset(offset).limit(limit)).all()

    def get_by_id(self, libro_id: int) -> Libro | None:
        return self.session.get(Libro, libro_id)

    def get_by_isbn(self, isbn: str) -> Libro | None:
        return self.session.exec(select(Libro).where(Libro.isbn == isbn)).first()

    def search_by_title(self, titulo: str) -> Sequence[Libro]:
        consulta = select(Libro).where(col(Libro.titulo).contains(titulo))
        return self.session.exec(consulta).all()

    def create_libro(self, libro: Libro) -> Libro:
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def update_libro(self, libro: Libro, datos: LibroBase) -> Libro:
        libro.sqlmodel_update(datos.model_dump())
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

    def delete_libro(self, libro: Libro) -> None:
        self.session.delete(libro)
        self.session.commit()

    def get_autor(self, autor_id: int) -> Autor | None:
        return self.session.get(Autor, autor_id)

    def add_autor(self, libro: Libro, autor: Autor) -> Libro:
        if autor not in libro.autores:
            libro.autores.append(autor) 
            self.session.add(libro)
            self.session.commit()
            self.session.refresh(libro)
        return libro

    

        



