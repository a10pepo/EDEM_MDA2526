# Guía de Introducción a Flask

## Índice
1. [¿Qué es Flask?](#qué-es-flask)
2. [Preparación del Entorno](#preparación-del-entorno)
3. [Tu Primera Aplicación Flask](#tu-primera-aplicación-flask)
4. [Conceptos Básicos](#conceptos-básicos)
5. [Trabajar con JSON](#trabajar-con-json)
6. [Recursos Adicionales](#recursos-adicionales)

## ¿Qué es Flask?
Flask es un framework web minimalista escrito en Python que permite crear aplicaciones web de manera rápida y con un mínimo número de líneas de código. Es especialmente popular por su simplicidad y flexibilidad.

### Características Principales:
- Servidor de desarrollo integrado
- Depurador integrado
- Soporte para pruebas unitarias
- Motor de plantillas Jinja2
- Compatible con WSGI 1.0
- Documentación extensiva
- Gran comunidad y muchas extensiones disponibles

## Preparación del Entorno

### Paso 1: Instalación de Python
1. Descarga Python desde [python.org](https://python.org)
2. Asegúrate de marcar la opción "Add Python to PATH" durante la instalación
3. Verifica la instalación abriendo una terminal y escribiendo:
   ```bash
   python --version
   ```

### Paso 2: Crear un Entorno Virtual
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv

# Activar el entorno virtual
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Paso 3: Instalar Flask
```bash
pip install flask
```

## Tu Primera Aplicación Flask

### Paso 1: Crear el archivo app.py
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola, estudiantes!'

if __name__ == '__main__':
    app.run(debug=True)
```

### Paso 2: Ejecutar la aplicación
```bash
python app.py
```
Visita http://localhost:5000 en tu navegador

## Conceptos Básicos

### 1. Rutas (Routes)
```python
@app.route('/about')
def about():
    return '¡Bienvenidos a mi primera aplicación Flask!'

@app.route('/user/<username>')
def show_user(username):
    return f'¡Hola, {username}!'
```

### 2. Métodos HTTP
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Procesando login...'
    return 'Por favor, inicia sesión'
```

### 3. Parámetros Dinámicos en URLs
```python
@app.route('/user/<username>')
def show_user(username):
    return f'Perfil de usuario: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Mostrando publicación {post_id}'
```

## Trabajar con JSON

Ya que construirás APIs en este curso, es importante aprender cómo Flask maneja datos JSON. JSON es el formato estándar para enviar y recibir datos en APIs web.

### 1. Devolver Respuestas JSON

Usa `jsonify()` para devolver datos JSON desde tus endpoints:

```python
from flask import jsonify

@app.route('/api/hello')
def hello_api():
    return jsonify({'message': '¡Hola, Mundo!'})

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': 'Juan Pérez', 'email': 'juan@ejemplo.com'}
    return jsonify(user)

@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': 'Alicia'},
        {'id': 2, 'name': 'Roberto'}
    ]
    return jsonify(users)
```

### 2. Leer JSON de las Peticiones

Cuando un cliente envía datos JSON a tu API, usa `request.get_json()` para leerlos:

```python
from flask import request, jsonify

@app.route('/api/greet', methods=['POST'])
def greet():
    # Obtener datos JSON del cuerpo de la petición
    data = request.get_json()

    # Acceder a campos del JSON
    name = data.get('name', 'Invitado')

    # Devolver una respuesta JSON
    return jsonify({'greeting': f'¡Hola, {name}!'})
```

**Probar con Postman:**
- Establece el método a POST
- En la pestaña Body, selecciona "raw" y "JSON"
- Ingresa: `{"name": "Alicia"}`
- Envía la petición

### 3. Almacenamiento Simple en Memoria

Para estos ejercicios, usaremos diccionarios de Python para almacenar datos (no se necesita base de datos):

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenar usuarios en memoria
users = {}
next_id = 1

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    global next_id

    if request.method == 'POST':
        # Crear un nuevo usuario
        data = request.get_json()
        user = {
            'id': next_id,
            'name': data.get('name'),
            'email': data.get('email')
        }
        users[next_id] = user
        next_id += 1
        return jsonify(user)

    else:  # GET
        # Devolver todos los usuarios
        return jsonify(list(users.values()))

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id])
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. Parámetros de Consulta

Accede a parámetros de consulta de URL con `request.args`:

```python
from flask import request, jsonify

@app.route('/api/search')
def search():
    # Acceder a parámetro de consulta: /api/search?q=flask
    query = request.args.get('q', '')
    return jsonify({'search_query': query})
```

**Nota:** Aprenderás más sobre códigos de estado HTTP, validación y manejo de errores en los próximos ejercicios.

## Recursos Adicionales

### Documentación Oficial
- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Tutorial Oficial de Flask](https://flask.palletsprojects.com/tutorial/)

### Herramientas Útiles
- Postman (para probar APIs)
- SQLite Browser (para bases de datos)
- Git (para control de versiones)

### Mejores Prácticas
1. Siempre usa entornos virtuales
2. Mantén el código organizado en módulos
3. Implementa manejo de errores
4. Escribe pruebas para tu código
5. Documenta tu código adecuadamente

## Consejos para Estudiantes
- Practica escribiendo código regularmente
- No tengas miedo de experimentar
- Únete a comunidades de Flask/Python
- Revisa proyectos de código abierto
- Mantén un registro de tu aprendizaje

¡Feliz aprendizaje!

## Tarea del ejercicio (lo que debes entregar)

**Objetivo:** Crear tu primera aplicación Flask con rutas simples y probarla usando Postman.

### 1) Construir la Aplicación
Crea un archivo `app.py` con los siguientes endpoints:

**Endpoints requeridos:**
- `GET /` - Retornar un mensaje de bienvenida (texto o JSON)
- `GET /about` - Retornar información sobre la app
- `GET /api/hello` - Retornar un mensaje JSON: `{"message": "¡Hola, Mundo!"}`
- `GET /api/user/<username>` - Retornar JSON con el nombre de usuario
- `POST /api/greet` - Aceptar JSON con un campo "name", retornar un saludo

**Ejemplo para el endpoint POST:**
```python
# Cuerpo de petición: {"name": "Alicia"}
# Respuesta: {"greeting": "¡Hola, Alicia!"}
```

### 2) Ejecutar la Aplicación
```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
python app.py
```

Visita http://127.0.0.1:5000 en tu navegador para ver tu app en ejecución.

### 3) Probar con Postman
- Crear una colección de Postman llamada "Flask Intro" (mantenerla local, no subirla al repo)
- Añadir peticiones para los 5 endpoints
- Para cada petición, incluir:
  - Un nombre claro (ej., "Obtener Mensaje de Bienvenida")
  - Una breve descripción de lo que hace el endpoint
  - El método HTTP correcto (GET o POST)
  - Respuesta de ejemplo
- Para la petición POST, recuerda:
  - Establecer Body a "raw" y "JSON"
  - Incluir un cuerpo JSON de ejemplo: `{"name": "Tu Nombre"}`

### 4) Entregables
Enviar lo siguiente:
1. Tu archivo `app.py`
2. Captura de pantalla mostrando la app ejecutándose en tu terminal
3. Captura de pantalla de tu colección de Postman mostrando las 5 peticiones
4. Colección de Postman exportada (archivo JSON) compartida por el canal indicado

### 5) Consejos
- Usa los ejemplos de esta guía como referencia
- Prueba cada endpoint en tu navegador (para peticiones GET) antes de probar en Postman
- Asegúrate de que tu app esté ejecutándose antes de probar en Postman
- No te preocupes por el manejo de errores o validación todavía - lo aprenderás en los próximos ejercicios
