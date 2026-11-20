from collections.abc import Sequence

from dependencies import LibroRepositoryDep
from models.biblioteca import Libro, LibroBase
from services.exceptions import (
    AutorNoEncontradoError,
    LibroIsbnDuplicadoError,
    LibroNoEncontradoError,
)


class LibroService:
    def __init__(self, repo: LibroRepositoryDep):
        self.repo = repo

    def get_libros(self, offset: int = 0, limit: int = 100) -> Sequence[Libro]:
        return self.repo.fetch_libros(offset, limit)

    def get_libro_by_id(self, libro_id: int) -> Libro | None:
        return self.repo.get_by_id(libro_id)

    def search_libros(self, titulo: str) -> Sequence[Libro]:
        return self.repo.search_by_title(titulo)

    def create_libro(self, datos: LibroBase) -> Libro:
        if self.repo.get_by_isbn(datos.isbn):
            raise LibroIsbnDuplicadoError()
        return self.repo.create_libro(Libro.model_validate(datos)
    )

    def update_libro(self, libro_id: int, datos: LibroBase) -> Libro:
        libro = self.get_libro_by_id(libro_id)

        if libro is None:
            raise LibroNoEncontradoError()
        otro = self.repo.get_by_isbn(datos.isbn)

        if otro and otro.id != libro_id:
            raise LibroIsbnDuplicadoError()
        return self.repo.update_libro(libro, datos)


    def delete_libro(self, libro_id: int) -> None:
        libro = self.get_libro_by_id(libro_id)
        if libro is None:
            raise LibroNoEncontradoError()
        self.repo.delete_libro(libro)

    def agregar_autor(self, libro_id: int, autor_id: int) -> Libro | None:
        libro = self.get_libro_by_id(libro_id)
        if libro is None:
            raise LibroNoEncontradoError()
        autor = self.repo.get_autor(autor_id)
        if autor is None:
            raise AutorNoEncontradoError()
        return self.repo.add_autor(libro, autor)
