import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from api.index import app
from backend.app import store


def client():
    store.reset_for_tests()
    app.config.update(TESTING=True)
    return app.test_client()


def test_vercel_api_turn_flow_with_local_fallback():
    test_client = client()

    created = [test_client.post("/api/turnos", json={}).get_json() for _ in range(2)]

    assert [item["turno"] for item in created] == ["A001", "A002"]
    assert [item["estado"] for item in created] == ["en_espera", "en_espera"]

    call_1 = test_client.post("/api/ventanillas/1/llamar", json={}).get_json()
    assert call_1["asignacion"]["turno"] == "A001"
    assert call_1["asignacion"]["mesa"] == 1

    duplicate_call = test_client.post("/api/ventanillas/1/llamar", json={})
    assert duplicate_call.status_code == 409

    call_2 = test_client.post("/api/ventanillas/2/llamar", json={}).get_json()
    assert call_2["asignacion"]["turno"] == "A002"
    assert call_2["asignacion"]["mesa"] == 2

    finish_1 = test_client.post("/api/ventanillas/1/finalizar", json={}).get_json()
    assert finish_1["turno_finalizado"] == "A001"

    finish_2 = test_client.post("/api/ventanillas/2/finalizar", json={}).get_json()
    assert finish_2["turno_finalizado"] == "A002"

    state = test_client.get("/api/estado").get_json()
    assert state["cantidad_espera"] == 0
    assert state["total_generados"] == 2
    assert state["total_atendidos"] == 2

