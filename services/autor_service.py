from collections.abc import Sequence

from dependencies import AutorRepositoryDep
from models.biblioteca import Autor, AutorBase
from services.exceptions import AutorNoEncontradoError


class AutorService():
    def __init__(self, repo: AutorRepositoryDep):
        self.repo = repo

    def get_autores(self, offset: int = 0, limit: int = 100) -> Sequence[Autor]:
        return self.repo.fetch_autores(offset, limit)

    def get_autor_by_id(self, autor_id: int) -> Autor | None:
        return self.repo.get_by_id(autor_id)

    def search_autores(self, nombre: str) -> Sequence[Autor] | None:
        return self.repo.search_by_name(nombre)

    def create_autor(self, datos: AutorBase) -> Autor:
        return self.repo.create_autor(Autor.model_validate(datos))

    def update_autor(self, autor_id: int, datos: AutorBase) -> Autor | None:
        autor = self.repo.get_by_id(autor_id)
        if autor is None:
            raise AutorNoEncontradoError()
        return self.repo.update_autor(autor, datos)

    def delete_autor(self, autor_id: int) -> None:
        autor = self.repo.get_by_id(autor_id)
        if autor is None:
            raise AutorNoEncontradoError()
        self.repo.delete_autor(autor)