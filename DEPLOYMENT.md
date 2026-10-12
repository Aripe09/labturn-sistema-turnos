# Publicacion de LabTurn en Internet

## Estado actual

El frontend Angular esta preparado para Vercel y ya no apunta a `localhost` en produccion. La URL de API en produccion queda como `/api`, usando la Function Flask incluida en `api/index.py`.

## Almacenamiento compartido

En Vercel, el estado de turnos debe guardarse en Upstash Redis o Vercel KV compatible con Redis REST. Las variables globales de memoria solo se usan como fallback local, porque una Function serverless puede reiniciarse o ejecutarse en instancias distintas.

Variables requeridas en Vercel:

- `UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN`

Tambien se aceptan los nombres de Vercel KV:

- `KV_REST_API_URL`
- `KV_REST_API_TOKEN`

`LABTURN_STATE_KEY` es opcional y permite cambiar la llave donde se guarda el estado compartido. Si faltan las variables en produccion, `/api/health` responde error y la app muestra un mensaje claro.

## Funcionamiento

La API usa una operacion atomica de Redis para:

- generar turnos consecutivos y ponerlos en espera;
- llamar el siguiente turno desde una mesa;
- impedir que dos mesas tomen el mismo turno;
- finalizar una atencion sin reasignar automaticamente.

## Publicacion

El despliegue principal usa el `vercel.json` de la raiz:

```bash
vercel --prod
```

