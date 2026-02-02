#  Mastodon Post Publisher

Este proyecto es una aplicación de línea de comandos (CLI) desarrollada en Python que permite publicar "toots" (estados) en la red social Mastodon de forma programática.

Fue creado como solución alternativa al desafío "X API Challenge" debido a las restricciones de pago (Error 402) de la API v2 de X, demostrando flexibilidad para integrar diferentes APIs sociales.

## Características Implementadas

- **Autenticación Segura:** Uso de OAuth2 mediante Access Tokens.
- **Gestión de Secretos:** Protección de credenciales utilizando variables de entorno (`.env`).
- **Publicación de Estado:** Envío de texto plano a la línea de tiempo del usuario.
- **Validación de Input:** Verificación de longitud (máximo 500 caracteres).
- **Manejo de Errores:** Control de excepciones de red y autenticación.
- **Feedback Visual:** Confirmación de éxito con enlace directo al post publicado.

##  Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Librerías:**
  - `Mastodon.py`: Wrapper oficial para interactuar con la API de Mastodon.
  - `python-dotenv`: Para la gestión de variables de entorno.
- **Entorno:** VS Code / Terminal.

##  Prerrequisitos

Antes de empezar, asegúrate de tener:

1. **Python 3.8** o superior instalado.
2. Una cuenta activa en cualquier instancia de **Mastodon** (ej. mastodon.social).
3. `pip` (gestor de paquetes de Python).