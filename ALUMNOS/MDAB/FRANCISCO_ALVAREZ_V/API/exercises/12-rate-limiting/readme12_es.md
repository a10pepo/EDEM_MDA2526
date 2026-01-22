# Ejercicio 12: Limitación de Tasa y Seguridad de API

## Inicio Rápido

```bash
cd exercises/12-rate-limiting
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Objetivo

Aprende a proteger tu API del abuso usando **limitación de tasa** con Flask-Limiter:

- **Prevenir Abuso**: Protege tu API de usuarios maliciosos y bots
- **Gestión de Recursos**: Controla la carga del servidor y previene el agotamiento de recursos
- **Uso Justo**: Asegura que todos los usuarios tengan acceso equitativo a tu API
- **Seguridad**: Previene ataques de fuerza bruta en endpoints de autenticación
- **Control de Costos**: Limita operaciones costosas (consultas de base de datos, llamadas a API externas)

## ¿Qué es la Limitación de Tasa?

La **limitación de tasa** restringe el número de solicitudes que un cliente puede hacer a tu API dentro de una ventana de tiempo específica.

**Ejemplos del mundo real:**
- **Twitter API**: 300 solicitudes por 15 minutos (nivel gratuito)
- **GitHub API**: 60 solicitudes por hora (no autenticado), 5000/hora (autenticado)
- **Stripe API**: 100 solicitudes por segundo
- **OpenAI API**: Varía según el plan y endpoint

**Por qué importa la limitación de tasa:**
1. **Previene ataques DoS**: Los usuarios maliciosos no pueden saturar tu servidor
2. **Detiene fuerza bruta**: Limita los intentos de adivinación de contraseñas
3. **Controla costos**: Previene que operaciones costosas agoten recursos
4. **Asegura disponibilidad**: Protege la API para todos los usuarios legítimos
5. **Cumplimiento**: Algunas regulaciones requieren limitación de tasa (ej., APIs de pago)

## Prerequisitos

Antes de comenzar este ejercicio, completa:
- **Ejercicio 06**: Autenticación JWT (este ejercicio se basa en conceptos JWT)
- **Ejercicio 03**: Fundamentos de API (comprensión de códigos de estado HTTP)

## Lo que Aprenderás

1. **Biblioteca Flask-Limiter**: Estándar de la industria para limitación de tasa en Flask
2. **Estrategias de limitación de tasa**:
   - Por dirección IP (predeterminado)
   - Por usuario (solicitudes autenticadas)
   - Por endpoint (límites diferentes para diferentes rutas)
3. **Código de estado HTTP 429**: "Demasiadas Solicitudes"
4. **Cabeceras de límite de tasa**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`
5. **Patrones de decoradores**: `@limiter.limit()`, `@limiter.exempt`
6. **Manejadores de errores personalizados**: Mensajes amigables de límite de tasa
7. **Mejores prácticas de seguridad**: Proteger endpoints sensibles

## Instalación

El ejercicio requiere estas dependencias (ya en `requirements.txt`):

```txt
Flask==3.0.0
Werkzeug==3.0.1
Flask-JWT-Extended==4.6.0
Flask-Limiter==3.5.0
```

Instálalas:
```bash
pip install -r requirements.txt
```

## Cómo Funciona Flask-Limiter

