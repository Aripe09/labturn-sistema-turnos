# LabTurn - Sistema Inteligente de Gestion de Turnos

LabTurn es una propuesta tecnologica profesional para gestionar turnos de atencion en un laboratorio. Incluye una aplicacion Angular integrada con navegacion interna y un backend Flask con una cola FIFO en memoria para cuatro mesas de atencion.

## Objetivo

Demostrar un sistema empresarial de turnos que permita generar tickets, visualizar llamados en un monitor publico y administrar cuatro mesas de atencion desde un panel operativo, sin solicitar datos personales y sin utilizar bases de datos.

## Tecnologias utilizadas

- Frontend: Angular, TypeScript, Angular Material y SCSS.
- Backend: Python con Flask y Flask-CORS.
- Comunicacion: API REST con polling HTTP cada segundo.
- Publicacion del frontend: preparado para Vercel.
- Control de versiones: Git y GitHub.

No utiliza bases de datos, WebSockets, Render, Firebase, Supabase, voz, Web Speech API, React, Vue ni Node.js como backend.

## Funcionalidades

- Generacion consecutiva de turnos: `A001`, `A002`, `A003`...
- Asignacion automatica a la primera mesa disponible.
- Cola de espera FIFO cuando las cuatro mesas estan ocupadas.
- Panel publico tipo monitor con cuatro tarjetas grandes.
- Panel de atencion para finalizar turnos y asignar automaticamente el siguiente.
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
- `POST /api/ventanillas/{id}/finalizar`
- `GET /api/health`

## Flujo de ejemplo

1. Se genera `A001` y se asigna a Mesa 1.
2. Se genera `A002` y se asigna a Mesa 2.
3. Se genera `A003` y se asigna a Mesa 3.
4. Se genera `A004` y se asigna a Mesa 4.
5. Se genera `A005` y queda en espera.
6. Al finalizar Mesa 2, `A005` se asigna automaticamente a Mesa 2.
7. El monitor recibe un nuevo `id_evento`, muestra el aviso destacado y reproduce una campanita si el sonido fue habilitado.

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

El proyecto esta preparado para desplegar frontend Angular y API Flask serverless desde el `vercel.json` de la raiz.

Para publicar:

```bash
npm install
cd frontend && npm install && cd ..
vercel --prod
```

Importante: en produccion Vercel necesita almacenamiento compartido. Configura `UPSTASH_REDIS_REST_URL` y `UPSTASH_REDIS_REST_TOKEN` en las variables de entorno del proyecto. Tambien se aceptan `KV_REST_API_URL` y `KV_REST_API_TOKEN`.

En produccion Angular usa `/api` como URL base. Ver `DEPLOYMENT.md` para los detalles de Upstash Redis y el comportamiento de `/api/health`.

## Limitaciones tecnicas

- El estado de produccion vive en Upstash Redis o Vercel KV compatible con Redis REST.
- El fallback en memoria es solo para desarrollo local.
- No hay persistencia historica permanente porque el sistema mantiene un estado operativo temporal de turnos.
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

