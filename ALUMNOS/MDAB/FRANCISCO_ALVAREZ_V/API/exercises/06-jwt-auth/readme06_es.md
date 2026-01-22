# Ejercicio 6: Autenticación con JSON Web Tokens (JWT)

## Objetivo

Aprender a implementar **autenticación sin estado** (stateless) utilizando JSON Web Tokens (JWT) en una API REST con Flask. Comprender por qué JWT es el método de autenticación preferido para APIs modernas y cómo difiere de la autenticación básica.

## Inicio Rápido

```bash
cd exercises/06-jwt-auth
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

---

## ¿Qué es la Autenticación JWT?

### El Problema con Basic Auth

En el Ejercicio 04, aprendiste Autenticación Básica donde:
- El cliente envía **usuario y contraseña con CADA petición**
- Las credenciales están codificadas en Base64 (¡no encriptadas!)
- El servidor debe verificar credenciales en cada petición
- Las credenciales viajan constantemente por la red (riesgo de seguridad)

### La Solución JWT

**JWT (JSON Web Token)** proporciona **autenticación sin estado**:
1. El cliente envía usuario/contraseña **UNA SOLA VEZ** a `/login`
2. El servidor valida y devuelve un **token firmado** (JWT)
3. El cliente almacena el token y lo envía en todas las peticiones futuras
4. El servidor valida la firma del token (¡no necesita consultar la base de datos!)
5. **Ya no se envían contraseñas por la red después del login**

### Estructura de JWT

Un token JWT tiene tres partes separadas por puntos:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTY3ODg4ODg4OH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│                                      │                                      │
│                                      │                                      └─ Firma (verifica que el token no ha sido alterado)
│                                      └─ Payload (identidad del usuario, expiración, etc.)
└─ Header (algoritmo y tipo de token)
```

**Conceptos Clave:**
- **Auto-contenido**: Contiene toda la info del usuario necesaria (sin consultar BD)
- **Sin estado**: El servidor no almacena sesiones
- **Firmado**: El servidor puede verificar que no fue modificado
- **Expiración**: Los tokens expiran después de un tiempo (por defecto 15 minutos)

---

## Estructura de la API

### Endpoints Públicos (Sin Autenticación)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/register` | Registrar una nueva cuenta de usuario |
| POST | `/login` | Iniciar sesión con credenciales, obtener token JWT |

### Endpoints Protegidos (JWT Requerido)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/profile` | Obtener información del perfil del usuario actual |
| GET | `/users` | Obtener lista de todos los usuarios |
| GET | `/protected` | Ejemplo de recurso protegido |

---

## Cómo Funciona la Autenticación JWT

### Flujo Paso a Paso

```
1. Registro de Usuario
   Cliente                   Servidor
     |                         |
     |  POST /register         |
     |  {username, password}   |
     |------------------------>|
     |                         | • Validar entrada
     |                         | • Hashear contraseña
     |                         | • Almacenar usuario
     |  201 Created            |
     |<------------------------|

2. Login (Obtener Token)
   Cliente                   Servidor
     |                         |
     |  POST /login            |
     |  {username, password}   |
     |------------------------>|
     |                         | • Validar credenciales
     |                         | • Generar token JWT
     |                         | • Firmar token con secreto
     |  200 OK                 |
     |  {access_token: "..."}  |
     |<------------------------|
     | Guardar token           |

3. Acceder a Recurso Protegido
   Cliente                   Servidor
     |                         |
     | GET /profile            |
     | Authorization: Bearer   |
     | <token>                 |
     |------------------------>|
     |                         | • Verificar firma del token
     |                         | • Extraer identidad del usuario
     |                         | • Devolver recurso
     |  200 OK                 |
     |  {datos usuario}        |
     |<------------------------|
```

---

## Detalles de Implementación

### 1. Configuración de JWT

```python
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta'  # ¡Cambiar en producción!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Vida del token

jwt = JWTManager(app)
```

### 2. Registro de Usuario (Público)

```python
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Almacenar usuario con contraseña hasheada
    users[username] = {
        'password': generate_password_hash(password)
    }
    return jsonify({'message': 'Usuario registrado'}), 201
```

### 3. Endpoint de Login (Público)

**¡Aquí es donde JWT difiere de Basic Auth!**

```python
@app.route('/login', methods=['POST'])
def login():
    # Obtener credenciales del CUERPO de la petición, no del header Authorization
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validar credenciales manualmente
    if username in users and check_password_hash(users[username]['password'], password):
        # Generar token JWT con identidad del usuario
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Credenciales inválidas'}), 401
```

