# Ejercicio 7: Consumo de APIs Públicas Externas

## Objetivo

Aprender a consumir APIs públicas externas e integrar sus datos en tu propia API Flask. Este ejercicio te enseña a trabajar con **múltiples endpoints de API** y a manejar los desafíos reales de integración con APIs.

## Inicio Rápido

```bash
cd exercises/07-public-api
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

---

## Lo Que Aprenderás

Este ejercicio se basa en el Ejercicio 06 (autenticación JWT) y añade:

1. **Consumir APIs Externas** con la librería `requests`
2. **Trabajar con Múltiples Endpoints de API** (Geocodificación + Clima)
3. **Gestionar Claves API** y autenticación con servicios de terceros
4. **Manejo de Errores** para fallos de APIs externas
5. **Parámetros de Consulta** para peticiones API flexibles
6. **Mejores Prácticas Modernas** (coordenadas vs nombres de ciudad obsoletos)

---

## El Reto: Construir una API del Clima

Crearás una API Flask que:
- Usa la **API de Geocodificación de OpenWeatherMap** para convertir nombres de ciudad en coordenadas
- Usa la **API de Clima Actual de OpenWeatherMap** para obtener datos del clima por coordenadas
- Combina ambas APIs para proporcionar información del clima para cualquier ciudad del mundo

### ¿Por Qué Dos Llamadas API?

**Enfoque Moderno (2025):**
```
Solicitud Usuario: "Obtener clima de París"
    ↓
Paso 1: API de Geocodificación
    Ciudad "París" → Coordenadas (48.8566, 2.3522)
    ↓
Paso 2: API del Clima
    Coordenadas → Datos del Clima
    ↓
Respuesta: {temperatura: 15°C, descripción: "nublado", ...}
```

**¿Por qué no usar directamente nombres de ciudad?**
- Las consultas por nombre de ciudad (`?q=Paris`) están **obsoletas** en OpenWeatherMap
- Múltiples ciudades comparten el mismo nombre (París, Francia vs París, Texas)
- Las coordenadas son **inequívocas** y funcionan globalmente
- La geocodificación proporciona contexto de ubicación adicional (país, estado)

---

## Requisitos Previos

### 1. Obtener una Clave API Gratuita de OpenWeatherMap

**Paso a paso:**

1. Ve a [https://openweathermap.org/](https://openweathermap.org/)
2. Haz clic en "Sign Up" en la esquina superior derecha
3. Crea una cuenta gratuita con tu correo electrónico
4. Verifica tu dirección de correo electrónico
5. Inicia sesión y ve a "API Keys" en tu perfil
6. Copia tu clave API predeterminada O genera una nueva
7. **Espera de 10 minutos a 2 horas** para la activación (normalmente instantánea)

**Ejemplo de Clave API:**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### 2. Configurar Tu Clave API

Abre `app.py` y reemplaza:
```python
OPENWEATHER_API_KEY = 'YOUR_API_KEY_HERE'
```

Con tu clave real:
```python
OPENWEATHER_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
```

---

## Estructura de la API

### Endpoints de Autenticación (del Ejercicio 06)

| Método | Endpoint | Auth Requerida | Descripción |
|--------|----------|----------------|-------------|
| POST | `/register` | No | Registrar un nuevo usuario |
| POST | `/login` | No | Login con credenciales JSON, obtener JWT |
| GET | `/profile` | JWT | Obtener perfil de usuario |

### Endpoint del Clima (Nuevo en el Ejercicio 07)

| Método | Endpoint | Auth Requerida | Descripción |
|--------|----------|----------------|-------------|
| GET | `/weather?city=NombreCiudad&country=CC` | **No** | Obtener clima de una ciudad |

**¿Por qué `/weather` es público?**
- El foco del ejercicio es **consumir APIs externas**, no autenticación
- Pruebas más simples (no necesitas hacer login primero)
- Caso de uso del mundo real: Widgets de clima públicos

---

## Cómo Funciona: Flujo de API de Dos Pasos

### Paso 1: API de Geocodificación (Ciudad → Coordenadas)

**Petición:**
```
GET https://api.openweathermap.org/geo/1.0/direct?q=Madrid,ES&appid=YOUR_KEY&limit=1
```

**Respuesta:**
```json
[
  {
    "name": "Madrid",
    "lat": 40.4165,
    "lon": -3.7026,
    "country": "ES",
    "state": "Madrid"
  }
]
```

**Lo que extraes:**
- `lat`: Latitud (40.4165)
- `lon`: Longitud (-3.7026)
- `name`: Nombre oficial de la ciudad
- `country`: Código de país ISO
- `state`: Estado/región (si está disponible)

### Paso 2: API del Clima (Coordenadas → Clima)

**Petición:**
```
GET https://api.openweathermap.org/data/2.5/weather?lat=40.4165&lon=-3.7026&appid=YOUR_KEY&units=metric&lang=es
```

**Respuesta:**
```json
{
  "main": {
    "temp": 18.5,
    "feels_like": 17.2,
    "humidity": 65,
    "pressure": 1013
  },
  "weather": [
    {
      "main": "Clouds",
      "description": "nubes dispersas",
      "icon": "03d"
    }
  ],
  "wind": {
    "speed": 3.5,
    "deg": 180
  },
  "dt": 1678888888
}
```

**Lo que extraes:**
- `temp`: Temperatura en Celsius
- `feels_like`: Temperatura "sensación térmica"
- `humidity`: Porcentaje de humedad
- `description`: Descripción del clima
- `wind.speed`: Velocidad del viento (m/s)

---

## Guía de Implementación

### TODOs en app.py

Necesitas completar **9 espacios estratégicos**:

#### TODOs de Autenticación (del Ejercicio 06):
1. Línea 79: Crear token de acceso JWT
2. Línea 94: Obtener identidad del usuario desde JWT

#### TODOs de API de Geocodificación:
3. Línea 147: Construir URL de geocodificación con consulta y clave API
4. Línea 153: Hacer petición GET a la API de geocodificación
5. Línea 165: Parsear respuesta JSON de la API de geocodificación
6. Línea 178: Extraer latitud de la respuesta
7. Línea 182: Extraer longitud de la respuesta

#### TODOs de API del Clima:
8. Línea 207: Construir URL del clima con coordenadas y clave API
9. Línea 212: Hacer petición GET a la API del clima
10. Línea 223: Parsear respuesta JSON de la API del clima

### Conceptos Clave a Implementar

**1. Construir URLs de API:**
```python
# Formato de URL de API de Geocodificación
url = f'{GEOCODING_API_URL}?q={query}&appid={API_KEY}&limit=1'