### Concepto Básico

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Identificar clientes por dirección IP
    default_limits=["200 per day", "50 per hour"]  # Aplicado a todas las rutas
)
```

**Componentes clave:**
- `key_func`: Cómo identificar clientes (dirección IP, ID de usuario, clave API, etc.)
- `default_limits`: Límites de respaldo aplicados a todas las rutas a menos que se sobrescriban
- `storage_uri`: Dónde almacenar datos de límite de tasa (memoria, Redis, etc.)

### Sintaxis de Límite de Tasa

Flask-Limiter usa un formato de cadena intuitivo:

```python
"5 per minute"     # 5 solicitudes por minuto
"100 per hour"     # 100 solicitudes por hora
"1000 per day"     # 1000 solicitudes por día
"1 per second"     # 1 solicitud por segundo
"10/minute"        # Sintaxis alternativa (igual que "10 per minute")
```

**Puedes combinar límites:**
```python
@limiter.limit("5 per minute;100 per hour;1000 per day")
```

Esto aplica TODOS los límites simultáneamente - el que se alcance primero activa el límite de tasa.

## Estructura del Ejercicio

El `app.py` proporcionado tiene una API parcialmente completa con TODOs:

- `app.py` - Archivo de inicio con espacios en blanco para completar
- `example/example12.py` - Solución de referencia completa
- `requirements.txt` - Dependencias
- `readme12_es.md` - Este archivo de instrucciones

## Parte 1: Comprendiendo la Estructura del Código (10 minutos)

### Paso 1.1: Revisar la Configuración

Abre `app.py` y examina la configuración:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=_____,  # TODO: ¿Qué identifica al cliente?
    default_limits=_____  # TODO: Establecer límites predeterminados razonables
)
```

**Tu tarea:**
1. Completa `key_func` con `get_remote_address` (rastrea por dirección IP)
2. Completa `default_limits` con `["200 per day", "50 per hour"]`

**¿Por qué estos valores predeterminados?**
- `200 per day`: Previene que una sola IP haga miles de solicitudes
- `50 per hour`: Control más granular dentro del límite diario
- Ambos límites se aplican - alcanzar cualquiera activa la limitación de tasa

### Paso 1.2: Entender la Función Clave

El parámetro `key_func` determina **quién** está haciendo la solicitud.

**Estrategias comunes:**

```python
# Estrategia 1: Por dirección IP (simple, funciona para solicitudes no autenticadas)
from flask_limiter.util import get_remote_address
key_func=get_remote_address

# Estrategia 2: Por usuario autenticado (requiere JWT/sesión)
def get_user_id():
    try:
        return get_jwt_identity()  # Nombre de usuario JWT
    except:
        return get_remote_address()  # Recurrir a IP si no está autenticado

key_func=get_user_id
```

Para este ejercicio, usaremos **dirección IP** ya que es más simple y funciona tanto para endpoints autenticados como no autenticados.

## Parte 2: Implementando Límites de Tasa (30 minutos)

### Tarea 2.1: Proteger Endpoint de Registro

Los endpoints de registro son a menudo objetivo de bots que crean cuentas de spam.

**Encuentra este código en `app.py`:**

```python
@app.route('/register', methods=['POST'])
@limiter.limit(_____)  # TODO: Agregar límite de tasa
def register():
    # ... lógica de registro
```

**Tu tarea:**
Completa el espacio en blanco con: `"5 per hour"`

**¿Por qué 5 por hora?**
- Los usuarios legítimos rara vez necesitan crear múltiples cuentas
- Previene el registro automático de bots
- Aún permite a un usuario reintentar si comete un error

**Prueba:**
```bash
# Intenta registrarte 6 veces en rápida sucesión - la sexta debería fallar
for i in {1..6}; do
  curl -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"user$i\",\"password\":\"pass123\"}"
  echo ""
done
```

**Esperado:** Las primeras 5 tienen éxito, la sexta devuelve HTTP 429 (Límite de tasa excedido)

### Tarea 2.2: Proteger Endpoint de Login

Los endpoints de login son objetivos principales para **ataques de fuerza bruta** (probar muchas contraseñas).

**Encuentra este código:**

```python
@app.route('/login', methods=['POST'])
@limiter.limit(_____)  # TODO: Prevenir fuerza bruta
def login():
    # ... lógica de login
```

**Tu tarea:**
Completa con: `"10 per minute"`

**¿Por qué 10 por minuto?**
- Permite a usuarios legítimos reintentar contraseñas incorrectas
- Previene adivinación automática de contraseñas
- Estándar de la industria para endpoints de autenticación

**Comparación del mundo real:**
- **GitHub**: 5 intentos fallidos activan CAPTCHA
- **AWS**: Ralentiza después de 5 intentos fallidos
- **Google**: Usa limitación de tasa adaptativa (ralentiza después de fallas)