**Diferencias Clave con el Ejercicio 04:**
- ❌ NO usar decorador `@auth.login_required`
- ❌ NO usar header HTTP Basic Auth
- ✅ Credenciales enviadas en cuerpo JSON
- ✅ Devuelve token JWT en lugar de sesión

### 4. Endpoints Protegidos (JWT Requerido)

```python
@app.route('/profile', methods=['GET'])
@jwt_required()  # ← Valida el token JWT
def profile():
    # Extraer identidad del usuario del token
    current_user = get_jwt_identity()
    return jsonify({'username': current_user}), 200
```

**Cómo funciona `@jwt_required()`:**
1. Extrae el token del header `Authorization: Bearer <token>`
2. Verifica la firma del token usando JWT_SECRET_KEY
3. Comprueba que el token no ha expirado
4. Hace disponible la identidad del usuario vía `get_jwt_identity()`

---

## Probando la API

### 1. Registrar un Usuario

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secreto123"}'
```

**Respuesta Esperada:**
```json
{
  "message": "Usuario registrado exitosamente",
  "username": "alice"
}
```

### 2. Login y Obtener Token JWT

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secreto123"}'
```

**Respuesta Esperada:**
```json
{
  "message": "Login exitoso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

**¡Guarda el token** - lo necesitarás para las siguientes peticiones!

### 3. Acceder a Endpoint Protegido con Token

Reemplaza `<TU_TOKEN>` con el token actual del paso 2:

```bash
curl -X GET http://127.0.0.1:5000/profile \
  -H "Authorization: Bearer <TU_TOKEN>"
```

**Respuesta Esperada:**
```json
{
  "username": "alice",
  "profile": "Información del perfil de alice",
  "account_created": "2025-01-01"
}
```

### 4. Probar SIN Token (Debería Fallar)

```bash
curl -X GET http://127.0.0.1:5000/profile
```

**Respuesta Esperada:**
```json
{
  "msg": "Missing Authorization Header"
}
```

### 5. Obtener Todos los Usuarios (Protegido)

```bash
curl -X GET http://127.0.0.1:5000/users \
  -H "Authorization: Bearer <TU_TOKEN>"
