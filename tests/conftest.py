import itertools
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from models.biblioteca import Prestamo
from repository.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """Una base de datos SQLite en memoria, nueva para cada test (no toca biblioteca.db)."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cliente de pruebas: la app usa la base en memoria en lugar de la real."""
    app.dependency_overrides[get_session] = lambda: session
    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------- Fábricas: crean datos por la API para no repetir código en los tests ----------

@pytest.fixture
def crear_autor(client):
    def _crear(nombre="Jorge Luis Borges", nacionalidad="Argentina"):
        r = client.post("/autores", json={"nombre": nombre, "nacionalidad": nacionalidad})
        assert r.status_code == 201
        return r.json()

    return _crear


@pytest.fixture
def crear_libro(client):
    contador = itertools.count(1)

    def _crear(isbn=None, titulo="Ficciones", stock=1):
        isbn = isbn or f"978-{next(contador)}"
        r = client.post(
            "/libros",
            json={"titulo": titulo, "isbn": isbn, "stock": stock, "anio": 1944},
        )
        assert r.status_code == 201
        return r.json()

    return _crear


@pytest.fixture
def crear_socio(client):
    contador = itertools.count(1)

    def _crear(email=None, activo=True, nombre="Ana"):
        email = email or f"socio{next(contador)}@example.com"
        r = client.post("/socios", json={"nombre": nombre, "email": email, "activo": activo})
        assert r.status_code == 201
        return r.json()

    return _crear


@pytest.fixture
def atrasar(session: Session):
    """Hace que un préstamo esté vencido hace N días (por API no se puede viajar en el tiempo)."""

    def _atrasar(prestamo_id: int, dias: int):
        prestamo = session.get(Prestamo, prestamo_id)

        if prestamo is None:
            raise ValueError(f"No se encontró ningún Prestamo con el ID {prestamo_id}")
        
        prestamo.fecha_vencimiento = date.today() - timedelta(days=dias)
        session.add(prestamo)
        session.commit()
               
        # 4. Refrescar el objeto para que Pytest vea los cambios actualizados
        session.refresh(prestamo)
        return prestamo

    return _atrasar


        