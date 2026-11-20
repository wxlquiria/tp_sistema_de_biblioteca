# Regla 8: email duplicado -> 409
def test_email_duplicado_devuelve_409(client, crear_socio):
    crear_socio(email="ana@example.com")

    r = client.post("/socios", json={"nombre": "Otra Ana", "email": "ana@example.com"})

    assert r.status_code == 409


def test_actualizar_socio_con_email_de_otro_devuelve_409(client, crear_socio):
    crear_socio(email="a@example.com")
    socio_b = crear_socio(email="b@example.com")

    r = client.put(
        f"/socios/{socio_b['id']}",
        json={"nombre": "B", "email": "a@example.com", "activo": True},
    )

    assert r.status_code == 409


def test_email_invalido_devuelve_422(client):
    r = client.post("/socios", json={"nombre": "Ana", "email": "esto-no-es-un-email"})

    assert r.status_code == 422


def test_un_socio_nuevo_esta_activo_por_defecto(client):
    r = client.post("/socios", json={"nombre": "Ana", "email": "ana@example.com"})

    assert r.status_code == 201
    assert r.json()["activo"] is True


def test_desactivar_y_reactivar_socio(client, crear_socio):
    socio = crear_socio()

    r = client.patch(f"/socios/{socio['id']}/activo", params={"activo": False})
    assert r.json()["activo"] is False

    r = client.patch(f"/socios/{socio['id']}/activo", params={"activo": True})
    assert r.json()["activo"] is True


# Regla 7: recurso inexistente -> 404
def test_socio_inexistente_devuelve_404(client):
    assert client.get("/socios/999").status_code == 404