# Formato de URL de API del Clima
url = f'{WEATHER_API_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=es'
```

**2. Hacer Peticiones HTTP:**
```python
import requests

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Procesar datos
else:
    # Manejar error
```

**3. Manejo de Errores:**
```python
try:
    response = requests.get(url)
    data = response.json()
except requests.exceptions.RequestException as e:
    # Error de red
except (KeyError, ValueError) as e:
    # Formato de respuesta inválido
```

---

## Probando la API

### 1. Probar Sin Clave API (Debería Fallar)

```bash
curl http://127.0.0.1:5000/weather?city=Madrid
```

**Respuesta Esperada:**
```json
{
  "error": "OpenWeatherMap API key not configured",
  "message": "Please set OPENWEATHER_API_KEY in app.py",
  "help": "Get a free API key at https://openweathermap.org/api"
}
```

### 2. Probar Con Clave API - Ciudad Predeterminada

```bash
curl http://127.0.0.1:5000/weather
```

**Respuesta Esperada (Madrid, predeterminada):**
```json
{
  "location": {
    "city": "Madrid",
    "country": "ES",
    "state": "Madrid",
    "coordinates": {
      "latitude": 40.4165,
      "longitude": -3.7026
    }
  },
  "weather": {
    "temperature": 18.5,
    "feels_like": 17.2,
    "humidity": 65,
    "pressure": 1013,
    "description": "nubes dispersas",
    "main": "Clouds",
    "icon": "03d"
  },
  "wind": {
    "speed": 3.5,
    "direction": 180
  },
  "timestamp": 1678888888
}
```

### 3. Probar Diferentes Ciudades

```bash
# París, Francia
curl http://127.0.0.1:5000/weather?city=Paris&country=FR

# Londres, Reino Unido
curl http://127.0.0.1:5000/weather?city=London&country=GB

# Nueva York, EE.UU.
curl http://127.0.0.1:5000/weather?city=New%20York&country=US