### Tarea 2.3: Endpoint de API General

La mayoría de los endpoints de API necesitan limitación de tasa moderada.

**Encuentra este código:**

```python
@app.route('/api/data', methods=['GET'])
@jwt_required()
@limiter.limit(_____)  # TODO: Límite estándar de API
def get_data():
    # ... lógica de recuperación de datos
```

**Tu tarea:**
Completa con: `"20 per minute"`

**¿Por qué 20 por minuto?**
- Permite uso normal de la aplicación
- Previene que un solo usuario sature el servidor
- Equilibra usabilidad con protección

### Tarea 2.4: Operaciones Costosas

Algunos endpoints consumen **muchos recursos** (consultas complejas de base de datos, llamadas a API externas, procesamiento de IA).

**Encuentra este código:**

```python
@app.route('/api/search', methods=['GET'])
@jwt_required()
@limiter.limit(_____)  # TODO: Límite estricto para operaciones costosas
def search():
    # ... operación de búsqueda costosa
```

**Tu tarea:**
Completa con: `"5 per minute"`

**¿Por qué límites más estrictos?**
- La búsqueda a menudo involucra escaneos de base de datos o llamadas a API externas
- Previene el agotamiento de recursos
- Fomenta el almacenamiento en caché eficiente del lado del cliente

**Ejemplos reales:**
- **Algolia Search**: 10,000 solicitudes/mes (nivel gratuito)
- **Elasticsearch**: A menudo limitado a 5-10 búsquedas concurrentes
- **OpenAI GPT-4**: 3 solicitudes/minuto (nivel gratuito)

### Tarea 2.5: Endpoints Exentos

Algunos endpoints **nunca** deberían tener límite de tasa.

**Encuentra este código:**

```python
@app.route('/api/unlimited', methods=['GET'])
@jwt_required()
_____  # TODO: Exentar de limitación de tasa
def unlimited():
    # ... operación crítica
```

**Tu tarea:**
Agrega: `@limiter.exempt`

**Cuándo exentar endpoints:**
- Comprobaciones de salud (los sistemas de monitoreo necesitan acceso confiable)
- Operaciones de emergencia/seguridad críticas (ej., "eliminar mi cuenta")
- Comunicación interna entre microservicios (usa autenticación en su lugar)
- Webhooks de fuentes confiables

**Advertencia:** Usa las exenciones con moderación - ¡incluso los endpoints "ilimitados" pueden ser abusados!

## Parte 3: Probando Límites de Tasa (30 minutos)

### Tarea 3.1: Ejecutar la Aplicación

```bash
cd exercises/12-rate-limiting
python app.py
```

Deberías ver:
```
Exercise 12: Rate Limiting and API Security
============================================================
Endpoints:
  POST   /register          - Register new user (5 per hour)
  POST   /login             - Login (10 per minute)
  GET    /api/data          - Get data (20 per minute)
  GET    /api/search?q=...  - Search (5 per minute)
  GET    /api/unlimited     - No rate limit
  ...
```

### Tarea 3.2: Probar Límite de Tasa de Registro

**Paso 1: Registrar un usuario (debería tener éxito):**
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

**Respuesta esperada:**
```json
{
  "message": "User alice registered successfully"
}
```

**Paso 2: Intentar registrar 5 usuarios más rápidamente:**
```bash
# Windows PowerShell:
for ($i=1; $i -le 5; $i++) {
  curl -X POST http://127.0.0.1:5000/register `
    -H "Content-Type: application/json" `
    -d "{`"username`":`"user$i`",`"password`":`"pass123`"}"
}

# Mac/Linux:
for i in {1..5}; do
  curl -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"user$i\",\"password\":\"pass123\"}"
  echo ""
