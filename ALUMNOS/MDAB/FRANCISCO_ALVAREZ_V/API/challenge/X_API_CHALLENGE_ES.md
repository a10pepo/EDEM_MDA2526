# Desafio X API: Publicador de Posts

## Objetivo

Construye una solucion en **cualquier lenguaje de programacion o framework** que pueda publicar exitosamente un post a traves de la API de X (anteriormente API de Twitter). Este es un desafio abierto disenado para probar tus habilidades de integracion de APIs, creatividad y practicas de desarrollo de software.

## Descripcion general del desafio

**Objetivo Principal:** Crear una aplicacion capaz de publicar al menos un post en X (Twitter).

**Enfoque:** Tienes completa libertad en como implementar esta solucion. Ya sea que construyas una herramienta CLI, aplicacion web, aplicacion movil o servicio automatizado - la eleccion es tuya!

---

## Prerrequisitos y Configuracion

Esta seccion te guiara paso a paso a traves de la configuracion de tus credenciales de la API de X. **Sigue estas instrucciones cuidadosamente** - esta es a menudo la parte mas complicada!

### Paso 1: Crear una cuenta de desarrollador de X

1. **Ve al portal de desarrolladores de X**
   - Visita [developer.x.com](https://developer.x.com)
   - Haz clic en "Sign up" o "Apply for a developer account"

2. **Solicita acceso de desarrollador**
   - Necesitaras una cuenta existente de X (Twitter)
   - Completa el formulario de solicitud:
     - **Caso de uso**: Selecciona "Hobbyist" → "Making a bot"
     - **Descripcion**: Explica que este es un **proyecto estudiantil** para aprender integracion de APIs
     - Ejemplo: *"Soy un estudiante trabajando en un proyecto de curso para aprender como integrar con APIs REST. Construire una aplicacion simple para publicar en X programaticamente como parte de mi curso de desarrollo de APIs."*
   - Se honesto y especifico - las solicitudes vagas pueden ser rechazadas
   - **El nivel gratuito es suficiente** para este desafio

3. **Espera la aprobacion**
   - La aprobacion del nivel gratuito (Essential Access) es instantanea - puedes comenzar inmediatamente
   - El Acceso Elevado (niveles de pago) puede tardar hasta 2 semanas para revision
   - Revisa tu correo electronico para la confirmacion

### Paso 2: Crear un proyecto y aplicacion

Una vez que tu cuenta de desarrollador este aprobada:

1. **Accede al portal de desarrolladores**
   - Ve a [developer.x.com/en/portal/dashboard](https://developer.x.com/en/portal/dashboard)
   - Inicia sesion con tu cuenta de X

2. **Crea un nuevo proyecto** (si no tienes uno)
   - Haz clic en "Create Project"
   - **Nombre del proyecto**: ej., "Proyecto API Estudiante"
   - **Caso de uso**: Selecciona "Making a bot"
   - **Descripcion**: Breve descripcion de tus objetivos de aprendizaje

3. **Crea una aplicacion dentro del proyecto**
   - Haz clic en "Create App" o "+ Add App"
   - **Nombre de la app**: ej., "Post Publisher" (debe ser unico entre todas las apps de X)
   - **Descripcion**: "Proyecto de curso para desarrollo de APIs"
   - Haz clic en "Complete"

4. **Configura los ajustes de la aplicacion**
   - Despues de crear la app, veras el panel de la aplicacion
   - Ve a la pestana "Settings"
   - Desplazate a "User authentication settings" y haz clic en "Set up"

5. **Configura los ajustes de autenticacion** (PASO CRITICO!)

   **Permisos de la aplicacion:**
   - Selecciona **"Read and Write"** (minimo requerido)
   - O selecciona **"Read and Write and Direct Messages"** si quieres acceso completo
   - NO selecciones "Read-only" - no podras publicar!

   **Tipo de aplicacion:**
   - Selecciona **"Web App, Automated App or Bot"**

   **Informacion de la app:**
   - **Callback URI / Redirect URL**: `http://127.0.0.1:3000/callback` (campo requerido, aunque no se usa para tokens pre-generados)
   - **Website URL**: `http://127.0.0.1:5000` o la URL de tu repositorio de GitHub

   Haz clic en "Save"

### Paso 3: Genera tus credenciales de API

Ahora necesitas obtener cuatro credenciales. Asi es como se ve el portal:

![Portal de Desarrolladores de X - Credenciales](./assets/x-api-dev-dashboard.png)

**Necesitas estas cuatro credenciales:**

1. **API Key** (tambien llamada Consumer Key)
2. **API Secret** (tambien llamada Consumer Secret)
3. **Access Token**
4. **Access Token Secret**

#### Encontrando tus credenciales en el portal:

Navega a tu App → pestana **"Keys and Tokens"**. Veras tres secciones:

**Seccion 1: Consumer Keys (API Key y Secret)**
- Haz clic en **"Reveal API Key hint"** o **"Regenerate"** para ver
- Copia ambas:
  - `X_API_KEY` = API Key
  - `X_API_SECRET` = API Secret Key
- **Guarda estas inmediatamente** - no podras ver el secret de nuevo!

**Seccion 2: Authentication Tokens (Access Token y Secret)**
- Esto es lo que necesitas para publicar en X!
- Haz clic en **"Generate"** si aun no has creado tokens
- O haz clic en **"Regenerate"** para crear nuevos
- **CRITICO**: Despues de generar, verifica que diga:

  **"Created with Read, Write, and Direct Messages permissions"**

  (Ve el resaltado rojo en la captura de pantalla arriba)

- Si dice "Read-only permissions", debes:
  1. Volver a App Settings → User authentication settings
  2. Cambiar permisos a "Read and Write"
  3. Guardar
  4. Regresar y **Regenerar** los tokens

- Copia ambos:
  - `X_ACCESS_TOKEN` = Access Token
  - `X_ACCESS_TOKEN_SECRET` = Access Token Secret
- **Guarda estos inmediatamente** - no podras verlos de nuevo!

**Seccion 3: OAuth 2.0 Client ID y Secret**
- NO necesitas estos para este desafio (usamos OAuth 1.0a)
- Puedes ignorar esta seccion

#### Guarda tus credenciales de forma segura

Crea un archivo de texto (temporalmente) o entrada en gestor de contrasenas con:
```
X_API_KEY=tu_api_key_aqui
X_API_SECRET=tu_api_secret_aqui
X_ACCESS_TOKEN=tu_access_token_aqui
X_ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui
```

**NO:**
- Compartas estas con nadie
- Las publiques en Discord/Slack/foros
- Las subas a Git (configuraremos `.gitignore` mas adelante)
- Las incluyas en capturas de pantalla

### Paso 4: Verifica tu configuracion

Antes de comenzar a programar, verifica tus credenciales:

**Lista de verificacion:**
- Tienes las 4 credenciales (API Key, API Secret, Access Token, Access Token Secret)
- Tu Access Token fue creado con permisos **"Read and Write"** o **"Read and Write and Direct Messages"**
- Has guardado las credenciales en algun lugar seguro
- Tu app es parte de un Proyecto en el Portal de Desarrolladores

**Problemas Comunes:**

| Problema | Solucion |
|----------|----------|
| "Read-only permissions" en Access Token | Ve a App Settings → User auth settings → Cambia a "Read and Write" → Regenera tokens |
| No encuentro la pestana "Keys and Tokens" | Asegurate de estar viendo tu App (no el Proyecto). Haz clic en el nombre de tu App. |
| Error "Forbidden" al publicar | Regenera Access Token despues de cambiar permisos |
| Perdi mis credenciales | Puedes regenerarlas en cualquier momento en el portal (pero las antiguas dejan de funcionar) |

### Paso 5: Entiende las limitaciones del nivel gratuito

Tu cuenta gratuita de la API de X tiene estos limites:

**Limites de Posts:**
- 17 posts por 24 horas (~510 posts por mes maximo)
- Subidas basicas de medios (imagenes)

**Restricciones:**
- Operaciones de lectura muy limitadas (timeline, busqueda)
- Sin analiticas o metricas
- Sin API de streaming
- Sin webhooks DESDE X (pero puedes enviar webhooks A tu servicio!)

**Consejo Pro**: Construye tu aplicacion con **modo mock/prueba** primero! Solo conecta a la API real cuando estes seguro de que tu codigo funciona. Esto ahorra tu preciosa cuota de API.

### Paso 6: Prepara tu entorno de desarrollo

Ahora estas listo para programar!

**Elige tus herramientas:**
- Lenguaje de programacion de tu eleccion
- Editor de codigo (VS Code, PyCharm, IntelliJ, etc.)
- Git para control de versiones
- Gestion de variables de entorno (archivos `.env`)

**Lectura recomendada:**
- [Documentacion de X API v2](https://docs.x.com/x-api/getting-started/about-x-api)
- [Endpoint de Manage Posts](https://docs.x.com/x-api/posts/manage-tweets/introduction)
- [Guia de Rate Limits](https://docs.x.com/x-api/fundamentals/rate-limits)

---

## Necesitas Ayuda?

**Si te atascas durante la configuracion:**

1. **Revisa la documentacion de X API**: [developer.x.com/en/docs](https://developer.x.com/en/docs)
2. **Verifica los permisos de tu app**: Deben ser "Read and Write" o superior
3. **Regenera tokens**: Si cambiaste permisos, regenera los Access Tokens
4. **Pregunta a tu instructor**: Trae capturas de pantalla de tu Portal de Desarrolladores (oculta las credenciales!)

**No pases horas atascado en la configuracion** - pide ayuda temprano!

---

## Requisitos principales

Tu solucion **DEBE**:

1. **Autenticarse** con la API de X usando credenciales validas
2. **Publicar un post** exitosamente (minimo 1 caracter, maximo 280 caracteres)
3. **Manejar errores** con elegancia (credenciales invalidas, limites de tasa, errores de red)
4. **Proteger secretos** - Usar variables de entorno o archivos de configuracion seguros
5. **Incluir documentacion** - README con instrucciones de configuracion

---

## Mejoras opcionales

Se te anima a extender tu solucion tanto como puedas! Aqui hay ideas basadas en conceptos que has aprendido a lo largo del curso. **Todas las sugerencias a continuacion son compatibles con el nivel gratuito de la API de X:**

### Mejoras basicas

**Validacion de Entrada y Manejo de Errores** *(Ejercicio 03 - Fundamentos de API)*
- Valida la longitud del post antes de enviar (1-280 caracteres)
- Verifica posts vacios o solo con espacios en blanco
- Valida payloads JSON si estas construyendo un wrapper de API
- Retorna codigos de estado HTTP apropiados (200, 201, 400, 401, 429, 500)
- Maneja errores de limite de tasa de X API (HTTP 429) con elegancia
- Proporciona mensajes de error significativos para ayudarte a depurar problemas

**Feedback al Usuario y Almacenamiento Local**
- Muestra mensaje de confirmacion antes de publicar ("Estas seguro de que quieres publicar esto?")
- Muestra mensaje de exito con marca de tiempo despues de publicar
- Almacena posts publicados localmente (archivo JSON, CSV o en memoria)
- Muestra conteo de llamadas API restantes (rastrea localmente basandote en tu uso)

**Modo de Desarrollo**
- **Modo test/mock**: Permite publicar a un archivo local en lugar de la API de X durante el desarrollo (esto ahorra tu cuota de API!)
- **Flag dry-run**: Vista previa de lo que se publicaria sin realmente publicar
- **Toggle de entorno**: Cambia entre "development" (mock) y "production" (API real)

### Mejoras intermedias

**Construye Tu Propio Wrapper de API** *(Ejercicios 04, 05, 06)*

Ya que no puedes usar las funciones avanzadas de X, construye tu propia API alrededor de la funcionalidad de publicacion de posts! Esto te permite practicar los metodos de autenticacion que aprendiste:

- **Basic Authentication**: Protege tus endpoints de publicacion de posts con Basic Auth (como Ejercicio 04)
- **API Key Authentication**: Genera y valida API keys para tu servicio (como Ejercicio 05)
- **JWT Tokens**: Usa JWT para gestionar sesiones si tienes multiples usuarios (como Ejercicio 06)

**Arquitectura de ejemplo:**
```
Tu Web App (con auth) → Tu Backend API → X API
                ↓
        JWT/API Key/Basic Auth
```

**Operaciones CRUD en Borradores de Posts** *(Ejercicio 08)*

El nivel gratuito de la API de X tiene capacidades de lectura muy limitadas, pero puedes implementar CRUD en **borradores de posts locales**:

- **Create**: Guarda borradores de posts en una base de datos o archivo
- **Read**: Lista todos tus borradores guardados
- **Update**: Edita borradores antes de publicar
- **Delete**: Elimina borradores que no quieres

Una vez que un borrador este listo, publicalo en X!

**Paginacion en Datos Locales** *(Ejercicio 09)*
- Implementa paginacion para tu historial de posts almacenado localmente
- Pagina a traves de borradores guardados
- Usa patrones de paginacion offset/limit o basados en cursor

**Caracteristicas de Entrada Mejoradas**
- **Plantillas de posts**: Formatos predefinidos (ej., "Actualizacion diaria: {contenido}")
- **Sustitucion de variables**: Reemplaza {fecha}, {hora}, {usuario} en plantillas
- **Sugerencias de hashtags**: Agrega automaticamente hashtags configurados
- **Ayudante de hilos**: Divide texto largo en multiples posts de 280 caracteres (almacenados como borradores)

### Mejoras avanzadas

**Sistema de Programacion Local**
- **Programa posts**: Almacena posts con marcas de tiempo futuras en una base de datos local
- **Cron job o programador de tareas**: Verifica posts programados y publica cuando llegue el momento
- **Gestion de cola**: Ve, edita o cancela posts programados
- **Posts recurrentes**: Publica el mismo contenido diaria/semanalmente (util para recordatorios)

**Interfaz Web para Tu Servicio**
- **Frontend**: Construye una UI para componer y publicar posts
- **Gestion de borradores**: Interfaz visual para crear, editar y organizar borradores
- **Calendario de programacion**: Muestra posts programados en una vista de calendario
- **Historial local**: Muestra posts que has publicado (desde tu almacenamiento local)

**Control de Acceso Basado en Roles** *(Ejercicio 10 - Roles y Permisos)*

Si estas construyendo un sistema multiusuario:

- **Multiples roles de usuario**: Admin, Editor, Viewer
- **Niveles de permisos**: Quien puede publicar inmediatamente, quien solo puede guardar borradores, quien puede programar
- **Flujo de aprobacion**: Editores crean borradores, Admins aprueban y publican
- **Restricciones de acceso**: Protege operaciones sensibles basandote en roles de usuario

**Exposicion de API Publica y Webhooks** *(Ejercicio 11 - ngrok)*

Nota: El nivel gratuito de X API no soporta webhooks DESDE X, pero puedes crear webhooks A tu servicio:

- **Expone tu API publicamente**: Usa ngrok para hacer tu publicador de posts accesible a otros
- **Recibe webhooks**: Deja que servicios externos activen posts via tu API (commits de GitHub, envios de formularios, confirmaciones de pago)
- **Publicacion basada en eventos**: Tu servicio recibe webhook → valida → publica en X API

**Flujo de ejemplo:**
```
GitHub Webhook → Tu API (ngrok) → Valida y formatea → Publica en X API
```

**Documentacion de API** *(Ejercicio OpenAPI - Swagger)*
- **OpenAPI/Swagger**: Documenta tus endpoints de API con documentacion interactiva
- **Docs auto-generados**: Usa herramientas como Flask-RESTX, Swagger UI, Redoc, Springdoc
- **Funcion try-it-out**: Permite a usuarios probar tu API directamente desde los docs
- **Solicitudes de ejemplo**: Proporciona payloads de muestra para todos los endpoints

**Generacion de Contenido e Integracion** *(Ejercicio 07 - APIs Publicas)*

Puedes consumir APIs publicas GRATUITAS y publicar sobre sus datos:

- **Actualizaciones del clima**: Obtener de OpenWeatherMap y publicar el clima diario
- **Titulares de noticias**: Obtener noticias de NewsAPI o feeds RSS y publicar resumenes
- **Datos curiosos**: Usar APIs publicas de datos curiosos para publicar contenido interesante
- **Precios de criptomonedas**: Obtener de CoinGecko y publicar actualizaciones de precios
- **Cita del dia**: APIs de citas aleatorias
- **Imagen del dia de NASA**: Publicar contenido de astronomia

**Integracion con Base de Datos**
- **Almacena todo**: Usuarios, borradores, posts programados, historial de posts, estadisticas de uso de API
- **Opciones de base de datos**: SQLite (simple), PostgreSQL, MySQL, MongoDB
- **Uso de ORM**: SQLAlchemy (Python), Sequelize (Node.js), Entity Framework (.NET)
- **Persistencia de datos**: Sobrevive reinicios de aplicacion

**Soporte de Medios**
- **Subidas de imagenes**: Adjunta imagenes a posts (soportado en nivel gratuito con scope media.write)
- **Vista previa de imagen**: Muestra imagen antes de publicar
- **Validacion de imagen**: Verifica tamano de archivo, formato, dimensiones
- **Texto alternativo**: Agrega descripciones de accesibilidad a imagenes
- **Nota**: Los endpoints de subida de medios de X API v2 estan disponibles; los endpoints de medios v1.1 seran deprecados el 9 de junio de 2025

**Testing y Calidad**
- **Tests unitarios**: Prueba tu logica de negocio (validacion, formateo, programacion)
- **Tests de integracion**: Prueba tus endpoints de API (con X API mockeada)
- **Mockea respuestas de X API**: Usa librerias para simular X API durante testing
- **Pipeline CI/CD**: Testing automatizado en commits (GitHub Actions, GitLab CI)

---

## Requisitos de seguridad

**CRITICO: Nunca subas API keys o secretos a tu repositorio!**

### Protegiendo tus credenciales

Has aprendido sobre proteger datos sensibles a lo largo del curso. Aqui esta como aplicarlo:

1. **Usa variables de entorno**
   ```bash
   # Archivo .env de ejemplo (NO SUBAS ESTO)
   X_API_KEY=tu_api_key_aqui
   X_API_SECRET=tu_api_secret_aqui
   X_ACCESS_TOKEN=tu_access_token_aqui
   X_ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui

   # Opcional: Toggle de modo
   APP_MODE=development  # o 'production'
   ```

2. **Agrega `.env` a `.gitignore`**
   ```
   # .gitignore
   .env
   .env.local
   .env.production
   config.json
   secrets.yml
   *.key
   *.pem
   credentials.txt
   x_api_keys.txt
   ```

3. **Proporciona archivos de plantilla**

   Crea `.env.example`:
   ```bash
   # .env.example
   X_API_KEY=tu_api_key_aqui
   X_API_SECRET=tu_api_secret_aqui
   X_ACCESS_TOKEN=tu_access_token_aqui
   X_ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui
   APP_MODE=development
   ```

4. **Documenta la configuracion en README**

   Explica paso a paso:
   - Copia `.env.example` a `.env`
   - Llena tus credenciales reales del Portal de Desarrolladores de X
   - Nunca compartas o subas el archivo `.env`

**Recuerda:** Si accidentalmente subes secretos:
1. **Inmediatamente** revocalos en el Portal de Desarrolladores de X
2. Genera nuevas credenciales
3. Eliminalos del historial de Git usando `git-filter-repo` o BFG Repo-Cleaner
4. Actualiza tu `.gitignore` para prevenir futuros accidentes

### Cargando variables de entorno en tu codigo

Aqui hay ejemplos practicos de como cargar tu archivo `.env` en diferentes lenguajes de programacion:

#### Python

Instala la libreria:
```bash
pip install python-dotenv
```

Carga variables de entorno:
```python
from dotenv import load_dotenv
import os

# Carga variables de entorno desde archivo .env
load_dotenv()

# Accede a tus credenciales
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

# Opcional: Verifica si esta corriendo en modo desarrollo
APP_MODE = os.getenv('APP_MODE', 'production')  # por defecto 'production'

if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
    raise ValueError("Faltan variables de entorno requeridas. Revisa tu archivo .env.")

print(f"Ejecutando en modo {APP_MODE}")
```

#### Notas importantes

- Siempre llama al cargador de dotenv **al inicio** de tu aplicacion
- El archivo `.env` debe estar en el directorio raiz de tu proyecto (mismo nivel que tu script principal)
- Las variables de entorno se cargan en el entorno de tu sistema, no se retornan como un diccionario
- Si una variable ya esta configurada en el entorno de tu sistema, el archivo `.env` no la sobreescribira (en la mayoria de las librerias)

---

## Guias de entrega

### Que incluir

1. **Codigo fuente**
   - Estructura de proyecto bien organizada
   - Nombres claros de archivos y carpetas
   - Codigo limpio y legible siguiendo mejores practicas para tu lenguaje
   - Comentarios explicando la logica

2. **README.md** debe incluir:
   - **Titulo y descripcion del proyecto**
   - **Caracteristicas que implementaste** (listalas claramente)
   - **Tecnologias usadas** (lenguaje, framework, librerias)
   - **Prerrequisitos** (Python 3.x, Node.js, etc.)
   - **Pasos de instalacion** (paso a paso, asume que el lector no sabe nada)
   - **Instrucciones de configuracion** (como configurar `.env`)
   - **Ejemplos de uso** (como ejecutar la app, comandos de ejemplo)
   - **Capturas de pantalla o GIFs** (muestra tu app en accion!)
   - **Conceptos del curso aplicados** (que inspiro tus caracteristicas)
   - **Limitaciones de API** (menciona las restricciones del nivel gratuito que sorteaste)
   - **Problemas conocidos o limitaciones**
   - **Mejoras futuras** (que agregarias con mas tiempo)

3. **Plantilla de configuracion**
   - `.env.example` con todas las variables requeridas
   - Comentarios claros explicando cada variable

4. **Documentacion adicional** (si aplica)
   - Documentacion de endpoints de API (si construiste una API web)
   - Diagramas de arquitectura (como interactuan los componentes)
   - Esquema de base de datos (si usaste una base de datos)
   - Coleccion de Postman (exportala e incluyela!)

### Que NO incluir

- API keys, tokens o secretos reales
- Archivos `.env` con credenciales reales
- Contrasenas o tokens hardcodeados en el codigo
- Informacion personal o direcciones de email
- Cualquier archivo de configuracion sensible
- Archivos de medios grandes o datos de prueba (usa `.gitignore`)
- Carpetas `node_modules/`, `venv/`, `__pycache__/`

---

## Criterios de evaluacion

Tu solucion sera evaluada en:

### Funcionalidad
- Publica posts exitosamente en X?
- Se manejan los errores apropiadamente?
- Funcionan las caracteristicas opcionales como se describen?
- Es la experiencia de usuario fluida e intuitiva?
- Implementaste soluciones alternativas para las limitaciones del nivel gratuito?

### Calidad de codigo
- Es el codigo legible y bien organizado?
- Se siguen las mejores practicas para tu lenguaje/framework elegido?
- Hay manejo de errores y logging apropiados?
- Has aplicado conceptos de los ejercicios del curso?
- Es el codigo modular y mantenible?

### Seguridad
- Estan las credenciales protegidas apropiadamente?
- Esta `.gitignore` configurado correctamente?
- Hay alguna vulnerabilidad de seguridad?
- Has evitado hardcodear datos sensibles?
- Validas la entrada del usuario para prevenir ataques de inyeccion?

### Documentacion
- Es el README claro y completo?
- Puede alguien mas configurar y ejecutar tu proyecto facilmente?
- Estan los pasos de configuracion bien explicados?
- Has documentado que conceptos de los ejercicios usaste?
- Hay ejemplos mostrando como usar tu aplicacion?

---

## Sugerencias de tecnologia

Eres libre de usar cualquier tecnologia, pero aqui hay algunas opciones populares:

### Lenguajes y frameworks
- **Python** - Tweepy, python-twitter, Flask, FastAPI
- **JavaScript/Node.js** - twitter-api-v2, twit, Express, Fastify
- **Java** - Twitter4J, Spring Boot
- **C#/.NET** - Tweetinvi, ASP.NET Core
- **Ruby** - Twitter gem, Sinatra, Rails
- **Go** - go-twitter, anaconda, Gin, Echo
- **PHP** - TwitterOAuth, CodeBird, Laravel

### Librerias utiles
- **Autenticacion** - Librerias OAuth 1.0a u OAuth 2.0 para X API
- **Clientes HTTP** - axios, requests, HttpClient, fetch, curl
- **Variables de Entorno** - dotenv, python-decouple, godotenv
- **Frameworks CLI** - Click (Python), Commander (Node.js), Cobra (Go)
- **Testing** - pytest, jest, JUnit, NUnit, PHPUnit
- **Programacion** - APScheduler (Python), node-cron (Node.js), Quartz (Java)
- **Bases de Datos** - SQLite, PostgreSQL, MongoDB

---

## Recursos utiles

### Documentacion de X API
- [Vision general de X API v2](https://docs.x.com/x-api/getting-started/about-x-api)
- [Endpoint de Manage Posts](https://docs.x.com/x-api/posts/manage-tweets/introduction)
- [Guia de Autenticacion](https://docs.x.com/fundamentals/authentication/oauth-1-0a/api-key-and-secret)
- [Rate Limits](https://docs.x.com/x-api/fundamentals/rate-limits)
- [Proyectos](https://docs.x.com/fundamentals/projects)

### Mejores practicas de seguridad
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Securing API Keys](https://cloud.google.com/docs/authentication/api-keys)

### Herramientas
- [Documentacion de ngrok](https://ngrok.com/docs) - Para exponer tu API local
- [Postman](https://www.postman.com/) - Testing de API
- [Swagger Editor](https://editor.swagger.io/) - Documentacion de API

### APIs publicas gratuitas (para generacion de contenido)
- [OpenWeatherMap](https://openweathermap.org/api) - Datos del clima
- [NewsAPI](https://newsapi.org/) - Titulares de noticias
- [CoinGecko](https://www.coingecko.com/en/api) - Precios de criptomonedas
- [NASA APIs](https://api.nasa.gov/) - Imagenes y datos del espacio

---

## Conectando con conceptos del curso

Mientras construyes tu solucion, piensa en como puedes aplicar lo que has aprendido:

- **Ejercicio 03 (Fundamentos de API)**: Como validaras la entrada y retornaras codigos de estado HTTP apropiados?
- **Ejercicio 04-06 (Autenticacion)**: Si construyes un wrapper de API, que metodo de autenticacion se adapta a tus necesidades?
- **Ejercicio 07 (APIs Publicas)**: Puedes consumir otras APIs gratuitas y publicar sus datos?
- **Ejercicio 08 (CRUD)**: Puedes implementar operaciones CRUD para borradores de posts almacenados localmente?
- **Ejercicio 09 (Paginacion)**: Si almacenas posts localmente, necesitaras paginacion?
- **Ejercicio 10 (Roles y Permisos)**: Tendria sentido el control de acceso basado en roles para un sistema multiusuario?
- **Ejercicio 11 (ngrok y Webhooks)**: Puedes exponer tu API con ngrok y aceptar webhooks de otros servicios?
- **Ejercicio 11-12 (Swagger)**: Ayudaria la documentacion OpenAPI a otros a usar tu API?

**No necesitas usar todos estos conceptos** - elige los que tengan sentido para tu solucion y el tiempo que tengas disponible!

---

## Notas importantes sobre el nivel gratuito

### Rate limits
- Tienes **17 posts por 24 horas** en el nivel gratuito (~510 posts por mes maximo)
- **Planifica tu testing cuidadosamente** - no desperdicies llamadas API durante el desarrollo
- Usa modo mock/test para desarrollo y depuracion
- Esto se traduce en aproximadamente 17 posts de prueba por dia si estas desarrollando activamente

### Estrategia de desarrollo
1. **Construye con modo mock primero**: Haz que tu app funcione sin llamar a X API
2. **Prueba exhaustivamente** con datos mock
3. **Conecta a la API real** solo cuando estes seguro
4. **Monitorea tu uso**: Lleva registro de cuantos posts has publicado
5. **Considera multiples cuentas de prueba** si necesitas mas cuota (revisa los terminos de servicio de X)

### Lo que NO puedes hacer (nivel gratuito)
- Acceder a analiticas o metricas de posts
- Usar API de streaming para posts en tiempo real
- Configurar webhooks DESDE X (Account Activity API)
- Operaciones de lectura extensas (timeline, busqueda)
- Publicacion automatizada de alto volumen

### Lo que SI puedes hacer (nivel gratuito)
- Publicar en X (17 posts por 24 horas)
- Subidas basicas de medios (imagenes soportadas con scope media.write)
- Eliminar tus propios posts (limitado)
- Construir tu propio wrapper de API alrededor de la publicacion de X
- Crear sistemas de programacion y gestion de borradores
- Recibir webhooks A tu servicio
- Integrar con otras APIs gratuitas para contenido

---

## Fecha limite

**Fecha limite de entrega: 20 de diciembre de 2025**

Por favor asegurate de que tu proyecto este completado y entregado para esta fecha. Comienza temprano para permitir tiempo para:
- Configurar tu cuenta de desarrollador de X (la aprobacion es instantanea para el nivel gratuito)
- Aprender la API de X
- Construir y probar tu solucion
- Escribir documentacion
- Resolver cualquier problema

---

## Preguntas Frecuentes

**P: Puedo usar una libreria wrapper en lugar de hacer peticiones HTTP crudas?**
R: Absolutamente! Usar librerias establecidas (como Tweepy para Python o twitter-api-v2 para Node.js) es una mejor practica. No reinventes la rueda. Nota: Usa `tweepy.Client` para X API v2, no el deprecado `tweepy.API`.

**P: Que pasa si accidentalmente subi mis API keys?**
R: Actua inmediatamente:
1. Revocalas en el Portal de Desarrolladores de X
2. Genera nuevas credenciales
3. Eliminalas del historial de Git usando `git-filter-repo` o BFG Repo-Cleaner
4. Agrega reglas apropiadas a `.gitignore`
5. Nunca reutilices credenciales comprometidas

**P: Necesito usar Flask ya que lo hemos usado en el curso?**
R: No! Puedes usar cualquier lenguaje o framework con el que te sientas comodo. Este desafio es agnostico al lenguaje. Muestranos lo que mejor sabes!

**P: Puedo publicar este proyecto en mi GitHub publico?**
R: Si! Este es un gran proyecto para portafolio. Solo asegurate absolutamente de que:
- No hay secretos subidos
- Tu `.gitignore` esta correcto
- Tu README esta completo y profesional

**P: Que pasa si mi solicitud de cuenta de desarrollador de X es rechazada?**
R: Se especifico en tu solicitud sobre usarlo para propositos educativos. Menciona que este es un proyecto de curso. Si es rechazada, contacta a tu instructor para orientacion.

---

## Referencia rapida: Lista de verificacion de configuracion de X API

Usa esto como referencia rapida despues de leer las instrucciones detalladas de configuracion arriba.

### Lista de verificacion de configuracion

**1. Cuenta de Desarrollador de X**
- [ ] Creada cuenta de X (Twitter)
- [ ] Solicitado acceso de desarrollador en [developer.x.com](https://developer.x.com)
- [ ] Cuenta de desarrollador aprobada

**2. Configuracion de Proyecto y App**
- [ ] Creado Proyecto en Portal de Desarrolladores
- [ ] Creada App dentro del Proyecto
- [ ] Nombre de app es unico y descriptivo

**3. Configurar Permisos (CRITICO!)**
- [ ] Ir a App Settings → User authentication settings
- [ ] Configurar permisos a **"Read and Write"** (minimo)
- [ ] Tipo de App: "Web App, Automated App or Bot"
- [ ] Callback URI: `http://127.0.0.1:3000/callback`
- [ ] Website URL: `http://127.0.0.1:5000` o tu repo
- [ ] Clic en "Save"

**4. Generar Credenciales**
- [ ] Navegar a App → pestana "Keys and Tokens"
- [ ] Copiar API Key (Consumer Key)
- [ ] Copiar API Secret (Consumer Secret)
- [ ] Generar Access Token y Secret
- [ ] Verificar que el token muestra "Read, Write, and Direct Messages permissions"
- [ ] Copiar Access Token
- [ ] Copiar Access Token Secret
- [ ] Guardadas las 4 credenciales de forma segura

**5. Seguridad**
- [ ] Credenciales guardadas en gestor de contrasenas o ubicacion segura
- [ ] Creada plantilla `.env.example` en el proyecto
- [ ] Agregado `.env` a `.gitignore`
- [ ] Nunca subidas credenciales reales a Git

**6. Testing**
- [ ] Construida aplicacion con modo mock/test primero
- [ ] Probado con dry-run antes de usar API real
- [ ] Publicado un post de prueba exitosamente
- [ ] Monitoreando uso de API para mantenerse dentro de los limites

### Soluciones rapidas para problemas

| Sintoma | Causa Probable | Solucion Rapida |
|---------|----------------|-----------------|
| "403 Forbidden" al publicar | Permisos incorrectos | Settings → Auth → Cambiar a "Read and Write" → Regenerar tokens |
| "401 Unauthorized" | Credenciales invalidas | Verifica que las 4 credenciales estan correctas, sin espacios extra |
| Advertencia "Read-only permissions" | Tokens generados antes del cambio de permisos | Regenerar Access Token despues de cambiar permisos |
| No encuentro credenciales | Ubicacion incorrecta en el portal | Panel de App → pestana "Keys and Tokens" (no configuracion del Proyecto) |
| Solicitud rechazada | Descripcion vaga | Menciona que es un **proyecto estudiantil** para aprender APIs |
| Tokens no funcionan despues de regenerar | Usando tokens antiguos | Actualiza archivo `.env` con nuevos tokens, los antiguos son invalidados |

### Donde obtener ayuda

1. **Durante la configuracion**: Revisa las instrucciones detalladas en la seccion "Prerrequisitos y Configuracion" arriba
2. **Docs de X API**: [developer.x.com/en/docs](https://developer.x.com/en/docs)
3. **Instructor**: Comparte capturas de pantalla (oculta credenciales!) por email
4. **Companeros**: Discute enfoques, pero no compartas credenciales

---

## Consejos finales

### Comienza simple, luego mejora
1. Haz que la publicacion basica de posts funcione primero (solo un post hardcodeado)
2. Agrega entrada del usuario
3. Prueba exhaustivamente con modo mock
4. Conecta a la API real y publica un post de prueba
5. Luego agrega mejoras una a la vez
6. Prueba despues de cada adicion

### Piensa como un desarrollador
- Como usarias esta herramienta tu mismo todos los dias?
- Que caracteristicas la harian mas util o divertida?
- Como puedes hacer facil para otros configurarla y usarla?
- Que haria de este un gran proyecto para portafolio?

### Seguridad primero
- Revisa tu `.gitignore` antes de **cada** commit
- Revisa tu codigo buscando secretos hardcodeados antes de hacer push
- Nunca compartas credenciales en capturas de pantalla o documentacion
- Usa `git log` y `git diff` para verificar lo que estas subiendo

### Documenta todo
- Tu yo futuro agradecera a tu yo presente por buena documentacion
- Otros deberian poder ejecutar tu proyecto sin hacer preguntas
- Explica POR QUE tomaste ciertas decisiones, no solo QUE construiste
- Incluye capturas de pantalla - la documentacion visual es poderosa

### Gestiona tu cuota de API
- Construye y prueba en modo mock tanto como sea posible
- Solo usa llamadas API reales cuando sea necesario
- Rastrea tu uso manualmente (el nivel gratuito no proporciona buenos dashboards)
- No agotes tu cuota en el dia uno!

---

**Buena suerte, y feliz programacion!**

Muestranos lo que puedes construir con las habilidades que has desarrollado a lo largo de este curso. Esta es tu oportunidad de crear algo practico, aprender una nueva API y mostrar tu aprendizaje a potenciales empleadores.

Recuerda: El objetivo no es la perfeccion - es demostrar que puedes integrar con APIs externas, manejar autenticacion y errores con elegancia, escribir codigo limpio y pensar creativamente sobre soluciones dentro de restricciones.

**Comienza simple, prueba seguido, documenta bien, y lo mas importante - diviertete!**

---

*Ultima actualizacion: Noviembre 2025*
*Compatible con el Nivel Gratuito de X API*
