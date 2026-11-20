from datetime import date, timedelta


def prestar(client, socio_id, libro_id):
    return client.post("/prestamos", json={"socio_id": socio_id, "libro_id": libro_id})


def stock_de(client, libro_id):
    return client.get(f"/libros/{libro_id}").json()["stock"]


def test_prestar_libro(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro(stock=2)

    r = prestar(client, socio["id"], libro["id"])

    assert r.status_code == 201
    prestamo = r.json()
    assert prestamo["socio_id"] == socio["id"]
    assert prestamo["libro_id"] == libro["id"]
    assert prestamo["fecha_devolucion"] is None
    assert prestamo["multa"] == 0


# Regla 1: un socio no puede tener más de 3 préstamos activos -> 409
def test_socio_no_puede_tener_mas_de_3_prestamos_activos(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro(stock=10)

    for _ in range(3):
        assert prestar(client, socio["id"], libro["id"]).status_code == 201

    assert prestar(client, socio["id"], libro["id"]).status_code == 409


def test_al_devolver_un_libro_el_socio_puede_pedir_otro(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro(stock=10)
    prestamos = [prestar(client, socio["id"], libro["id"]).json() for _ in range(3)]
    assert prestar(client, socio["id"], libro["id"]).status_code == 409

    client.post(f"/prestamos/{prestamos[0]['id']}/devolucion")

    assert prestar(client, socio["id"], libro["id"]).status_code == 201


# Regla 2: sin stock no se presta; al prestar se descuenta 1 -> 409
def test_al_prestar_se_descuenta_1_de_stock(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro(stock=2)

    prestar(client, socio["id"], libro["id"])

    assert stock_de(client, libro["id"]) == 1


def test_no_se_presta_un_libro_sin_stock(client, crear_socio, crear_libro):
    socio_1 = crear_socio()
    socio_2 = crear_socio()
    libro = crear_libro(stock=1)
    assert prestar(client, socio_1["id"], libro["id"]).status_code == 201

    r = prestar(client, socio_2["id"], libro["id"])

    assert r.status_code == 409
    assert stock_de(client, libro["id"]) == 0


# Regla 3: socio inactivo no puede pedir préstamos -> 403
def test_socio_inactivo_no_puede_pedir_prestamos(client, crear_socio, crear_libro):
    socio = crear_socio(activo=False)
    libro = crear_libro(stock=1)

    r = prestar(client, socio["id"], libro["id"])

    assert r.status_code == 403
    assert stock_de(client, libro["id"]) == 1  # no se descontó nada


# Regla 4: el plazo es de 14 días
def test_el_plazo_es_de_14_dias(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro()

    prestamo = prestar(client, socio["id"], libro["id"]).json()

    assert prestamo["fecha_prestamo"] == date.today().isoformat()
    assert prestamo["fecha_vencimiento"] == (date.today() + timedelta(days=14)).isoformat()


# Regla 5: al devolver se repone el stock y se calcula la multa ($100 por día de atraso)
def test_al_devolver_se_repone_el_stock(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro(stock=1)
    prestamo = prestar(client, socio["id"], libro["id"]).json()
    assert stock_de(client, libro["id"]) == 0

    r = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert r.status_code == 200
    assert r.json()["fecha_devolucion"] == date.today().isoformat()
    assert stock_de(client, libro["id"]) == 1


def test_devolver_a_tiempo_no_tiene_multa(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro()
    prestamo = prestar(client, socio["id"], libro["id"]).json()

    r = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert r.json()["multa"] == 0


def test_la_multa_es_100_por_dia_de_atraso(client, crear_socio, crear_libro, atrasar):
    socio = crear_socio()
    libro = crear_libro()
    prestamo = prestar(client, socio["id"], libro["id"]).json()
    atrasar(prestamo["id"], dias=3)

    r = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert r.json()["multa"] == 300


# Regla 6: no se puede devolver un préstamo ya devuelto -> 409
def test_no_se_puede_devolver_dos_veces(client, crear_socio, crear_libro):
    socio = crear_socio()
    libro = crear_libro()
    prestamo = prestar(client, socio["id"], libro["id"]).json()
    client.post(f"/prestamos/{prestamo['id']}/devolucion")

    r = client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert r.status_code == 409
    assert stock_de(client, libro["id"]) == 1  # el stock no se repuso dos veces


# Regla 7: recurso inexistente -> 404
def test_prestar_con_socio_inexistente_devuelve_404(client, crear_libro):
    libro = crear_libro()

    assert prestar(client, 999, libro["id"]).status_code == 404


def test_prestar_libro_inexistente_devuelve_404(client, crear_socio):
    socio = crear_socio()

    assert prestar(client, socio["id"], 999).status_code == 404


def test_devolver_prestamo_inexistente_devuelve_404(client):
    assert client.post("/prestamos/999/devolucion").status_code == 404


# Extra: listado de préstamos vencidos
def test_listar_prestamos_vencidos(client, crear_socio, crear_libro, atrasar):
    socio = crear_socio()
    libro = crear_libro(stock=5)
    vencido = prestar(client, socio["id"], libro["id"]).json()
    prestar(client, socio["id"], libro["id"])  # este está al día
    atrasar(vencido["id"], dias=2)

    r = client.get("/prestamos/vencidos")

    assert [p["id"] for p in r.json()] == [vencido["id"]]


def test_un_prestamo_devuelto_ya_no_figura_como_vencido(
    client, crear_socio, crear_libro, atrasar
):
    socio = crear_socio()
    libro = crear_libro()
    prestamo = prestar(client, socio["id"], libro["id"]).json()
    atrasar(prestamo["id"], dias=2)
    client.post(f"/prestamos/{prestamo['id']}/devolucion")

    assert client.get("/prestamos/vencidos").json() == []