from __future__ import annotations

from collections import deque
from copy import deepcopy
import os
from threading import RLock
from typing import Any

from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)


def _allowed_origins() -> list[str] | str:
    origins = os.getenv("ALLOWED_ORIGINS", "").strip()
    if not origins:
        return "*"
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


CORS(app, origins=_allowed_origins())


class LabTurnState:
    """In-memory FIFO turn manager for a single-process Flask demo."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._next_number = 1
        self._waiting: deque[str] = deque()
        self._last_called: dict[str, Any] | None = None
        self._event_counter = 0
        self._generated_count = 0
        self._finished_count = 0
        self._desks = [
            {"id": 1, "nombre": "Mesa 1", "estado": "disponible", "turno_actual": None},
            {"id": 2, "nombre": "Mesa 2", "estado": "disponible", "turno_actual": None},
            {"id": 3, "nombre": "Mesa 3", "estado": "disponible", "turno_actual": None},
            {"id": 4, "nombre": "Mesa 4", "estado": "disponible", "turno_actual": None},
        ]

    def reset_for_tests(self) -> None:
        with self._lock:
            self.__init__()

    def create_turn(self) -> dict[str, Any]:
        with self._lock:
            turn = f"A{self._next_number:03d}"
            self._next_number += 1
            self._generated_count += 1
            self._waiting.append(turn)

            return {"turno": turn, "estado": "en_espera", "mesa": None, "asignacion": None}

    def call_next(self, desk_id: int) -> tuple[dict[str, Any], int]:
        with self._lock:
            desk = self._find_desk(desk_id)
            if desk is None:
                return {"error": "Mesa no encontrada"}, 404
            if desk["turno_actual"] is not None:
                return {"error": f"Mesa {desk_id} ya esta atendiendo un turno"}, 409
            if not self._waiting:
                return {"error": "No hay turnos en espera"}, 409

            next_turn = self._waiting.popleft()
            return {"mesa": desk_id, "asignacion": self._assign_to_desk(desk, next_turn)}, 200

    def finish_desk(self, desk_id: int) -> dict[str, Any] | None:
        with self._lock:
            desk = self._find_desk(desk_id)
            if desk is None:
                return None

            finished_turn = desk["turno_actual"]
            desk["turno_actual"] = None
            desk["estado"] = "disponible"
            if finished_turn is not None:
                self._finished_count += 1

            return {
                "mesa": desk_id,
                "turno_finalizado": finished_turn,
            }

    def state(self) -> dict[str, Any]:
        with self._lock:
            return {
                "ventanillas": deepcopy(self._desks),
                "turnos_en_espera": list(self._waiting),
                "cantidad_espera": len(self._waiting),
                "ultimo_llamado": deepcopy(self._last_called),
                "siguiente_turno": f"A{self._next_number:03d}",
                "total_generados": self._generated_count,
                "total_atendidos": self._finished_count,
            }

    def desks(self) -> list[dict[str, Any]]:
        with self._lock:
            return deepcopy(self._desks)

    def _find_desk(self, desk_id: int) -> dict[str, Any] | None:
        return next((desk for desk in self._desks if desk["id"] == desk_id), None)

    def _assign_to_desk(self, desk: dict[str, Any], turn: str) -> dict[str, Any]:
        self._event_counter += 1
        desk["estado"] = "ocupada"
        desk["turno_actual"] = turn
        event = {
            "id_evento": self._event_counter,
            "turno": turn,
            "mesa": desk["id"],
            "mensaje": f"TURNO {turn} - PASE A MESA {desk['id']}",
        }
        self._last_called = event
        return deepcopy(event)


store = LabTurnState()


@app.post("/api/turnos")
def create_turn():
    return jsonify(store.create_turn()), 201


@app.get("/api/estado")
def get_state():
    return jsonify(store.state())


@app.get("/api/ventanillas")
def get_desks():
    return jsonify({"ventanillas": store.desks()})


@app.get("/api/turnos/espera")
def get_waiting_turns():
    return jsonify({"turnos_en_espera": store.state()["turnos_en_espera"]})


@app.post("/api/ventanillas/<int:desk_id>/llamar")
def call_next(desk_id: int):
    result, status = store.call_next(desk_id)
    return jsonify(result), status


@app.post("/api/ventanillas/<int:desk_id>/finalizar")
def finish_desk(desk_id: int):
    result = store.finish_desk(desk_id)
    if result is None:
        return jsonify({"error": "Mesa no encontrada"}), 404
    return jsonify(result)


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "LabTurn API",
        "store": "memory",
        "workers": 1,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True, use_reloader=False)