# Tokio, Japón
curl http://127.0.0.1:5000/weather?city=Tokyo&country=JP
```

**Nota:** Usa `%20` para espacios en URLs, o usa comillas en curl:
```bash
curl "http://127.0.0.1:5000/weather?city=New York&country=US"
```

### 4. Probar Nombres de Ciudad Ambiguos

**Sin código de país:**
```bash
curl http://127.0.0.1:5000/weather?city=Paris
# Retorna: París, Francia (más común)
```

**Con código de país:**
```bash
curl "http://127.0.0.1:5000/weather?city=Paris&country=US"
# Retorna: París, Texas, EE.UU.
```

### 5. Probar Ciudad Inválida (Debería Fallar)

```bash
curl http://127.0.0.1:5000/weather?city=InvalidCityXYZ
```

**Respuesta Esperada:**
```json
{
  "error": "City not found",
  "message": "Could not find coordinates for city: InvalidCityXYZ",
  "suggestion": "Try adding a country code, e.g., ?city=Paris&country=FR"
}
```

---

## Entendiendo la Librería `requests`

### Instalación

```bash
pip install requests
```

### Uso Básico

```python
import requests

# Petición GET
response = requests.get('https://api.example.com/data')

# Verificar estado
if response.status_code == 200:
    print("¡Éxito!")

# Parsear JSON
data = response.json()

# Acceder a datos
print(data['key'])
```

### Con Parámetros de Consulta

**Método 1: String de URL**
```python
url = f'https://api.example.com/data?param1={value1}&param2={value2}'
response = requests.get(url)
```

**Método 2: Diccionario de parámetros (más limpio)**
```python
params = {'param1': value1, 'param2': value2}
response = requests.get('https://api.example.com/data', params=params)
```

### Manejo de Errores

```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Lanza excepción para 4xx/5xx
    data = response.json()
except requests.exceptions.Timeout:
    print("Tiempo de espera agotado")
except requests.exceptions.ConnectionError:
    print("Error de red")
except requests.exceptions.HTTPError as e:
    print(f"Error HTTP: {e}")
except ValueError:
    print("Respuesta JSON inválida")
```

---

## Problemas Comunes y Soluciones

### Problema 1: Clave API No Activada

**Síntoma:**
```json
{
  "cod": 401,
  "message": "Invalid API key"
}
```

**Solución:**
- Espera de 10 minutos a 2 horas para la activación
- Verifica que copiaste la clave completa (sin espacios)
- Comprueba que estás usando la clave correcta de tu cuenta de OpenWeatherMap

### Problema 2: Ciudad No Encontrada

**Síntoma:**
```json
{
  "error": "City not found",
  "message": "Could not find coordinates for city: Madrd"
}
```

**Solución:**
- Verifica la ortografía: "Madrd" → "Madrid"
- Añade código de país para desambiguación
- Usa nombres de ciudad en inglés (ej: "Munich" no "München")

### Problema 3: Timeout de Red

**Síntoma:**
```
Error: Could not connect to Geocoding API
```

**Solución:**
- Verifica la conexión a internet
- Comprueba que la API de OpenWeatherMap no esté caída: [status.openweathermap.org](https://status.openweathermap.org/)
- Intenta de nuevo en unos segundos

### Problema 4: Límite de Tasa

**Límites del nivel gratuito:**
- 60 llamadas por minuto
- 1,000,000 llamadas por mes

**Si alcanzas el límite:**
```json
{
  "cod": 429,
  "message": "Too many requests"
}
```

**Solución:**
- Espera 60 segundos
- Implementa caché (objetivo adicional)
- Actualiza a nivel de pago si es necesario

---

## Criterios de Aceptación

Tu implementación debería:

- ✅ Llamar exitosamente a la API de Geocodificación de OpenWeatherMap
- ✅ Llamar exitosamente a la API de Clima Actual de OpenWeatherMap
- ✅ Manejar validación de clave API
- ✅ Manejar errores de ciudad no encontrada
- ✅ Manejar errores de red con gracia
- ✅ Parsear respuestas JSON correctamente
- ✅ Retornar datos de clima estructurados
- ✅ Soportar parámetro opcional de código de país
- ✅ Usar HTTPS (no HTTP) para llamadas API
- ✅ Usar coordenadas (no consultas por nombre de ciudad obsoletas)

---

## Objetivos Adicionales

Una vez completes la implementación básica:

### 1. Añadir Caché de Respuestas

Evitar llamadas API repetidas para la misma ciudad:

```python
from datetime import datetime, timedelta

weather_cache = {}  # {ciudad: {datos: {...}, expira: timestamp}}

def get_cached_weather(city):
    if city in weather_cache:
        if weather_cache[city]['expires'] > datetime.now():
            return weather_cache[city]['data']
    return None

