# LabTurn - Sistema Inteligente de Gestion de Turnos

LabTurn es una propuesta tecnologica profesional para gestionar turnos de atencion en un laboratorio. Incluye una aplicacion Angular integrada con navegacion interna y un backend Flask con una cola FIFO en memoria para cuatro mesas de atencion.

## Objetivo

Demostrar un sistema empresarial de turnos que permita generar tickets, visualizar llamados en un monitor publico y administrar cuatro mesas de atencion desde un panel operativo, sin solicitar datos personales y sin utilizar bases de datos.

## Tecnologias utilizadas

- Frontend: Angular, TypeScript, Angular Material y SCSS.
- Backend: Python con Flask y Flask-CORS.
- Comunicacion: API REST con polling HTTP cada segundo.
- Publicacion: Angular y Flask en Vercel.
- Control de versiones: Git y GitHub.

No utiliza bases de datos, Redis, Upstash, Render, KV, Firebase, Supabase, WebSockets, voz, Web Speech API, React, Vue ni Node.js como backend.

## Funcionalidades

- Generacion consecutiva de turnos: `A001`, `A002`, `A003`...
- Cola de espera FIFO.
- Panel publico tipo monitor con cuatro tarjetas grandes.
- Panel de atencion para llamar el siguiente turno y finalizar turnos.
- Sonido digital breve de notificacion, activado por el usuario desde el monitor.
- Identificador de evento por asignacion para evitar sonidos duplicados.
- Navegacion interna desde una sola aplicacion web.
- Estadisticas de turnos generados, atendidos y pendientes.
- Mensajes de error cuando la API Flask no esta disponible.
- Diseno responsive con identidad visual premium.

## Arquitectura

```text
labturn-sistema-turnos/
  frontend/   Aplicacion Angular
  backend/    API REST Flask
  README.md
  .gitignore
```

Pantallas:

- `/`: abre la aplicacion integrada de LabTurn.
- `/clientes`: generador de turnos de autoservicio.
- `/clientes/monitor`: monitor publico de turnos.
- `/atencion`: panel de control de cuatro mesas.

Endpoints:

- `POST /api/turnos`
- `GET /api/estado`
- `GET /api/ventanillas`
- `GET /api/turnos/espera`
- `POST /api/ventanillas/{id}/llamar`
- `POST /api/ventanillas/{id}/finalizar`
- `GET /api/health`

## Flujo de ejemplo

1. Se genera `A001` y queda en espera.
2. Se genera `A002` y queda en espera.
3. Mesa 1 llama el siguiente turno y recibe `A001`.
4. Mesa 2 llama el siguiente turno y recibe `A002`.
5. Al finalizar Mesa 1, la mesa queda disponible.
6. El monitor recibe un nuevo `id_evento`, muestra el aviso destacado y reproduce una campanita si el sonido fue habilitado.

## Instalacion

### Backend

> Requiere Python 3.11 o superior instalado localmente.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Ejecucion local

Forma recomendada en Windows PowerShell:

```powershell
cd C:\Users\pedra\Documents\Codex\2026-10-12\act-a-como-un-desarrollador-full\outputs\labturn-sistema-turnos
npm start
```

Ese comando prepara dependencias, inicia Flask en el puerto `5000`, inicia Angular en el puerto `4200` y mantiene ambos procesos activos en la misma terminal. Para detener el sistema completo, presionar `Ctrl+C`.

Ejecucion manual del backend:

```powershell
cd backend
python -m pip install --target .deps -r requirements.txt
$env:PYTHONPATH="$PWD\.deps"
python app.py
```

Ejecucion manual del frontend:

```powershell
cd frontend
npm install
npm start
```

Abrir:

- Aplicacion integrada: `http://127.0.0.1:4200/`
- Clientes: `http://127.0.0.1:4200/clientes`
- Monitor: `http://127.0.0.1:4200/clientes/monitor`
- Atencion: `http://127.0.0.1:4200/atencion`

## Pruebas

Backend:

```bash
cd backend
pytest
```

Frontend:

```bash
cd frontend
npm run build
```

Pruebas esperadas:

- Backend: pytest sobre `backend/tests`.
- Frontend: `npm run build` completado correctamente.
- Flujo cubierto: generacion consecutiva, llamado explicito desde mesas, cola FIFO, bloqueo de doble asignacion, finalizacion y monitor por polling.

## Vercel

El proyecto esta preparado para desplegar Angular y Flask unicamente en Vercel desde el `vercel.json` de la raiz.

Para publicar:

```bash
npm install
cd frontend && npm install && cd ..
vercel --prod
```

Angular usa rutas relativas `/api`, asi que no requiere configurar URLs externas.

## Limitaciones tecnicas

- El estado vive en memoria RAM del proceso Flask.
- Vercel Functions no garantizan una unica instancia persistente; esta version es una demo temporal.
- Si Vercel recicla o escala la Function, los turnos pueden reiniciarse.
- No hay persistencia historica porque no se utiliza ninguna base de datos ni almacenamiento externo.
- El sonido del monitor requiere presionar `Activar sonido` por politicas de navegadores.

## GitHub

Repositorio esperado: `https://github.com/Aripe09/labturn-sistema-turnos`.

Comandos de publicacion:

```bash
gh auth login -h github.com
gh repo create labturn-sistema-turnos --public --source . --remote origin --push
```

Para agregar al docente `alextessfp` como colaborador en GitHub:

1. Abrir el repositorio en GitHub.
2. Ir a `Settings`.
3. Entrar a `Collaborators`.
4. Seleccionar `Add people`.
5. Escribir `alextessfp` y confirmar la invitacion.

No se envio ninguna invitacion automaticamente.

## Autoria

Proyecto preparado para la presentacion academica de LabTurn por `Aripe09`.
Despliegue inicial de LabTurn mediante GitHub y Vercel.

