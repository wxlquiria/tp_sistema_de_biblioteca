def test_crear_y_obtener_autor(client, crear_autor):
    autor = crear_autor(nombre="Julio Cortázar", nacionalidad="Argentina")

    r = client.get(f"/autores/{autor['id']}")

    assert r.status_code == 200
    assert r.json()["nombre"] == "Julio Cortázar"


def test_buscar_autor_por_nombre(client, crear_autor):
    crear_autor(nombre="Julio Cortázar")
    crear_autor(nombre="Alejandra Pizarnik")

    r = client.get("/autores/buscar", params={"nombre": "Cort"})

    assert [a["nombre"] for a in r.json()] == ["Julio Cortázar"]


def test_autor_inexistente_devuelve_404(client):
    assert client.get("/autores/999").status_code == 404


def test_borrar_autor(client, crear_autor):
    autor = crear_autor()

    assert client.delete(f"/autores/{autor['id']}").status_code == 204
    assert client.get(f"/autores/{autor['id']}").status_code == 404