```

---

## Entendiendo los Tokens JWT

### Inspeccionar tu Token

1. Copia el `access_token` de tu respuesta de `/login`
2. Ve a [https://jwt.io/](https://jwt.io/)
3. Pega tu token en el campo "Encoded"
4. Ve el payload decodificado:

```json
{
  "sub": "alice",           // Sujeto (identidad del usuario)
  "exp": 1678888888,        // Timestamp de expiración
  "iat": 1678885288,        // Timestamp de emisión
  "type": "access"          // Tipo de token
}
```

**Importante:** El token está **firmado**, no **encriptado**:
- ✅ El servidor puede verificar que no ha sido alterado
- ❌ Cualquiera puede leer el contenido (¡no pongas secretos en JWT!)
- ✅ Si alguien modifica el payload, la verificación de firma falla

---

## Comparación JWT vs Basic Auth

| Característica | Basic Auth (Ejercicio 04) | JWT (Ejercicio 06) |
|----------------|---------------------------|-------------------|
| **Credenciales enviadas** | En cada petición | Solo en login |
| **Con/Sin estado** | Sin estado (pero menos seguro) | Sin estado |
| **Almacenamiento servidor** | No hay sesiones | No hay sesiones |
| **Consulta BD** | En cada petición | Solo en login |
| **Escalabilidad** | Buena | Excelente |
| **Seguridad** | Base64 (no seguro) | Tokens firmados |
| **Expiración token** | No | Sí (automática) |
| **Compatible móvil/SPA** | No ideal | Perfecto |
| **Caso de uso** | APIs simples, testing | APIs producción |

### Cuándo Usar Cada Una

**Basic Auth:**
- Herramientas internas
- Prototipos rápidos
- Desarrollo/testing
- APIs simples servidor-a-servidor

**JWT:**
- Aplicaciones web en producción
- Aplicaciones móviles
- Single Page Applications (React, Vue, Angular)
- Arquitectura de microservicios
- APIs accedidas por múltiples clientes

---

## Mejores Prácticas de Seguridad

### ✅ HACER

1. **Usar HTTPS en producción** - Los tokens pueden ser interceptados en HTTP
2. **Establecer tiempos cortos de expiración** - Por defecto 15 minutos es bueno
3. **Almacenar tokens de forma segura**:
   - Web: Cookies `httpOnly` (previene XSS)
   - Móvil: Almacenamiento seguro (Keychain, KeyStore)
   - NO en localStorage (vulnerable a XSS)
4. **Usar claves secretas fuertes** - Aleatorias, largas, variable de entorno
5. **Implementar refresh tokens** - Para sesiones largas sin re-login
6. **Validar todas las entradas** - Verificar formato de usuario/contraseña

### ❌ NO HACER

1. **No poner datos sensibles en JWT** - Cualquiera puede decodificarlo
2. **No usar secretos débiles** - Hace los tokens fáciles de falsificar
3. **No omitir HTTPS** - Los tokens pueden ser robados
4. **No hacer tokens válidos para siempre** - Riesgo de seguridad
5. **No almacenar contraseñas en texto plano** - Siempre hashear

---

## Errores Comunes y Soluciones

### 1. Falta el Header de Autorización

```json
{"msg": "Missing Authorization Header"}
```

**Solución:** Añadir header a la petición:
```bash
-H "Authorization: Bearer <token>"
```

### 2. Token Inválido

```json
{"msg": "Signature verification failed"}
```

**Causas:**
- El token fue modificado
- JWT_SECRET_KEY incorrecta
- Token generado por servidor diferente

### 3. Token Expirado

```json
{"msg": "Token has expired"}
```

**Solución:** Hacer login nuevamente para obtener un token nuevo

### 4. Token Mal Formado

```json
{"msg": "Not enough segments"}
```

**Causa:** Formato del token incorrecto
**Solución:** Asegurar formato `Bearer <token>`, no solo `<token>`

---

## Criterios de Aceptación

Tu implementación debe:

- ✅ Permitir registro de usuario vía POST `/register`
- ✅ Aceptar credenciales de login en cuerpo JSON (no en header Authorization)
- ✅ Devolver un token JWT válido en login exitoso
- ✅ Proteger rutas con decorador `@jwt_required()`
- ✅ Extraer identidad del usuario con `get_jwt_identity()`
- ✅ Devolver 401 para credenciales inválidas
- ✅ Devolver 401 para tokens JWT faltantes/inválidos
- ✅ Hashear contraseñas antes de almacenar
- ✅ Usar formato de respuesta de error consistente

---

## Objetivos Adicionales

Una vez completes la implementación básica:

1. **Añadir Configuración de Expiración de Token**
   ```python
   app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
   ```

2. **Implementar Refresh Tokens** (Avanzado)
   ```python
   from flask_jwt_extended import create_refresh_token, jwt_required, get_jwt_identity

   @app.route('/refresh', methods=['POST'])
   @jwt_required(refresh=True)
   def refresh():
       current_user = get_jwt_identity()
       new_token = create_access_token(identity=current_user)
       return jsonify({'access_token': new_token}), 200
   ```

3. **Añadir Logout de Usuario** (Lista Negra de Tokens)
   - Mantener una lista negra de tokens revocados
   - Verificar lista negra en callback de `@jwt_required()`

4. **Añadir Actualización de Perfil de Usuario**
   ```python
   @app.route('/profile', methods=['PUT'])
   @jwt_required()
   def update_profile():
       # Actualizar datos del usuario
   ```

5. **Añadir Endpoint de Cambio de Contraseña**
   - Requerir contraseña actual para verificación
   - Hashear nueva contraseña antes de almacenar

---

## Próximos Pasos

**Ejercicio 07:** Aprende a consumir APIs externas (clima, GitHub, etc.)

**Ejercicio 10:** Añade **Autorización** (roles y permisos) a tus tokens JWT
- Ejercicio actual: **Autenticación** (quién eres)
- Ejercicio 10: **Autorización** (qué puedes hacer)
- JWT incluirá claims de roles (admin, usuario, etc.)

---

## Recursos Adicionales

- [Documentación Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decodificar e inspeccionar tokens
- [RFC 7519 - Especificación JWT](https://tools.ietf.org/html/rfc7519)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

## Resumen

**Puntos Clave:**

1. **JWT = Autenticación Sin Estado**
   - Enviar credenciales una vez, obtener token
   - Usar token para todas las peticiones subsiguientes
   - No se necesitan sesiones del lado del servidor

2. **Estructura JWT**
   - Header + Payload + Firma
   - Firmado (verificable) pero no encriptado (legible)
   - Contiene identidad del usuario y expiración

3. **Flujo de Buenas Prácticas**
   - POST /login con cuerpo JSON → obtener JWT
   - Almacenar JWT de forma segura
   - Enviar JWT en header Authorization: `Bearer <token>`
   - Todas las rutas protegidas usan `@jwt_required()`

4. **Seguridad**
   - Usar HTTPS en producción
   - Expiración corta de tokens
   - Claves secretas fuertes
   - Nunca poner datos sensibles en payload JWT

5. **Autenticación ≠ Autorización**
   - Este ejercicio: ¿Quién eres? (Autenticación)
   - Ejercicio 10: ¿Qué puedes hacer? (Autorización con roles)

¡Buena suerte! 🚀