done
```

**Esperado:** Después de 5 registros en la misma hora, obtendrás:
```json
{
  "error": "Rate limit exceeded",
  "message": "5 per 1 hour",
  "retry_after": "Check the Retry-After header"
}
```

**Estado HTTP:** `429 Too Many Requests`

### Tarea 3.3: Inspeccionar Cabeceras de Límite de Tasa

Cada respuesta incluye información de límite de tasa en las cabeceras.

**Hacer una solicitud:**
```bash
curl -i http://127.0.0.1:5000/health
```

**Busca estas cabeceras:**
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 199
X-RateLimit-Reset: 1704672000
```

**Significado de las cabeceras:**
- `X-RateLimit-Limit`: Total de solicitudes permitidas en la ventana
- `X-RateLimit-Remaining`: Solicitudes restantes antes de alcanzar el límite
- `X-RateLimit-Reset`: Timestamp Unix cuando se reinicia el límite
- `Retry-After`: Segundos a esperar antes de reintentar (solo en respuestas 429)

**Los clientes deberían usar estas cabeceras para:**
1. Mostrar la cuota restante a los usuarios
2. Reintentar automáticamente después del período de enfriamiento
3. Implementar retroceso exponencial

### Tarea 3.4: Probar Límite de Tasa de Login

**Paso 1: Login exitoso:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

Guarda el `access_token` de la respuesta.

**Paso 2: Simular ataque de fuerza bruta (11 intentos rápidos de login):**
```bash
# Windows PowerShell:
for ($i=1; $i -le 11; $i++) {
  Write-Host "Intento $i"
  curl -X POST http://127.0.0.1:5000/login `
    -H "Content-Type: application/json" `
    -d '{"username":"alice","password":"wrongpassword"}'
}

# Mac/Linux:
for i in {1..11}; do
  echo "Intento $i"
  curl -X POST http://127.0.0.1:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"wrongpassword"}'
  echo ""
done
```

**Esperado:** Los intentos 1-10 devuelven 401 (No autorizado), el intento 11 devuelve 429 (Límite de tasa excedido).

**Beneficio de seguridad:** Un atacante solo puede probar 10 contraseñas por minuto, haciendo impracticable la fuerza bruta.

### Tarea 3.5: Probar Endpoints Autenticados

**Paso 1: Login y obtener un token válido:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

Copia el `access_token`.

**Paso 2: Probar el endpoint `/api/data` (límite: 20 por minuto):**
```bash
# Reemplaza YOUR_TOKEN_HERE con tu token real
TOKEN="YOUR_TOKEN_HERE"

# Windows PowerShell:
for ($i=1; $i -le 21; $i++) {
  Write-Host "Solicitud $i"
  curl http://127.0.0.1:5000/api/data `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
TOKEN="YOUR_TOKEN_HERE"
for i in {1..21}; do
  echo "Solicitud $i"
  curl http://127.0.0.1:5000/api/data \
    -H "Authorization: Bearer $TOKEN"
  echo ""
done
```

**Esperado:** Las solicitudes 1-20 tienen éxito, la solicitud 21 devuelve 429.

### Tarea 3.6: Probar Endpoint de Búsqueda Costosa

**Probar el límite estricto en búsqueda (5 por minuto):**
```bash
TOKEN="YOUR_TOKEN_HERE"

