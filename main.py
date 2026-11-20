from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, select

from models.biblioteca import Autor, Libro, Socio
from repository import database
from repository.database import create_db_and_tables
from routers import autor, libro, prestamo, socio


def create_dummy_data():
    with Session(database.engine) as session:
        if session.exec(select(Libro)).first():
            return

        borges = Autor(nombre="Jorge Luis Borges", nacionalidad="Argentina")
        cortazar = Autor(nombre="Julio Cortázar", nacionalidad="Argentina")
        pizarnik = Autor(nombre="Alejandra Pizarnik", nacionalidad="Argentina")
        bioy = Autor(nombre="Adolfo Bioy Casares", nacionalidad="Argentina")
        session.add_all([borges, cortazar, pizarnik, bioy])
        session.commit()

        libros_demo = [
            Libro(titulo="Ficciones", isbn="DEMO-0001", stock=3, anio=1944, autores=[borges]),
            Libro(titulo="El Aleph", isbn= "DEMO-0002" , stock=2, anio=1949, autores=[borges]),
            Libro(titulo="Rayuela", isbn="DEMO-0003", stock=4, anio=1963, autores=[cortazar]),
            Libro(titulo="Bestiario", isbn="DEMO-0004", stock=1, anio=1951, autores=[cortazar]),
            Libro(
                titulo="Los trabajos y las noches",
                isbn="DEMO-0005",
                stock=2,
                anio=1965,
                autores=[pizarnik],
            ),
            # Un libro con dos autores (relación muchos a muchos)
            Libro(
                titulo="Seis problemas para don Isidro Parodi",
                isbn="DEMO-0006",
                stock=2,
                anio=1942,
                autores=[borges, bioy],
            ),
        ]
        session.add_all(libros_demo)

        socios_demo = [
            Socio(nombre="Martina Gómez", email="martina@example.com"),
            Socio(nombre="Santiago Fernández", email="santiago@example.com"),
            Socio(nombre="Valentina López", email="valentina@example.com"),
            Socio(nombre="Mateo Rodríguez", email="mateo@example.com", activo = False),
        ]
        session.add_all(socios_demo)
        session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  
    create_dummy_data()  
    yield


app = FastAPI(title="API de Biblioteca", lifespan=lifespan)

app.include_router(autor.router)
app.include_router(libro.router)
app.include_router(socio.router)
app.include_router(prestamo.router)





