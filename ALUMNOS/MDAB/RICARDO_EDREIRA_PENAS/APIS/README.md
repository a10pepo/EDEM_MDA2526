# X API Post Publisher

Aplicación web para publicar posts en X (Twitter) usando Python y Flask.

**Autor:** Ricardo Edreira Penas  
**Proyecto:** X API Challenge - Enero 2026

---

## Descripción

Aplicación web que permite publicar tweets en X de forma sencilla. Tiene gestión de borradores, historial y modo desarrollo para probar sin gastar el límite de la API.

---

## Características

- Publicar posts en X (hasta 280 caracteres)
- Modo desarrollo que simula las publicaciones
- Contador de caracteres en tiempo real
- Confirmación antes de publicar
- Historial de posts publicados
- Guardar borradores
- Interfaz oscura moderna
- Funciona en móvil y tablet
- Usa Docker para el despliegue

---

## Tecnologías Usadas

| Categoría | Tecnología |
|-----------|------------|
| Backend | Python 3.11 + Flask |
| API | Tweepy (X API v2) |
| Frontend | HTML5, CSS3, JavaScript |
| Almacenamiento | JSON |
| Contenedores | Docker |

---

## Estructura

```
├── app/                     # Backend Python
├── static/                  # CSS y JS
├── templates/               # HTML
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Instalación

### Con Docker

```bash
# Clonar
git clone https://github.com/RicardoEdreiraPenas/x-post-publisher.git
cd x-post-publisher

# Configurar .env
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar
docker-compose up --build

# Abrir http://localhost:5000
```

### Sin Docker

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Ejecutar
python run.py
```

---

## Configuración

### Credenciales de X API

1. Ir a [X Developer Portal](https://developer.x.com)
2. Crear proyecto y aplicación
3. Configurar permisos: "Read and Write"
4. Copiar las 4 credenciales

### Archivo .env

```bash
X_API_KEY=tu_api_key
X_API_SECRET=tu_api_secret
X_ACCESS_TOKEN=tu_access_token
X_ACCESS_TOKEN_SECRET=tu_access_token_secret

# development = pruebas | production = real
APP_MODE=development
```

---

## Uso

1. Abrir la app en el navegador
2. Escribir el mensaje
3. Ver el contador de caracteres
4. Hacer clic en Publicar
5. Confirmar

También se pueden guardar borradores para publicar después.

---

## Docker

```bash
# Ejecutar
docker-compose up

# Detener
docker-compose down

# Ver logs
docker-compose logs -f
```

---

## Conceptos Aplicados del Curso

- Fundamentos de API (validación, errores HTTP)
- OAuth 1.0a para autenticación
- CRUD para los borradores
- Variables de entorno para proteger credenciales
- Docker para despliegue

---

## Limitaciones

- API gratuita permite 17 posts/día
- Modo desarrollo no gasta límite

---

## Problemas Comunes

| Error | Solución |
|-------|----------|
| 401 | Revisar credenciales |
| 403 | Cambiar permisos en X Developer |
| 402 | Usar modo development |

---

## Documentación

- `WALKTHROUGH.md` - Descripción del proyecto
- `GUIA_DESARROLLO.md` - Cómo se hizo

---

**Ricardo Edreira Penas**  
GitHub: @RicardoEdreiraPenas