# Windows PowerShell:
for ($i=1; $i -le 6; $i++) {
  Write-Host "Búsqueda $i"
  curl "http://127.0.0.1:5000/api/search?q=test" `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
for i in {1..6}; do
  echo "Búsqueda $i"
  curl "http://127.0.0.1:5000/api/search?q=test" \
    -H "Authorization: Bearer $TOKEN"
  echo ""
done
```

**Esperado:** Las búsquedas 1-5 tienen éxito, la búsqueda 6 devuelve 429.

**Nota:** El límite más estricto (5 vs 20) simula la protección de una operación costosa.

### Tarea 3.7: Probar Endpoint Exento

**Probar el endpoint ilimitado:**
```bash
TOKEN="YOUR_TOKEN_HERE"

# Hacer 100 solicitudes rápidamente - todas deberían tener éxito
# Windows PowerShell:
for ($i=1; $i -le 100; $i++) {
  curl http://127.0.0.1:5000/api/unlimited `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
for i in {1..100}; do
  curl http://127.0.0.1:5000/api/unlimited \
    -H "Authorization: Bearer $TOKEN" -s | head -n 1
done
```

**Esperado:** ¡Todas las 100 solicitudes tienen éxito - sin limitación de tasa!

## Parte 4: Comprendiendo Estrategias de Límite de Tasa (20 minutos)

### Estrategia 1: Limitación de Tasa por IP (Implementación Actual)

**Cómo funciona:**
- Rastrea solicitudes por la dirección IP del cliente
- Usa `get_remote_address()` como función clave

**Pros:**
- Simple de implementar
- Funciona para solicitudes no autenticadas
- Protege contra ataques de una sola fuente

**Contras:**
- Los usuarios detrás del mismo NAT/proxy comparten el mismo límite
- No distingue entre usuarios autenticados de la misma IP
- Puede bloquear usuarios legítimos en redes compartidas (oficinas, universidades)

**Casos de uso:**
- Endpoints públicos (registro, login)
- APIs anónimas
- Aplicaciones simples

### Estrategia 2: Limitación de Tasa por Usuario

**Cómo funciona:**
- Rastrea solicitudes por ID de usuario autenticado (de JWT)
- Recurre a IP para solicitudes no autenticadas

**Ejemplo de implementación:**
```python
from flask_jwt_extended import get_jwt_identity

def get_user_key():
    """Usar identidad JWT si está disponible, de lo contrario dirección IP"""
    try:
        identity = get_jwt_identity()
        return identity if identity else get_remote_address()
    except:
        return get_remote_address()

limiter = Limiter(
    app=app,
    key_func=get_user_key,  # Rastreo por usuario
    default_limits=["1000 per day", "100 per hour"]
)
```

**Pros:**
- Límites justos por usuario (no por IP)
- Los usuarios en redes compartidas no se afectan entre sí
- Puede ofrecer límites diferentes para diferentes niveles de usuario (gratis vs premium)

**Contras:**
- Requiere autenticación
- No protege endpoints no autenticados
- Los usuarios pueden crear múltiples cuentas para eludir los límites

**Casos de uso:**
- APIs SaaS con cuentas de usuario
- Servicios premium/escalonados
- Sistemas de cuota por usuario

### Estrategia 3: Limitación de Tasa Escalonada (Avanzado)

**Cómo funciona:**
- Límites diferentes basados en el rol del usuario, nivel de suscripción o clave de API

**Ejemplo de implementación:**
```python
from flask import g

def get_rate_limit():
    """Devolver límites diferentes según el rol del usuario"""
    try:
        # Obtener rol del usuario de las reclamaciones JWT
        claims = get_jwt()
        role = claims.get('role', 'free')

        if role == 'admin':
            return "1000 per hour"
        elif role == 'premium':
            return "500 per hour"
        else:  # nivel gratuito
            return "50 per hour"
    except:
        return "10 per hour"  # Usuarios no autenticados

# Límite dinámico basado en usuario
@app.route('/api/data')
@limiter.limit(get_rate_limit)
def get_data():
    # ...
```

**Casos de uso:**
- Plataformas SaaS multinivel
- Modelos freemium
- APIs empresariales

## Parte 5: Mejores Prácticas (15 minutos)

### Mejor Práctica 1: Usar Límites Diferentes para Endpoints Diferentes

```python
# Límite generoso para leer datos
@app.route('/api/data', methods=['GET'])
@limiter.limit("100 per minute")

# Límite estricto para crear datos
@app.route('/api/data', methods=['POST'])
@limiter.limit("10 per minute")

# Muy estricto para operaciones costosas
@app.route('/api/export', methods=['GET'])
@limiter.limit("1 per hour")
```

**¿Por qué?** Las operaciones de lectura suelen ser más baratas que las escrituras, y algunas operaciones (exportaciones, informes) son muy costosas.

### Mejor Práctica 2: Incluir Siempre Cabeceras de Límite de Tasa

¡Los clientes necesitan conocer su cuota! Flask-Limiter incluye automáticamente:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

**Mejor práctica para clientes:**
```python
# Pseudocódigo para cliente de API
response = make_request()

if response.status == 429:
    retry_after = response.headers['Retry-After']
    sleep(retry_after)
    retry_request()

remaining = response.headers['X-RateLimit-Remaining']
if remaining < 10:
    warn_user("Acercándose al límite de tasa")
```

### Mejor Práctica 3: Mensajes de Error Amigables

No solo devuelvas "429 Too Many Requests" - ¡explica qué sucedió!

**Buen manejador de errores (ya en `app.py`):**
```python
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description),  # ej., "5 per 1 hour"
        'retry_after': 'Check the Retry-After header'
    }), 429
