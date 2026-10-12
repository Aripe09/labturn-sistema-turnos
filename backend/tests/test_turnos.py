import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, store


def client():
    app.config.update(TESTING=True)
    store.reset_for_tests()
    return app.test_client()


def test_generates_consecutive_turns_and_keeps_them_waiting():
    test_client = client()

    created = [test_client.post("/api/turnos").get_json() for _ in range(4)]

    assert [item["turno"] for item in created] == ["A001", "A002", "A003", "A004"]
    assert [item["mesa"] for item in created] == [None, None, None, None]
    assert [item["asignacion"] for item in created] == [None, None, None, None]


def test_fifo_queue_and_explicit_desk_calls():
    test_client = client()

    for _ in range(2):
        test_client.post("/api/turnos")

    state = test_client.get("/api/estado").get_json()
    assert state["turnos_en_espera"] == ["A001", "A002"]

    first = test_client.post("/api/ventanillas/1/llamar").get_json()
    second = test_client.post("/api/ventanillas/2/llamar").get_json()

    assert first["asignacion"]["turno"] == "A001"
    assert first["asignacion"]["mesa"] == 1
    assert second["asignacion"]["turno"] == "A002"
    assert second["asignacion"]["mesa"] == 2

    state = test_client.get("/api/estado").get_json()
    assert state["cantidad_espera"] == 0
    assert state["ultimo_llamado"]["id_evento"] == 2


def test_busy_desk_cannot_call_another_turn():
    test_client = client()
    test_client.post("/api/turnos")
    test_client.post("/api/turnos")

    assert test_client.post("/api/ventanillas/1/llamar").status_code == 200
    duplicate = test_client.post("/api/ventanillas/1/llamar")

    assert duplicate.status_code == 409
    state = test_client.get("/api/estado").get_json()
    assert state["turnos_en_espera"] == ["A002"]


def test_finish_without_waiting_turns_leaves_desk_available():
    test_client = client()
    test_client.post("/api/turnos")
    test_client.post("/api/ventanillas/1/llamar")

    result = test_client.post("/api/ventanillas/1/finalizar").get_json()

    assert result["turno_finalizado"] == "A001"
    desks = test_client.get("/api/ventanillas").get_json()["ventanillas"]
    assert desks[0]["estado"] == "disponible"
    assert desks[0]["turno_actual"] is None

