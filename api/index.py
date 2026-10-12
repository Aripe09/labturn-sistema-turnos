from __future__ import annotations

import json
import os
from collections import deque
from copy import deepcopy
from threading import RLock
from typing import Any

import requests
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def _initial_state() -> dict[str, Any]:
    return {
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


def _public_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "ventanillas": deepcopy(state["desks"]),
        "turnos_en_espera": list(state["waiting"]),
        "cantidad_espera": len(state["waiting"]),
        "ultimo_llamado": deepcopy(state["last_called"]),
        "siguiente_turno": f"A{state['next_number']:03d}",
        "total_generados": state["generated_count"],
        "total_atendidos": state["finished_count"],
    }


def _assign_to_desk(state: dict[str, Any], desk: dict[str, Any], turn: str) -> dict[str, Any]:
    state["event_counter"] += 1
    desk["estado"] = "ocupada"
    desk["turno_actual"] = turn
    event = {
        "id_evento": state["event_counter"],
        "turno": turn,
        "mesa": desk["id"],
        "mensaje": f"TURNO {turn} - PASE A MESA {desk['id']}",
    }
    state["last_called"] = event
    return deepcopy(event)


class MemoryStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._state = _initial_state()

    def create_turn(self) -> dict[str, Any]:
        with self._lock:
            turn = f"A{self._state['next_number']:03d}"
            self._state["next_number"] += 1
            self._state["generated_count"] += 1

            desk = next((item for item in self._state["desks"] if item["estado"] == "disponible"), None)
            if desk is None:
                self._state["waiting"].append(turn)
                return {"turno": turn, "estado": "en_espera", "mesa": None, "asignacion": None}

            assigned = _assign_to_desk(self._state, desk, turn)
            return {"turno": turn, "estado": "asignado", "mesa": assigned["mesa"], "asignacion": assigned}

    def finish_desk(self, desk_id: int) -> dict[str, Any] | None:
        with self._lock:
            desk = next((item for item in self._state["desks"] if item["id"] == desk_id), None)
            if desk is None:
                return None

            finished_turn = desk["turno_actual"]
            desk["turno_actual"] = None
            desk["estado"] = "disponible"
            if finished_turn is not None:
                self._state["finished_count"] += 1

            next_assignment = None
            if self._state["waiting"]:
                next_assignment = _assign_to_desk(self._state, desk, self._state["waiting"].pop(0))

            return {"mesa": desk_id, "turno_finalizado": finished_turn, "nueva_asignacion": next_assignment}

    def state(self) -> dict[str, Any]:
        with self._lock:
            return _public_state(self._state)


REDIS_SCRIPT = r"""
local key = KEYS[1]
local action = ARGV[1]
local desk_id = tonumber(ARGV[2] or "0")

local raw = redis.call("GET", key)
local state
if raw then
  state = cjson.decode(raw)
else
  state = {
    next_number = 1,
    waiting = {},
    last_called = cjson.null,
    event_counter = 0,
    generated_count = 0,
    finished_count = 0,
    desks = {
      {id = 1, nombre = "Mesa 1", estado = "disponible", turno_actual = cjson.null},
      {id = 2, nombre = "Mesa 2", estado = "disponible", turno_actual = cjson.null},
      {id = 3, nombre = "Mesa 3", estado = "disponible", turno_actual = cjson.null},
      {id = 4, nombre = "Mesa 4", estado = "disponible", turno_actual = cjson.null}
    }
  }
end

local function assign_to_desk(desk, turn)
  state.event_counter = state.event_counter + 1
  desk.estado = "ocupada"
  desk.turno_actual = turn
  local event = {
    id_evento = state.event_counter,
    turno = turn,
    mesa = desk.id,
    mensaje = "TURNO " .. turn .. " - PASE A MESA " .. desk.id
  }
  state.last_called = event
  return event
end

local function public_state()
  return {
    ventanillas = state.desks,
    turnos_en_espera = state.waiting,
    cantidad_espera = #state.waiting,
    ultimo_llamado = state.last_called,
    siguiente_turno = string.format("A%03d", state.next_number),
    total_generados = state.generated_count,
    total_atendidos = state.finished_count
  }
end

local result
if action == "create" then
  local turn = string.format("A%03d", state.next_number)
  state.next_number = state.next_number + 1
  state.generated_count = state.generated_count + 1

  local free_desk = nil
  for i, desk in ipairs(state.desks) do
    if desk.estado == "disponible" then
      free_desk = desk
      break
    end
  end

  if free_desk then
    local assignment = assign_to_desk(free_desk, turn)
    result = {turno = turn, estado = "asignado", mesa = assignment.mesa, asignacion = assignment}
  else
    table.insert(state.waiting, turn)
    result = {turno = turn, estado = "en_espera", mesa = cjson.null, asignacion = cjson.null}
  end
elseif action == "finish" then
  local desk = nil
  for i, item in ipairs(state.desks) do
    if item.id == desk_id then
      desk = item
      break
    end
  end

  if not desk then
    result = {error = "Mesa no encontrada", status = 404}
  else
    local finished_turn = desk.turno_actual
    desk.turno_actual = cjson.null
    desk.estado = "disponible"
    if finished_turn ~= cjson.null then
      state.finished_count = state.finished_count + 1
    end

    local next_assignment = cjson.null
    if #state.waiting > 0 then
      local next_turn = table.remove(state.waiting, 1)
      next_assignment = assign_to_desk(desk, next_turn)
    end

    result = {mesa = desk_id, turno_finalizado = finished_turn, nueva_asignacion = next_assignment}
  end
elseif action == "state" then
  result = public_state()
elseif action == "desks" then
  result = {ventanillas = state.desks}
elseif action == "waiting" then
  result = {turnos_en_espera = state.waiting}
else
  result = {error = "Accion no soportada", status = 400}
end

redis.call("SET", key, cjson.encode(state))
return cjson.encode(result)
"""


