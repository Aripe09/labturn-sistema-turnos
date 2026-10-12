import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from api.index import app, memory_store


def client():
    os.environ.pop("VERCEL", None)
    memory_store._state = {
        "next_number": 1,
        "waiting": [],
        "last_called": None,
        "event_counter": 0,
        "generated_count": 0,
        "finished_count": 0,
        "desks": [
            {"id": 1, "nombre": "Mesa 1", "estado": "disponible", "turno_actual": None},
            {"id": 2, "nombre": "Mesa 2", "estado": "disponible", "turno_actual": None},
            {"id": 3, "nombre": "Mesa 3", "estado": "disponible", "turno_actual": None},
            {"id": 4, "nombre": "Mesa 4", "estado": "disponible", "turno_actual": None},
        ],
    }
    app.config.update(TESTING=True)
    return app.test_client()


def test_vercel_api_turn_flow_with_local_fallback():
    test_client = client()

    created = [test_client.post("/api/turnos", json={}).get_json() for _ in range(5)]

    assert [item["turno"] for item in created] == ["A001", "A002", "A003", "A004", "A005"]
    assert [item["mesa"] for item in created] == [1, 2, 3, 4, None]

    finish = test_client.post("/api/ventanillas/2/finalizar", json={}).get_json()
    assert finish["turno_finalizado"] == "A002"
    assert finish["nueva_asignacion"]["turno"] == "A005"
    assert finish["nueva_asignacion"]["mesa"] == 2

    state = test_client.get("/api/estado").get_json()
    assert state["cantidad_espera"] == 0
    assert state["total_generados"] == 5
    assert state["total_atendidos"] == 1