```

**Ejemplo de respuesta:**
```json
{
  "error": "Rate limit exceeded",
  "message": "5 per 1 hour",
  "retry_after": "Check the Retry-After header"
}
```

### Mejor Práctica 4: Exentar Endpoints Críticos

```python
@app.route('/health')
@limiter.exempt  # Los sistemas de monitoreo necesitan acceso confiable
def health():
    return {'status': 'ok'}

@app.route('/api/emergency-stop')
@limiter.exempt  # Operación de seguridad crítica
@jwt_required()
def emergency_stop():
    # Detener operación peligrosa
    pass
```

**Cuándo exentar endpoints:**
- Comprobaciones de salud (monitoreo)
- Operaciones de emergencia/seguridad
- Comunicación interna entre microservicios (usa autenticación en su lugar)
- Webhooks de fuentes confiables

### Mejor Práctica 5: Usar Redis en Producción

Para este ejercicio, usamos almacenamiento en memoria:
```python
limiter = Limiter(
    app=app,
    storage_uri="memory://"  # Simple, pero no escala
)
```

**En producción, usa Redis:**
```python
limiter = Limiter(
    app=app,
    storage_uri="redis://localhost:6379"  # Compartido entre múltiples servidores
)
```

**¿Por qué Redis?**
- Contadores de límite de tasa compartidos entre múltiples servidores de API
- Persistente a través de reinicios de la aplicación
- Rápido y confiable
- Estándar de la industria

### Mejor Práctica 6: Registrar Violaciones de Límite de Tasa

Agrega registro para detectar abuso:

```python
from flask import request
import logging

@app.errorhandler(429)
def ratelimit_handler(e):
    # Registrar la violación
    logging.warning(
        f"Rate limit exceeded: IP={request.remote_addr}, "
        f"Path={request.path}, Limit={e.description}"
    )

    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429
