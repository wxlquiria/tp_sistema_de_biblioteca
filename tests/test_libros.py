def test_crear_libro(client, crear_libro):
    libro = crear_libro(titulo="Ficciones", stock=3)

    assert libro["titulo"] == "Ficciones"
    assert libro["stock"] == 3
    assert "id" in libro


def test_isbn_duplicado_devuelve_409(client, crear_libro):
    crear_libro(isbn="978-DUP")

    r = client.post(
        "/libros",
        json={"titulo": "Otro", "isbn": "978-DUP", "stock": 1, "anio": 2000},
    )

    assert r.status_code == 409


def test_actualizar_libro_con_isbn_de_otro_devuelve_409(client, crear_libro):
    crear_libro(isbn="978-A")
    libro_b = crear_libro(isbn="978-B")

    r = client.put(
        f"/libros/{libro_b['id']}",
        json={"titulo": "B", "isbn": "978-A", "stock": 1, "anio": 2000},
    )

    assert r.status_code == 409


def test_actualizar_libro_conservando_su_isbn_es_valido(client, crear_libro):
    libro = crear_libro(isbn="978-A")

    r = client.put(
        f"/libros/{libro['id']}",
        json={"titulo": "Nuevo título", "isbn": "978-A", "stock": 5, "anio": 2000},
    )

    assert r.status_code == 200
    assert r.json()["titulo"] == "Nuevo título"


def test_stock_negativo_devuelve_422(client):
    r = client.post(
        "/libros",
        json={"titulo": "X", "isbn": "978-X", "stock": -1, "anio": 2000},
    )

    assert r.status_code == 422


def test_libro_inexistente_devuelve_404(client):
    assert client.get("/libros/999").status_code == 404


def test_buscar_libro_por_titulo(client, crear_libro):
    crear_libro(titulo="Ficciones")
    crear_libro(titulo="El Aleph")

    r = client.get("/libros/buscar", params={"titulo": "Aleph"})

    assert [x["titulo"] for x in r.json()] == ["El Aleph"]


def test_libro_devuelve_sus_autores(client, crear_libro, crear_autor):
    libro = crear_libro()
    autor = crear_autor()

    r = client.post(f"/libros/{libro['id']}/autores/{autor['id']}")
    assert r.status_code == 200
    assert [a["nombre"] for a in r.json()["autores"]] == [autor["nombre"]]

    r = client.get(f"/libros/{libro['id']}")
    assert r.json()["autores"][0]["id"] == autor["id"]


def test_agregar_autor_inexistente_devuelve_404(client, crear_libro):
    libro = crear_libro()

    assert client.post(f"/libros/{libro['id']}/autores/999").status_code == 404


def test_borrar_libro(client, crear_libro):
    libro = crear_libro()

    assert client.delete(f"/libros/{libro['id']}").status_code == 204
    assert client.get(f"/libros/{libro['id']}").status_code == 404