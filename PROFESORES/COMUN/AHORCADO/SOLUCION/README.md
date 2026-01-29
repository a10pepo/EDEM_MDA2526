A continuación podéis encontrar la solución al juego del ahorcado implementado en Python.

El código está estructurado de la siguiente manera:

SOLUCION A: En esta solución haremos el desarrollo con las siguientes conditiones
- Usaremos Docker compose con volumenes en lugar de contenedor
- Pasaremos el fichero de palabras.txt estático en el fichero

```bash
docker compose up
```

SOLUCION B: En esta solución haremos el desarrollo con las siguientes conditiones
- Usaremos Docker compose con un contenedor creado

OPCION 1:
```bash
docker build -t ahorcado:latest .
docker compose up
```

OPCION 2:
```bash
docker compose build
docker compose up
```

SOLUCION C: En esta solución haremos el desarrollo con las siguientes conditiones
- Usaremos Docker compose con un contenedor creado
- Pasaremos el fichero de palabras.txt dinámicamente al contenedor

```bash
docker compose build
docker compose up
```

SOLUCION D: En esta solución haremos el desarrollo con las siguientes conditiones
- Usaremos Docker compose con un contenedor creado
- Pasaremos el fichero de palabras.txt dinámicamente al contenedor
- Implementaremos el acceso a la api de RAE (En el fichero .env se añade la variable MODE=API)

```bash
docker compose build
docker compose up
```