```

**Usa registros para:**
- Identificar IPs abusivas
- Detectar tráfico de bots
- Optimizar límites de tasa según patrones de uso reales

## Lista de Verificación de Pruebas

**Configuración Básica:**
- [ ] Flask-Limiter instalado (`pip install -r requirements.txt`)
- [ ] La aplicación se ejecuta sin errores (`python app.py`)
- [ ] Endpoint de comprobación de salud accesible (`/health`)

**Implementación de Límite de Tasa:**
- [ ] Limiter inicializado con `get_remote_address` y límites predeterminados
- [ ] Endpoint de registro limitado a "5 per hour"
- [ ] Endpoint de login limitado a "10 per minute"
- [ ] Endpoint de datos limitado a "20 per minute"
- [ ] Endpoint de búsqueda limitado a "5 per minute"
- [ ] Endpoint ilimitado marcado con `@limiter.exempt`

**Pruebas:**
- [ ] Límite de registro aplicado (el sexto intento en una hora falla)
- [ ] Límite de login aplicado (el undécimo intento en un minuto falla)
- [ ] Límite de endpoint de datos aplicado (la solicitud 21 falla)
- [ ] Límite de búsqueda aplicado (la sexta búsqueda falla)
- [ ] Endpoint ilimitado sin límite (100+ solicitudes tienen éxito)
- [ ] Cabeceras de límite de tasa presentes en las respuestas
- [ ] Código de estado 429 devuelto cuando se excede el límite
- [ ] Manejador de error personalizado devuelve respuesta JSON

**Comprensión:**
- [ ] Puede explicar cuándo usar limitación de tasa
- [ ] Entiende diferentes estrategias de límite de tasa (por IP vs por usuario)
- [ ] Sabe cuándo exentar endpoints
- [ ] Puede elegir límites apropiados para diferentes operaciones

## Problemas Comunes y Soluciones

### Problema 1: El Límite de Tasa No Funciona

**Síntoma:** Puedes hacer solicitudes ilimitadas sin obtener errores 429.

**Causas posibles:**
1. **El orden del decorador importa:**
   ```python
   # INCORRECTO - el limiter se ejecuta antes que JWT, por lo que las solicitudes no autenticadas pasan
   @jwt_required()
   @limiter.limit("5 per minute")
   def endpoint():
       pass

   # CORRECTO - el limiter se ejecuta primero
   @limiter.limit("5 per minute")
   @jwt_required()
   def endpoint():
       pass
   ```

2. **Endpoint marcado como exento:**
   Verifica si `@limiter.exempt` está aplicado (intencionalmente o por error).

3. **Límites demasiado generosos:**
   "1000 per minute" no se activará durante las pruebas manuales - usa límites pequeños para probar.

### Problema 2: El Límite de Tasa se Reinicia Demasiado Rápido

**Síntoma:** Después de alcanzar el límite, se reinicia inmediatamente en lugar de esperar la ventana completa.

**Causa:** Reiniciar la aplicación Flask borra los contadores de límite de tasa en memoria.

**Solución:** Este es el comportamiento esperado con almacenamiento `memory://`. En producción, usa Redis para contadores persistentes.

### Problema 3: Múltiples Usuarios de la Misma IP Comparten el Límite

**Síntoma:** Dos usuarios en la misma red (oficina, universidad) comparten el mismo límite de tasa.

**Causa:** Usar `get_remote_address()` (basado en IP) en lugar de rastreo por usuario.

**Solución:** Implementar limitación de tasa por usuario (ver Parte 4, Estrategia 2).

### Problema 4: Las Cabeceras de Límite de Tasa No Se Muestran

**Síntoma:** No hay cabeceras `X-RateLimit-*` en las respuestas.

**Causa:** Flask-Limiter agrega cabeceras automáticamente, pero pueden no mostrarse en todos los clientes.

**Solución:** Usa `curl -i` o verifica la pestaña Network de DevTools del navegador para ver las cabeceras.

### Problema 5: "429 Too Many Requests" para Comprobaciones de Salud

**Síntoma:** El sistema de monitoreo obtiene errores 429 al verificar `/health`.

**Solución:** Exentar el endpoint de comprobación de salud:
```python
@app.route('/health')
@limiter.exempt
def health():
    return {'status': 'ok'}
```

## Ejemplos de Limitación de Tasa del Mundo Real

### Ejemplo 1: API de GitHub

**Nivel gratuito (no autenticado):**
- 60 solicitudes por hora

**Autenticado:**
- 5,000 solicitudes por hora

**API de búsqueda (límite especial):**
- 10 solicitudes por minuto (más estricto porque la búsqueda es costosa)

