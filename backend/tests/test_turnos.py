from app import app, store


def client():
    app.config.update(TESTING=True)
    store.reset_for_tests()
    return app.test_client()


def test_generates_consecutive_turns_and_assigns_available_desks():
    test_client = client()

    created = [test_client.post("/api/turnos").get_json() for _ in range(4)]

    assert [item["turno"] for item in created] == ["A001", "A002", "A003", "A004"]
    assert [item["mesa"] for item in created] == [1, 2, 3, 4]
    assert [item["asignacion"]["mesa"] for item in created] == [1, 2, 3, 4]


def test_fifo_queue_and_auto_assignment_after_finish():
    test_client = client()

    for _ in range(5):
        test_client.post("/api/turnos")

    state = test_client.get("/api/estado").get_json()
    assert state["turnos_en_espera"] == ["A005"]

    result = test_client.post("/api/ventanillas/2/finalizar").get_json()

    assert result["turno_finalizado"] == "A002"
    assert result["nueva_asignacion"]["turno"] == "A005"
    assert result["nueva_asignacion"]["mesa"] == 2

    state = test_client.get("/api/estado").get_json()
    assert state["cantidad_espera"] == 0
    assert state["ultimo_llamado"]["id_evento"] == 5


def test_finish_without_waiting_turns_leaves_desk_available():
    test_client = client()
    test_client.post("/api/turnos")

    result = test_client.post("/api/ventanillas/1/finalizar").get_json()

    assert result["turno_finalizado"] == "A001"
    assert result["nueva_asignacion"] is None
    desks = test_client.get("/api/ventanillas").get_json()["ventanillas"]
    assert desks[0]["estado"] == "disponible"
    assert desks[0]["turno_actual"] is None