class RedisStore:
    def __init__(self) -> None:
        self._url = (
            os.getenv("KV_REST_API_URL")
            or os.getenv("UPSTASH_REDIS_REST_URL")
            or ""
        ).rstrip("/")
        self._token = os.getenv("KV_REST_API_TOKEN") or os.getenv("UPSTASH_REDIS_REST_TOKEN") or ""
        self._key = os.getenv("LABTURN_STATE_KEY", "labturn:state")
        if not self._url or not self._token:
            raise RuntimeError("Redis/KV no configurado")

    def _command(self, action: str, arg: int | None = None) -> dict[str, Any]:
        payload: list[Any] = ["EVAL", REDIS_SCRIPT, 1, self._key, action]
        if arg is not None:
            payload.append(str(arg))

        response = requests.post(
            self._url,
            headers={"Authorization": f"Bearer {self._token}"},
            json=payload,
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise RuntimeError(data["error"])
        result = data.get("result")
        if isinstance(result, str):
            return json.loads(result)
        return result

    def create_turn(self) -> dict[str, Any]:
        return self._command("create")

    def finish_desk(self, desk_id: int) -> dict[str, Any] | None:
        result = self._command("finish", desk_id)
        if result.get("status") == 404:
            return None
        return result

    def state(self) -> dict[str, Any]:
        return self._command("state")

    def desks(self) -> dict[str, Any]:
        return self._command("desks")

    def waiting(self) -> dict[str, Any]:
        return self._command("waiting")


memory_store = MemoryStore()


def get_store():
    if os.getenv("VERCEL") == "1":
        return RedisStore()

    try:
        return RedisStore()
    except RuntimeError:
        return memory_store


def service_unavailable(error: Exception):
    return jsonify({
        "error": "Redis/KV no configurado",
        "detalle": str(error),
        "mensaje": "Configura KV_REST_API_URL y KV_REST_API_TOKEN en Vercel para usar LabTurn en internet."
    }), 503


@app.post("/api/turnos")
def create_turn():
    try:
        return jsonify(get_store().create_turn()), 201
    except RuntimeError as error:
        return service_unavailable(error)


@app.get("/api/estado")
def get_state():
    try:
        return jsonify(get_store().state())
    except RuntimeError as error:
        return service_unavailable(error)


@app.get("/api/ventanillas")
def get_desks():
    try:
        store = get_store()
        if isinstance(store, RedisStore):
            return jsonify(store.desks())
        return jsonify({"ventanillas": store.state()["ventanillas"]})
    except RuntimeError as error:
        return service_unavailable(error)


@app.get("/api/turnos/espera")
def get_waiting_turns():
    try:
        store = get_store()
        if isinstance(store, RedisStore):
            return jsonify(store.waiting())
        return jsonify({"turnos_en_espera": store.state()["turnos_en_espera"]})
    except RuntimeError as error:
        return service_unavailable(error)


@app.post("/api/ventanillas/<int:desk_id>/finalizar")
def finish_desk(desk_id: int):
    try:
        result = get_store().finish_desk(desk_id)
    except RuntimeError as error:
        return service_unavailable(error)

    if result is None:
        return jsonify({"error": "Mesa no encontrada"}), 404
    return jsonify(result)


@app.get("/api/health")
def health():
    try:
        store_type = "redis" if isinstance(get_store(), RedisStore) else "memory"
    except RuntimeError:
        store_type = "redis_missing"
    return jsonify({"status": "ok", "service": "LabTurn API", "store": store_type})