**Cómo comunican los límites:**
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1704672000
X-RateLimit-Resource: core
```

### Ejemplo 2: API de Twitter v2

**Nivel gratuito:**
- 500,000 Tweets leídos por mes
- 1,667 Tweets por hora

**Nivel básico ($100/mes):**
- 10,000,000 Tweets por mes

**Cómo lo aplican:**
- Devuelve 429 con cabecera `x-rate-limit-reset`
- Los clientes deben esperar hasta el tiempo de reinicio antes de reintentar

### Ejemplo 3: API de Stripe

**Límites:**
- 100 solicitudes de lectura por segundo
- 100 solicitudes de escritura por segundo (más estricto en la práctica)

**Manejo especial:**
- Los endpoints de pago tienen límites más estrictos
- El modo de prueba tiene límites separados del modo en vivo

**Cómo manejan los excesos:**
- Código de estado 429
- Retroceso exponencial recomendado
- Los SDKs reintentan automáticamente con retroceso

## Más Allá de Este Ejercicio

### Próximos Pasos

1. **Ejercicio 13+**: Aplica limitación de tasa a tu API de proyecto final
2. **Despliegue en producción**: Configura Redis para almacenamiento de límite de tasa
3. **Monitoreo**: Configura alertas para violaciones de límite de tasa
4. **Análisis**: Rastrea patrones de uso de API para optimizar límites

### Temas Avanzados (Más Allá de Este Curso)

1. **Limitación de Tasa Distribuida**:
   - Redis Cluster para alta disponibilidad
   - Hashing consistente para fragmentación

2. **Limitación de Tasa Adaptativa**:
   - Aumentar límites para usuarios confiables
   - Disminuir límites para IPs sospechosas
   - Detección de anomalías basada en aprendizaje automático

3. **Algoritmo de Token Bucket**:
   - Más sofisticado que ventanas fijas
   - Permite tráfico en ráfagas
   - Se rellena a una tasa constante

4. **Limitación de Tasa Geográfica**:
   - Límites diferentes por región
   - Límites más estrictos para países de alto riesgo
   - Bloqueo basado en GeoIP

5. **Limitación de Tasa Basada en Costos**:
   - Asignar "costo" a cada endpoint
   - Rastrear costo total en lugar de conteo de solicitudes
   - Ejemplo: 1 búsqueda = 5 puntos, 1 lectura = 1 punto

## Recursos Adicionales

### Documentación Oficial
- **[Documentación de Flask-Limiter](https://flask-limiter.readthedocs.io/)** - Referencia completa de la biblioteca
- **[RFC 6585](https://tools.ietf.org/html/rfc6585)** - Especificación del código de estado HTTP 429
- **[Redis](https://redis.io/)** - Almacén de datos en memoria para producción

### Tutoriales
- [Mejores Prácticas de Limitación de Tasa](https://nordicapis.com/everything-you-need-to-know-about-api-rate-limiting/)
- [Limitación de Tasa de API de GitHub](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

### Bibliotecas Alternativas
- **[django-ratelimit](https://django-ratelimit.readthedocs.io/)** - Para aplicaciones Django
- **[express-rate-limit](https://github.com/nfriedly/express-rate-limit)** - Para Node.js/Express

## Entregables

Cuando completes este ejercicio, deberías tener:

1. **`app.py` Completado**:
   - Todos los TODOs completados correctamente
   - Limiter inicializado con función clave y valores predeterminados apropiados
   - Todos los endpoints tienen límites de tasa apropiados
   - Endpoint exento configurado

2. **Evidencia de Pruebas**:
   - Capturas de pantalla o registros mostrando la aplicación del límite de tasa
   - Respuestas 429 cuando se exceden los límites
   - Cabeceras de límite de tasa en respuestas exitosas

3. **Comprensión**:
   - Explicar por qué endpoints diferentes tienen límites diferentes
   - Describir cuándo usar limitación de tasa por IP vs por usuario
   - Identificar límites apropiados para tus propios proyectos de API

## Preguntas para Considerar

1. ¿Por qué el endpoint de login está limitado más estrictamente que el endpoint de datos?
2. ¿Qué pasaría si usaras limitación de tasa por usuario para el endpoint `/register`?
3. ¿Cómo implementarías límites de tasa diferentes para usuarios gratuitos vs premium?
4. ¿Cuándo exentarías un endpoint de la limitación de tasa? ¿Cuáles son los riesgos?
5. ¿Cómo ayudan las cabeceras de límite de tasa a los clientes de API a implementar mejor lógica de reintento?
6. ¿Cuál es la diferencia entre limitación de tasa y estrangulamiento?

¡Buena suerte protegiendo tus APIs! 🛡️
