# Publicacion de LabTurn en Internet

## Arquitectura

LabTurn se publica en dos servicios:

- Frontend Angular en Vercel.
- Backend Flask en Render como Web Service.

El backend guarda los turnos en listas, diccionarios y variables en memoria RAM. No usa Redis, Upstash, KV, PostgreSQL, MySQL, SQLite ni ningun almacenamiento externo.

## Por que Flask no va en Vercel

Vercel ejecuta funciones serverless. Esa arquitectura no garantiza que dos solicitudes usen el mismo proceso ni la misma memoria. Por eso no es correcto guardar la cola de turnos en variables globales dentro de Vercel Functions.

Render ejecuta Flask como un proceso web normal. Mientras el proceso este activo, las solicitudes comparten la misma memoria y las cuatro ventanillas ven el mismo estado.

## Limitaciones aceptadas

- Si Render reinicia el servicio, la cola se borra y el siguiente turno vuelve a `A001`.
- En el plan gratuito, Render puede dormir el servicio tras inactividad.
- El primer acceso despues de dormir puede tardar mas.
- Debe usarse un solo worker de Gunicorn para mantener una sola memoria compartida.

## Backend en Render

El archivo `render.yaml` define:

```bash
gunicorn --workers 1 --threads 8 --timeout 60 --bind 0.0.0.0:$PORT backend.app:app
```

`--workers 1` es importante. Si se usan varios workers, cada worker tendria su propia memoria y podrian aparecer estados diferentes.

Variable recomendada en Render:

- `ALLOWED_ORIGINS`: URL publica de Vercel, por ejemplo `https://tu-app.vercel.app`.

Si no se configura, Flask permite CORS desde cualquier origen para facilitar la practica escolar.

## Frontend en Vercel

Angular obtiene la URL del backend desde la variable de entorno:

- `LABTURN_API_URL`

Cuando tengas la URL real de Render, configúrala en Vercel con este formato:

```text
https://TU-SERVICIO.onrender.com/api
```

No inventes esta URL: debe ser la URL real que Render te muestre al crear el Web Service.

## Verificacion

Backend:

```text
https://TU-SERVICIO.onrender.com/api/health
```

Debe responder:

```json
{
  "service": "LabTurn API",
  "status": "ok",
  "store": "memory",
  "workers": 1
}
```

Frontend:

- `/clientes`: genera turnos.
- `/atencion`: llama y finaliza turnos desde cuatro mesas.
- `/clientes/monitor`: muestra llamados y reproduce sonido cuando se habilita.
