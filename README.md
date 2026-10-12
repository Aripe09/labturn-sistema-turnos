# LabTurn - Sistema Inteligente de Gestion de Turnos

LabTurn es una propuesta tecnologica profesional para gestionar turnos de atencion en un laboratorio. Incluye un frontend Angular con tres pantallas y un backend Flask con una cola FIFO en memoria para cuatro mesas de atencion.

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

- `/clientes`: generador de turnos de autoservicio.
- `/clientes/monitor`: monitor publico de turnos.
- `/atencion`: panel de control de cuatro mesas.

Endpoints:

- `POST /api/turnos`
- `GET /api/estado`
- `GET /api/ventanillas`
- `POST /api/ventanillas/{id}/finalizar`
- `GET /api/health`

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

En una terminal:

```bash
cd backend
.venv\Scripts\activate
flask --app app run --host 127.0.0.1 --port 5000
```

En otra terminal:

```bash
cd frontend
npm start
```

Abrir:

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

Las pruebas cubren generacion consecutiva, asignacion automatica, cola FIFO, finalizacion y reasignacion del siguiente turno.

## Vercel

El frontend esta preparado con `frontend/vercel.json`.

Para publicar:

```bash
cd frontend
npm install
npm run build
vercel
```

Importante: Vercel solo alojara el frontend Angular. El backend Flask debe ejecutarse como servicio Python aparte para que la API REST exista. Este proyecto no usa Render por restriccion, y tampoco afirma persistencia en memoria dentro de funciones serverless. Para la demostracion completa, ejecutar Flask localmente en un unico proceso.

Si el frontend publicado necesita consumir un backend remoto, configurar `apiUrl` en `frontend/src/environments/environment.ts` con la URL publica real de la API antes del build.

## Limitaciones tecnicas

- El estado vive en memoria de Python y se pierde al reiniciar Flask.
- La demo debe ejecutarse con un unico proceso Flask para conservar una sola cola compartida.
- No hay persistencia historica ni recuperacion ante reinicio porque no se utiliza base de datos.
- El sonido del monitor requiere presionar `Activar sonido` por politicas de navegadores.

## GitHub

Repositorio sugerido: `labturn-sistema-turnos`.

Comandos para subirlo si ya tienes un repositorio creado en GitHub:

```bash
git init
git add .
git commit -m "Implement LabTurn turn management system"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/labturn-sistema-turnos.git
git push -u origin main
```

Para agregar al docente `alextessfp` como colaborador en GitHub:

1. Abrir el repositorio en GitHub.
2. Ir a `Settings`.
3. Entrar a `Collaborators`.
4. Seleccionar `Add people`.
5. Escribir `alextessfp` y confirmar la invitacion.

No se envio ninguna invitacion automaticamente.

