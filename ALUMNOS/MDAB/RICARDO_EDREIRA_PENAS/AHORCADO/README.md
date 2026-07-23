# Ahorcado — Ricardo Edreira Peñas

Juego del ahorcado en Python con persistencia en PostgreSQL, contenerizado con Docker.

## Descripción

La aplicación carga una lista de palabras desde `palabras.txt`, itera sobre el alfabeto español para adivinar cada palabra y guarda los resultados (letras acertadas, falladas, intentos y timestamp) en una base de datos PostgreSQL.

## Estructura

```
AHORCADO_Ricardo_Edreira/
├── ahorcado.py          # Lógica principal del juego
├── palabras.txt         # Lista de palabras (10 palabras en español)
├── requirements.txt     # Dependencias Python
├── Dockerfile           # Imagen de la aplicación
├── docker-compose.yml   # Orquestación de app + base de datos
├── .env.example         # Variables de entorno (plantilla)
└── .gitignore
```

## Cómo ejecutar

1. Copia el fichero de variables de entorno:
   ```bash
   cp .env.example .env
   ```

2. Edita `.env` con tus credenciales si lo deseas.

3. Levanta los servicios:
   ```bash
   docker compose up --build
   ```

La app espera a que PostgreSQL esté listo antes de conectarse. Los resultados quedan guardados en la tabla `resultados`.

## Autor

Ricardo Edreira Peñas — EDEM MDA 2025/26