def cache_weather(city, data, ttl_minutes=10):
    weather_cache[city] = {
        'data': data,
        'expires': datetime.now() + timedelta(minutes=ttl_minutes)
    }
```

### 2. Añadir Más Endpoints del Clima

```python
# Pronóstico de 5 días
@app.route('/weather/forecast', methods=['GET'])
def forecast():
    # Usar: https://api.openweathermap.org/data/2.5/forecast
    pass

# Calidad del aire
@app.route('/weather/air-quality', methods=['GET'])
def air_quality():
    # Usar: https://api.openweathermap.org/data/2.5/air_pollution
    pass
```

### 3. Añadir Iconos del Clima

Retornar URLs de iconos para visualización en frontend:

```python
weather_info['weather']['icon_url'] = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
```

### 4. Añadir Conversión de Unidades de Temperatura

```python
@app.route('/weather', methods=['GET'])
def weather():
    units = request.args.get('units', 'metric')  # metric, imperial, standard
    # Usar en llamada API: &units={units}
```

### 5. Proteger Endpoint del Clima con JWT

Hacer que el endpoint del clima requiera autenticación:

```python
@app.route('/weather', methods=['GET'])
@jwt_required()  # Añadir este decorador
def weather():
    current_user = get_jwt_identity()
    # Rastrear consultas de clima del usuario para analíticas
```

---

## Entendiendo la Obsolescencia de APIs

**⚠️ Nota Importante Sobre Cambios en OpenWeatherMap**

OpenWeatherMap ha marcado como obsoletas las consultas por nombre de ciudad:

**Forma Antigua (Obsoleta, pero aún funciona):**
```python
# Consulta directa por nombre de ciudad - NO RECOMENDADA
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
```

**Problemas:**
- Ya no se mantiene activamente
- Correcciones de bugs no garantizadas
- Puede eliminarse en versiones futuras
- Ambigua para ciudades con el mismo nombre

**Forma Nueva (Recomendada):**
```python
# Paso 1: Geocodificar
geocoding_url = f'https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}'
# Obtener coordenadas

# Paso 2: Clima por coordenadas
weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
```

**Beneficios:**
- Mantenida activamente
- Resultados inequívocos
- Mejores mensajes de error
- A prueba de futuro
- Contexto de ubicación adicional

**¡Este ejercicio enseña la forma NUEVA!**

---

## Recursos Adicionales

### Documentación de OpenWeatherMap

- [API de Clima Actual](https://openweathermap.org/current)
- [API de Geocodificación](https://openweathermap.org/api/geocoding-api)
- [Guía de Clave API](https://openweathermap.org/appid)
- [FAQ](https://openweathermap.org/faq)

### Librería requests de Python

- [Documentación Oficial](https://requests.readthedocs.io/)
- [Guía de Inicio Rápido](https://requests.readthedocs.io/en/latest/user/quickstart/)

### Códigos de País ISO

- [Códigos ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- Ejemplos: ES (España), FR (Francia), US (Estados Unidos), GB (Reino Unido)

---

## Resumen

**Conclusiones Clave:**

1. **Consumo de APIs Externas**
   - Usa la librería `requests` para llamadas HTTP
   - Parsea respuestas JSON con `.json()`
   - Maneja errores con gracia

2. **Flujos de Trabajo de API Multipaso**
   - Algunas tareas requieren múltiples llamadas API
   - Geocodificación → Coordenadas → Clima
   - Encadena respuestas juntas

3. **Mejores Prácticas de API**
   - Usa HTTPS, no HTTP
   - Sigue recomendaciones actuales (coordenadas vs nombres de ciudad)
   - Valida claves API antes de hacer peticiones
   - Maneja límites de tasa y errores

4. **Integración del Mundo Real**
   - Claves API y autenticación de terceros
   - Parámetros de consulta para peticiones flexibles
   - Respuestas de error estructuradas
   - Extracción comprehensiva de datos

5. **Construyendo sobre Conocimiento Previo**
   - Autenticación JWT (Ejercicio 06)
   - Enrutamiento Flask y manejo de errores
   - Respuestas JSON
   - ¡Ahora añadiendo: Consumo de APIs externas!

**Próximos Pasos:**
- **Ejercicio 08**: Operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
- **Ejercicio 09**: Paginación de API
- **Ejercicio 10**: Control de Acceso Basado en Roles (RBAC)

¡Buena suerte! 🌤️
