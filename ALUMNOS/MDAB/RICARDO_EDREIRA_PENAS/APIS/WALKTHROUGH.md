# Proyecto X API Post Publisher

## Qué hace este proyecto

Esta aplicación permite publicar posts en X (Twitter) desde una web. Tiene modo desarrollo para probar sin usar la API real, guardar borradores y ver el historial de lo que has publicado.

---

## Características principales

- Publicar en X con validación de 280 caracteres
- Modo desarrollo que simula las publicaciones (no gasta el límite de API)
- Contador en tiempo real
- Modal de confirmación
- Historial guardado localmente
- Gestión de borradores
- Tema oscuro
- Responsive

---

## Tecnologías

- Python 3.11 con Flask
- Tweepy para conectar con X API
- HTML, CSS y JavaScript vanilla
- Almacenamiento en JSON
- Docker para despliegue

---

## Estructura de archivos

```
├── app/
│   ├── config.py         # Carga las credenciales del .env
│   ├── cliente_x.py      # Conexión con X API
│   ├── almacenamiento.py # Guarda en JSON
│   └── rutas.py          # Rutas Flask
├── templates/            # Páginas HTML
├── static/              # CSS y JS
├── Dockerfile
└── requirements.txt
```

---

## Endpoints

- `/` - Página para escribir posts
- `/publicar` - Envía el post
- `/historial` - Ver posts anteriores
- `/borradores` - Gestionar borradores

---

## Cómo funciona

1. El usuario abre la web
2. Escribe el post (máx 280 chars)
3. El JS valida en tiempo real
4. Al publicar, se abre un modal de confirmación
5. Si confirma, se envía a la API de X vía Tweepy
6. Se guarda en el historial local (JSON)

En modo desarrollo, se salta el paso 5 y solo guarda localmente.

---

## Conceptos del curso usados

- **API REST**: Integración con X API
- **OAuth 1.0a**: Autenticación con Tweepy
- **CRUD**: Operaciones con borradores
- **Env variables**: Proteger credenciales

---

## Limitaciones

La API gratuita solo permite 17 posts al día, por eso el modo desarrollo es útil para probar.
