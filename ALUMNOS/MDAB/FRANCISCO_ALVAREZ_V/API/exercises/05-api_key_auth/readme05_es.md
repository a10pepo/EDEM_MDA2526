# Ejercicio 5: Autenticación con Clave API

## Objetivo

Aprender a implementar **autenticación con clave API** en una API REST Flask, entendiendo cuándo y por qué usar claves API en lugar de credenciales usuario/contraseña.

## Inicio Rápido

```bash
cd exercises/05-api_key_auth
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

---

## Lo Que Aprenderás

Este ejercicio se basa en el Ejercicio 04 (Autenticación Básica) e introduce:

1. **Generación de Claves API** usando UUID
2. **Decoradores Personalizados** para validación de claves API
3. **Autenticación Basada en Cabeceras** con `x-api-key`
4. **Cuándo Usar Claves API** vs Autenticación Básica
5. **Patrón de Recuperación de Claves** (recuperar claves API perdidas)

---

## ¿Qué Son las Claves API?

Las **claves API** son identificadores únicos utilizados para autenticar peticiones API sin enviar credenciales usuario/contraseña repetidamente.

### Ejemplos del Mundo Real:

- **Google Maps API**: Requiere clave API en cada petición
- **OpenWeatherMap**: Envía clave API en query string (`?appid=TU_CLAVE`)
- **GitHub API**: Usa tokens de acceso personal (un tipo de clave API)
- **Stripe**: Usa claves secretas para procesamiento de pagos

### Clave API vs Autenticación Básica

| Característica | Auth Básica | Clave API |
|----------------|-------------|-----------|
| **Envía credenciales** | Cada petición (usuario:contraseña) | Una vez en el registro |
| **Formato del token** | Base64 codificado `user:pass` | UUID o cadena aleatoria |
| **Expira** | Nunca (a menos que cambie contraseña) | Puede revocarse/regenerarse |
| **Almacenamiento** | Cliente almacena contraseña | Cliente almacena clave API |
| **Seguridad** | Credenciales expuestas en cada petición | Credenciales solo enviadas una vez |
| **Caso de uso** | Apps simples, paneles admin | APIs públicas, acceso terceros |

---

## Estructura de la API

### Endpoints Públicos (Sin Autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/register` | Registrar nuevo usuario, recibir clave API |

### Protegidos por Autenticación Básica

| Método | Endpoint | Auth Requerida | Descripción |
|--------|----------|----------------|-------------|
| GET | `/api-key` | Auth Básica | Recuperar tu clave API (si se perdió) |

### Protegidos por Clave API

| Método | Endpoint | Auth Requerida | Descripción |
|--------|----------|----------------|-------------|
| GET | `/users` | Clave API | Listar todos los usuarios |

---

## Cómo Funciona

### Patrón 1: Registrarse y Obtener Clave API

```
Cliente                         Servidor
  |                               |
  |  POST /register               |
  |  {username, password}         |
  | ----------------------------> |
  |                               | Genera clave API UUID
  |                               | Hashea contraseña
  |                               | Almacena ambos
  |  {api_key: "abc123..."}       |
  | <---------------------------- |
  |                               |
  | Cliente guarda clave API      |
```

**Ejemplo:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"secret123"}' \
     http://127.0.0.1:5000/register
