# Pokémon Tweet Bot - Entregable API-X

## Datos del Autor

- **Nombre:** Javier Aguado
- **Proyecto:** Entregable API-X
- **Fecha:** Enero 2026
- **GitHub:** [GitHub](https://github.com/javieri21)

---

**Un bot automatizado que publica información detallada de Pokémon en Twitter cada 90 minutos usando APIs REST.**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Twitter API](https://img.shields.io/badge/Twitter%20API-v2-1DA1F2)
![PokéAPI](https://img.shields.io/badge/PokéAPI-REST-yellow)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)

---

## Descripción del Proyecto

**Pokémon Tweet Bot** es una aplicación que automatiza la publicación de información sobre Pokémon en Twitter. El bot consulta la **PokéAPI** para obtener datos de Pokémon (tipos, debilidades, fortalezas) y publica tweets con imágenes cada 15 minutos, manteniendo un registro del último Pokémon publicado para continuar desde donde quedó.

**Ideal para:**
- Mantener una cuenta de Twitter activa con contenido automático
- Compartir información Pokémon regularmente
- Aprender sobre integración de múltiples APIs
- Practicar Docker y lo aprendido en clase

---

## Características Implementadas

- ✅ **Automatización temporal**: Publica un tweet cada 90 minutos sin intervención manual
- ✅ **Integración PokéAPI**: Obtiene datos dinámicos de más de 1000 Pokémon
- ✅ **Integración Twitter API v2**: Publica tweets con imágenes usando tweepy
- ✅ **Información enriquecida**: Incluye tipo, debilidades, fortalezas y ejemplos de Pokémon relacionados
- ✅ **Manejo de errores robusto**: Diferenciación de excepciones (429 Rate Limit, timeouts, conexión)
- ✅ **Modo desarrollo/producción**: Simula publicaciones sin consumir API quota
- ✅ **Persistencia de estado**: Recuerda el último Pokémon publicado entre ejecuciones
- ✅ **Control Ctrl+C**: Parada elegante del programa con validación de credenciales
- ✅ **Dockerizado**: Ejecutable en contenedor con volúmenes persistentes
- ✅ **Validación de límites Twitter**: Trunca mensajes que superen 280 caracteres
- ✅ **Historial local**: Guarda registro de tweets publicados en `mis_tweets.json`

---

## Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.11+ | Lenguaje principal |
| **tweepy** | 4.14.0 | Cliente oficial de Twitter API v2 |
| **requests** | 2.31.0 | Peticiones HTTP a PokéAPI |
| **python-dotenv** | 0.9.9 | Gestión de variables de entorno |
| **Docker** | Latest | Containerización |
| **Docker Compose** | 3.8+ | Orquestación |

---

## Requisitos Previos

### Instalación Local
- **Python 3.11 o superior**
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para clonar el repositorio)
- **Credenciales de Twitter API v2** ([developer.x.com](https://developer.x.com/en))

---

## Instalación

### Opción 1: Ejecución Local

#### Paso 1: Clonar o descargar el proyecto
```bash
git clone <tu-repositorio>
cd Entregable-API-X
```

#### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Paso 3: Configurar variables de entorno
```bash
cp .env.example .env
```

#### Paso 4: Ejecutar la aplicación
```bash
python XPokemonAPI.py
```

---

### Opción 2: Ejecución con Docker

#### Paso 1: Clonar el proyecto
```bash
git clone <tu-repositorio>
cd Entregable-API-X
```

#### Paso 2: Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

#### Paso 3: Construir e iniciar con Docker Compose
```bash
docker-compose up --build
```

#### Paso 4: Para detener el contenedor
```bash
docker-compose down -v
```

---

## Configuración

### Archivo `.env`

Crea un archivo `.env` en la raíz del proyecto (copia de `.env.example`):

```dotenv
# Credenciales de Twitter API v2
API_KEY=tu_api_key_aqui
API_SECRET_KEY=tu_api_secret_aqui
ACCESS_TOKEN=tu_access_token_aqui
ACCESS_TOKEN_SECRET=tu_access_token_secret_aqui

# Modo de ejecución
APP_MODE=production    # Cambia a 'development' para modo simulación sin publicar en X
```

---

### Resultado Esperado modo Development
```
¡Conoce a Pikachu [25]!
Tipo: Electric

Debilidades: Ground
Ejemplos: Dugtrio [51]

Fortalezas: Flying, Water
Ejemplos: Pidgeot [18]

Tweet publicado con éxito. ID: 1234567890
[Esperando 90 minutos para próxima publicación...]
```

### Detener el Bot
```bash
# Presiona Ctrl+C en la consola
⛔ Programa interrumpido por el usuario (Ctrl+C)
```

### Ver Historial de Tweets
```bash
cat mis_tweets.json
```

### Ver Último Pokémon Publicado
```bash
cat last_pokemon_id.txt
```

---

## 🎓 Conceptos Aplicados del Curso

### 1. **Integración de APIs REST**
   - Consumo de PokéAPI (datos de Pokémon)
   - Consumo de Twitter API v2 (publicaciones)

### 2. **Manejo de Errores y Excepciones**
   - Try-catch selectivo con múltiples tipos de excepción

### 3. **Programación Asincrónica y Temporal**
   - Bucles infinitos con `time.sleep()`
   - Control de interrupciones (`KeyboardInterrupt`)
   - Gestión de timeouts en requests (10 segundos)

### 4. **Seguridad y Secretos**
   - Variables de entorno con `python-dotenv`
   - Separación de configuración en `.env`

### 5. **Persistencia de Datos**
   - Lectura/escritura de archivos

### 6. **Containerización y DevOps**
   - Dockerfile optimizado
   - Docker Compose para orquestación

---

##  Limitaciones de las APIs

### PokéAPI (Gratuita - No tiene límite de rate)
| Aspecto | Límite |
|--------|--------|
| Pokémon disponibles | 1,025+ |

### Twitter API v2 (Tier Gratuito)
| Aspecto | Límite |
|--------|--------|
| Tweets por dia | 17 |
| Imágenes | ✅ Soportado |

---

## Problemas Conocidos y Limitaciones

### 1. **Límite de Rate (429) en Twitter**
   - **Problema**: Si publicas demasiado rápido, Twitter devuelve error 429
   - **Solución**: Publicar cada cierto tiempo = 90 min

### 2. **Truncamiento de mensajes**
   - **Problema**: Tweets muy largos se cortan a 280 caracteres
   - **Solución**: Se truncan con "..." al exceder límite

---

## Mejoras Futuras

### Corto Plazo
- [ ] Almacenar datos en **PostgreSQL** en lugar de archivos

### Largo Plazo
- [ ] Análisis de **engagement** en Twitter (retweets, likes)

---