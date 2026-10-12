# Publicacion de LabTurn en Vercel

## Arquitectura

LabTurn se publica unicamente en Vercel:

- Angular se compila como frontend estatico.
- Flask se expone como Vercel Function desde `api/index.py`.
- Angular llama al backend con rutas relativas `/api/...`.

No usa Redis, Upstash, Render, Firebase, Supabase, bases de datos ni almacenamiento externo.

## Modo demo con memoria temporal

El backend guarda los turnos en listas, diccionarios y variables en memoria RAM del proceso Flask. Esto permite que la practica funcione desde el enlace publico de Vercel sin ejecutar servidores en la computadora local.

Limitacion importante: Vercel Functions no garantizan una unica instancia persistente para todas las solicitudes. Por eso, esta version es una demo temporal y no debe presentarse como sincronizacion garantizada entre multiples instancias. Si Vercel recicla o escala la Function, el estado puede reiniciarse.

## Verificacion

Despues del despliegue, revisa:

```text
https://TU-APP.vercel.app/api/health
```

Debe responder:

```json
{
  "service": "LabTurn API",
  "mode": "vercel_demo",
  "status": "ok",
  "store": "memory",
  "warning": "Estado temporal en memoria; Vercel no garantiza una unica instancia persistente."
}
```

Luego prueba:

- `/clientes`: generar turnos.
- `/atencion`: llamar y finalizar desde las cuatro mesas.
- `/clientes/monitor`: ver el ultimo llamado y activar sonido.
