# Publicacion de LabTurn en Internet

## Estado actual

El frontend Angular esta preparado para Vercel y ya no apunta a `localhost` en produccion. La URL de API en produccion queda como `/api`, lista para usar un backend publicado en el mismo dominio o redirigido por Vercel.

## Limitacion critica

El backend Flask actual guarda la cola de turnos en memoria RAM. Esa arquitectura funciona para una demostracion local con un unico proceso Flask, pero no garantiza estado compartido ni persistente en Vercel Functions.

En Vercel, Flask puede ejecutarse como una Function de Python, pero cada solicitud puede terminar en una instancia diferente o reiniciada. Por eso, usar variables globales en memoria puede provocar:

- turnos reiniciados;
- mesas con estados distintos entre usuarios;
- duplicados bajo concurrencia;
- perdida del estado al escalar, dormir o redeplegar.

## Alternativas viables

### Opcion A: Vercel + Redis/KV

Usar Vercel para frontend y backend serverless, pero mover el estado de turnos a un almacenamiento compartido tipo Redis/KV.

Ventajas:

- funciona con HTTPS publico;
- sincroniza usuarios/dispositivos;
- conserva cola FIFO de forma centralizada;
- se integra bien con Vercel.

Requiere autorizacion porque introduce un servicio de datos externo.

### Opcion B: Flask en un servidor Python persistente

Publicar Angular en Vercel y ejecutar Flask en un servidor Python persistente que mantenga un unico proceso en memoria.

Ventajas:

- conserva Flask y la logica actual casi intacta;
- no requiere base de datos para una demo simple.

Limitaciones:

- si el proceso se reinicia, se pierde el estado;
- requiere un proveedor de backend distinto de Vercel;
- no usar Render, por restriccion del proyecto.

### Opcion C: Solo frontend en Vercel

Publicar unicamente Angular en Vercel.

No cumple el objetivo completo, porque el boton de generar turno no funcionara sin backend publico.

## Decision necesaria

Para publicar LabTurn completo y funcional desde cualquier dispositivo, se necesita elegir una de estas opciones. No se debe desplegar el backend Flask con memoria RAM en Vercel como solucion final porque no cumple el requisito de datos compartidos reales.