```

**Respuesta:**
```json
{
  "message": "User registered successfully",
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

**El cliente guarda esta clave API** (en archivo de config, variable de entorno, o almacenamiento seguro).

### Patrón 2: Usar Clave API para Endpoints Protegidos

```
Cliente                         Servidor
  |                               |
  |  GET /users                   |
  |  Header: x-api-key: abc123... |
  | ----------------------------> |
  |                               | Valida clave API
  |                               | Verifica si existe
  |  {users: [...]}               |
  | <---------------------------- |
```

**Ejemplo:**
```bash
curl -H "x-api-key: a1b2c3d4-e5f6-4789-a012-3456789abcde" \
     http://127.0.0.1:5000/users
```

**Respuesta:**
```json
{
  "users": ["alice", "bob"],
  "count": 2
}
```

### Patrón 3: Recuperar Clave API Perdida (Opcional)

Si un usuario pierde su clave API, puede recuperarla usando su usuario/contraseña:

```bash
curl -u alice:secret123 http://127.0.0.1:5000/api-key
```

**Respuesta:**
```json
{
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

---

## Guía de Implementación

### TODOs en app.py

Necesitas completar **5 espacios estratégicos**:

1. **Línea 4**: Importar librería `uuid`
2. **Línea 46**: Obtener clave API de las cabeceras de petición (`x-api-key`)
3. **Línea 54**: Comparar clave API extraída con claves almacenadas
4. **Línea 87**: Generar clave API única usando `uuid.uuid4()`
5. **Línea 106**: Establecer método HTTP para endpoint de recuperación de clave API
6. **Línea 129**: Aplicar decorador `@api_key_required`

### Conceptos Clave a Implementar

#### 1. Generar Claves API con UUID

**¿Qué es UUID?**
- **Universally Unique Identifier** (Identificador Único Universal)
- Número de 128 bits, típicamente mostrado como 32 dígitos hexadecimales
- Ejemplo: `550e8400-e29b-41d4-a716-446655440000`

**¿Por qué UUID para claves API?**
- Probabilidad de colisión extremadamente baja (claves duplicadas)
- Criptográficamente aleatorio
- Formato estandarizado
- No necesita búsquedas en BD para generación

**Implementación:**
```python
import uuid

# Generar una clave API única
api_key = str(uuid.uuid4())
# Resultado: "a1b2c3d4-e5f6-4789-a012-3456789abcde"
```

#### 2. Crear Decoradores Personalizados

**¿Qué es un decorador?**
Un decorador es una función que envuelve otra función para añadir comportamiento extra.

**Patrón básico de decorador:**
```python
from functools import wraps

def mi_decorador(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        # Código antes de la función
        print("Antes de llamar función")

        # Llamar a la función original
        result = f(*args, **kwargs)

        # Código después de la función
        print("Después de llamar función")

        return result
    return funcion_decorada

@mi_decorador
def hola():
    print("¡Hola!")
```

**Para validación de clave API:**
```python
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Extraer clave API de cabeceras
        api_key = request.headers.get('x-api-key')

        # 2. Validar que existe
        if not api_key:
            return jsonify({'error': 'Clave API ausente'}), 401

        # 3. Verificar si es válida
        if api_key not in claves_validas:
            return jsonify({'error': 'Clave API inválida'}), 401

        # 4. Si es válida, llamar función original
        return f(*args, **kwargs)

    return decorated
```

#### 3. Leer Cabeceras en Flask

```python
from flask import request

# Obtener una cabecera específica
api_key = request.headers.get('x-api-key')

# Verificar si existe cabecera
if 'x-api-key' in request.headers:
    print("Clave API presente")

# Obtener todas las cabeceras
todas_cabeceras = request.headers
```

**Nombres comunes de cabeceras para claves API:**
- `x-api-key` (más común)
- `Authorization: Bearer TU_CLAVE`
- `api-key`
- `X-API-KEY`

---

## Probando la API

### 1. Registrar un Nuevo Usuario

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"secret123"}' \
     http://127.0.0.1:5000/register
```

**Respuesta Esperada:**
```json
{
  "message": "User registered successfully",
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

**¡Guarda la clave API!** La necesitarás para peticiones posteriores.

### 2. Acceder a Endpoint Protegido con Clave API

```bash
curl -H "x-api-key: a1b2c3d4-e5f6-4789-a012-3456789abcde" \
     http://127.0.0.1:5000/users
```

**Respuesta Esperada:**
```json
{
  "users": ["alice"],
  "count": 1
}
```

### 3. Probar con Clave API Inválida

```bash
curl -H "x-api-key: clave-invalida-12345" \
     http://127.0.0.1:5000/users
```

**Respuesta Esperada:**
```json
{
  "error": "Invalid API key",
  "message": "API key not recognized"
}
```

### 4. Probar sin Clave API

```bash
curl http://127.0.0.1:5000/users
```

**Respuesta Esperada:**
```json
{
  "error": "API key missing",
  "message": "Include x-api-key header"
}
```

### 5. Recuperar Clave API con Autenticación Básica

```bash
curl -u alice:secret123 http://127.0.0.1:5000/api-key
```

**Respuesta Esperada:**
```json
{
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

---

## Entendiendo el Flujo del Código

### Flujo de Registro

```python
@app.route('/register', methods=['POST'])
def register():
    # 1. Obtener usuario y contraseña del cuerpo JSON
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 2. Validar entrada
    if not username or not password:
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400

    # 3. Verificar si usuario existe
    if username in users:
        return jsonify({'error': 'Usuario ya existe'}), 409

    # 4. Generar clave API única
    api_key = str(uuid.uuid4())

    # 5. Almacenar usuario con contraseña hasheada y clave API
    users[username] = {
        'password': generate_password_hash(password),
        'api_key': api_key
    }

    # 6. Devolver clave API al cliente
    return jsonify({'api_key': api_key}), 201
```

### Flujo de Validación de Clave API

```python
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Extraer clave API de cabeceras
        api_key = request.headers.get('x-api-key')

        # 2. Verificar si está presente
        if not api_key:
            return respuesta_error('Clave API ausente'), 401

        # 3. Buscar clave API en base de datos
        for username, user_data in users.items():
            if user_data.get('api_key') == api_key:
                # ¡Válida! Llamar función protegida
                return f(*args, **kwargs)

        # 4. Clave API no encontrada
        return respuesta_error('Clave API inválida'), 401

    return decorated
```

---

## Problemas Comunes y Soluciones

### Problema 1: "pip install uuid" falla

**Síntoma:**
```
ERROR: Could not find a version that satisfies the requirement uuid
```

**Solución:**
`uuid` es parte de la librería estándar de Python. **No necesitas instalarlo.**
Solo impórtalo directamente:
```python
import uuid
```

### Problema 2: Clave API No Funciona

**Síntoma:**
```json
{
  "error": "Invalid API key"
}
```

**Solución:**
- Verifica que estás usando la clave API exacta de la respuesta de registro
- Comprueba espacios extra o comillas en la cabecera
- Asegúrate de que el nombre de cabecera sea exactamente `x-api-key` (insensible a mayúsculas en HTTP)

**Consejo de depuración:**
```bash
# Almacenar clave API en variable para evitar errores tipográficos
API_KEY="a1b2c3d4-e5f6-4789-a012-3456789abcde"
curl -H "x-api-key: $API_KEY" http://127.0.0.1:5000/users
```

### Problema 3: Error de Clave API Ausente

**Síntoma:**
```json
{
  "error": "API key missing"
}
```

**Solución:**
Asegúrate de incluir el flag `-H` con curl:
```bash
# Incorrecto (sin cabecera)
curl http://127.0.0.1:5000/users

# Correcto
curl -H "x-api-key: TU_CLAVE" http://127.0.0.1:5000/users
```

### Problema 4: Decorador No Funciona

**Síntoma:**
Endpoint protegido accesible sin clave API.

**Solución:**
Asegúrate de que el decorador está aplicado:
```python
# Incorrecto
@app.route('/users', methods=['GET'])
def get_users():  # Falta @api_key_required
    ...

# Correcto
@app.route('/users', methods=['GET'])
@api_key_required  # Decorador aplicado
def get_users():
    ...
```

---

## Criterios de Aceptación

Tu implementación debería:

- ✅ Generar claves API únicas con UUID
- ✅ Almacenar claves API con datos de usuario
- ✅ Devolver clave API en el registro
- ✅ Validar claves API desde cabecera `x-api-key`
- ✅ Rechazar peticiones sin clave API (401)
- ✅ Rechazar peticiones con clave API inválida (401)
- ✅ Permitir recuperación de clave API usando Auth Básica
- ✅ Usar decorador personalizado para protección con clave API
- ✅ Permitir múltiples usuarios con claves API únicas

---

## Objetivos Adicionales

Una vez completes la implementación básica:

### 1. Añadir Regeneración de Clave API

Permitir a usuarios regenerar su clave API:

```python
@app.route('/api-key/regenerate', methods=['POST'])
@auth.login_required
def regenerate_api_key():
    current_user = auth.current_user()

    # Generar nueva clave API
    new_api_key = str(uuid.uuid4())
    users[current_user]['api_key'] = new_api_key

    return jsonify({
        'message': 'API key regenerated',
        'api_key': new_api_key
    }), 200
```

### 2. Añadir Expiración de Clave API

Rastrear cuándo se crearon las claves API y expirar las antiguas:

```python
from datetime import datetime, timedelta

# En registro
users[username] = {
    'password': hashed_password,
    'api_key': api_key,
    'key_created_at': datetime.now()
}

# En decorador
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')

        for username, user_data in users.items():
            if user_data.get('api_key') == api_key:
                # Verificar si expiró (ej: 30 días)
                created = user_data.get('key_created_at')
                if datetime.now() - created > timedelta(days=30):
                    return jsonify({'error': 'API key expired'}), 401

                return f(*args, **kwargs)

        return jsonify({'error': 'Invalid API key'}), 401

    return decorated
```

### 3. Añadir Límite de Tasa

Rastrear llamadas API por clave y limitar peticiones:

```python
from collections import defaultdict
from datetime import datetime

# Rastrear peticiones por clave API
api_calls = defaultdict(list)  # {api_key: [timestamp1, timestamp2, ...]}

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')

        # Validar que existe clave API...

        # Límite de tasa: Máx 10 peticiones por minuto
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Eliminar llamadas antiguas
        api_calls[api_key] = [
            call_time for call_time in api_calls[api_key]
            if call_time > minute_ago
        ]

        # Verificar límite
        if len(api_calls[api_key]) >= 10:
            return jsonify({'error': 'Rate limit exceeded'}), 429

        # Registrar esta llamada
        api_calls[api_key].append(now)

        return f(*args, **kwargs)

    return decorated
```

### 4. Añadir Múltiples Claves API por Usuario

Permitir a usuarios tener múltiples claves API para diferentes aplicaciones:

```python
users = {
    'alice': {
        'password': 'hashed',
        'api_keys': {
            'key1': {'name': 'App Móvil', 'created': datetime.now()},
            'key2': {'name': 'Dashboard Web', 'created': datetime.now()}
        }
    }
}
```

### 5. Añadir Ámbitos de Clave API

Implementar permisos para claves API:

```python
users = {
    'alice': {
        'password': 'hashed',
        'api_keys': {
            'key1': {'scopes': ['read', 'write']},
            'key2': {'scopes': ['read']}  # Clave solo lectura
        }
    }
}

def api_key_required(scopes=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('x-api-key')

            # Validar clave API y verificar ámbitos
            for username, user_data in users.items():
                for key, key_info in user_data['api_keys'].items():
                    if key == api_key:
                        if scopes and not set(scopes).issubset(key_info['scopes']):
                            return jsonify({'error': 'Permisos insuficientes'}), 403
                        return f(*args, **kwargs)

            return jsonify({'error': 'Clave API inválida'}), 401

        return decorated
    return decorator

# Uso
@app.route('/users', methods=['GET'])
@api_key_required(scopes=['read'])
def get_users():
    ...

@app.route('/users', methods=['POST'])
@api_key_required(scopes=['write'])
def create_user():
    ...
```

---

## Cuándo Usar Claves API vs Otros Métodos de Autenticación

### Usar Claves API Cuando:

✅ Construyes APIs públicas para desarrolladores terceros
✅ Permites acceso programático (scripts, bots)
✅ Necesitas revocar acceso sin cambiar contraseñas
✅ Quieres rastrear uso por aplicación
✅ Construyes comunicación servidor-a-servidor

### Usar Autenticación Básica Cuando:

✅ Paneles de administración simples
✅ Herramientas internas
✅ Autenticación temporal
✅ Prototipos rápidos
✅ Endpoints de recuperación de clave API

### Usar JWT (Siguiente Ejercicio) Cuando:

✅ Se necesita autenticación sin estado
✅ Arquitectura de microservicios
✅ Aplicaciones móviles/web
✅ Necesitas tokens que expiren
✅ Quieres incrustar datos de usuario en token

---

## Resumen

**Conclusiones Clave:**

1. **Claves API vs Autenticación Básica**
   - Las claves API son tokens persistentes
   - Auth Básica envía credenciales en cada petición
   - Claves API mejor para APIs públicas

2. **UUID para Generación de Claves**
   - Librería estándar, no necesita instalación
   - Criptográficamente seguro
   - Virtualmente sin riesgo de colisión

3. **Decoradores Personalizados**
   - Envuelven funciones para añadir comportamiento
   - Usa `@wraps(f)` para preservar metadatos de función
   - Aplica con `@nombre_decorador` encima de función

4. **Autenticación Basada en Cabeceras**
   - Claves API típicamente en cabeceras
   - Usa `request.headers.get('nombre-cabecera')`
   - Las cabeceras son insensibles a mayúsculas

5. **Mejores Prácticas de Seguridad**
   - Hashea contraseñas, nunca almacenes texto plano
   - Las claves API deben ser largas y aleatorias
   - Siempre usa HTTPS en producción
   - Permite regeneración de claves

**Próximos Pasos:**
- **Ejercicio 06**: Autenticación JWT (tokens sin estado)
- **Ejercicio 07**: Consumir APIs Públicas Externas
- **Ejercicio 08**: Operaciones CRUD

¡Buena suerte! 🔑
