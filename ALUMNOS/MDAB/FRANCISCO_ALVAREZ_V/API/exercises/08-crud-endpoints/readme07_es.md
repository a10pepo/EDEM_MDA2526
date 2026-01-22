# Ejercicio 8: Creación de Endpoints CRUD

## Objetivo
Implementar endpoints CRUD (Crear, Leer, Actualizar, Eliminar) en una API REST utilizando Python y Flask.

## Descripción
En este ejercicio, ampliarás la API desarrollada en los ejercicios anteriores para incluir operaciones CRUD sobre los recursos de "estudiantes". Deberás crear rutas que permitan a los usuarios crear nuevos estudiantes, obtener la lista de estudiantes, actualizar información de un estudiante específico y eliminar estudiantes. Completa los espacios en blanco en el código proporcionado para implementar estas funcionalidades.

## Inicio Rápido

```bash
cd exercises/08-crud-endpoints
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Werkzeug
python app.py
```

## Requisitos
1. **Instalación de Dependencias Adicionales:**
   - Asegúrate de tener instalada la biblioteca `Flask` y las extensiones utilizadas en ejercicios anteriores.

2. **Estructura de la API:**
   - **Crear Estudiante (`POST /estudiantes`):** Permite registrar un nuevo estudiante.
   - **Obtener Estudiantes (`GET /estudiantes`):** Retorna una lista de todos los estudiantes.
   - **Actualizar Estudiante (`PUT /estudiantes/<username>`):** Actualiza la información de un estudiante específico.
   - **Eliminar Estudiante (`DELETE /estudiantes/<username>`):** Elimina un estudiante específico.

3. **Implementación de CRUD:**
   - Utiliza los métodos HTTP adecuados para cada operación.
   - Asegura que las rutas estén protegidas utilizando la autenticación JWT implementada en ejercicios anteriores.
   - Valida las entradas y maneja errores apropiadamente.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar cada una de las operaciones CRUD.
   - Asegúrate de que las operaciones funcionen correctamente y que se manejen los errores de manera adecuada.

## Pasos Sugeridos

1. **Actualiza el Archivo `app.py`:**
   - Importa las bibliotecas necesarias.
   - Crea las rutas para las operaciones CRUD sobre "estudiantes".

2. **Desarrolla las Operaciones CRUD en `app.py`:**

   Completa el siguiente código en `ejercicios/07-crud-endpoints/app.py`, llenando los espacios en blanco indicados por `_____`:

   ```python
   from flask import Flask, jsonify, request
   from flask_httpauth import HTTPBasicAuth
   from werkzeug.security import generate_password_hash, check_password_hash
   from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
   import requests
   
   app = Flask(__name__)
   auth = HTTPBasicAuth()
   
   # Configuración de JWT
   app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_jwt'  # Cambia esto por una clave secreta segura
   jwt = JWTManager(app)
   
   # Base de datos simulada para almacenar estudiantes
   estudiantes = {
       # 'nombre_estudiante': {'password': 'hashed_password', 'api_key': 'api_key'}
   }
   
   @auth.verify_password
   def verify_password(username, password):
       if username in estudiantes and check_password_hash(estudiantes.get(username)['password'], password):
           return username
       return None
   
   @app.route('/estudiantes', methods=['____'])
   def register_student():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')
       
       if not username or not password:
           return jsonify({'message': 'Username and password are required.'}), 400
       if username in estudiantes:
           return jsonify({'message': 'User already exists.'}), 400
       
       # Hashear la contraseña antes de almacenarla
       estudiantes[username] = {
           'password': generate_password_hash(password),
           'api_key': 'api_key_placeholder'  # Implementa la generación de API Key si aplica
       }
       return jsonify({'message': 'User registered successfully.'}), 201
   
   @app.route('/login', methods=['____'])
   @auth.login_required
   def login():
       current_user = auth.current_user()
       access_token = create_access_token(identity=current_user)
       return jsonify({'access_token': access_token}), 200
   
   @app.route('/perfil', methods=['____'])
   @jwt_required()
   def perfil():
       current_user = get_jwt_identity()
       return jsonify({'perfil': f'Información del perfil de {current_user}'}), 200
   
   # Crear Estudiante
   @app.route('/estudiantes', methods=['____'])
   @jwt_required()
   def crear_estudiante():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')
       
       if not username or not password:
           return jsonify({'message': 'Username and password are required.'}), 400
       if username in estudiantes:
           return jsonify({'message': 'Student already exists.'}), 400
       
       estudiantes[username] = {
           'password': generate_password_hash(password),
           'api_key': 'api_key_placeholder'  # Implementa la generación de API Key si aplica
       }
       return jsonify({'message': 'Student created successfully.'}), 201
   
   # Obtener Estudiantes
   @app.route('/estudiantes', methods=['___'])
   @jwt_required()
   def obtener_estudiantes():
       return jsonify({'students': list(estudiantes.keys())}), 200
   
   # Actualizar Estudiante
   @app.route('/estudiantes/<username>', methods=['___'])
   @jwt_required()
   def actualizar_estudiante(username):
       if username not in estudiantes:
           return jsonify({'message': 'Student not found.'}), 404
       
       data = request.get_json()
       password = data.get('password')
       
       if password:
           estudiantes[username]['password'] = generate_password_hash(password)
           return jsonify({'message': 'Student updated successfully.'}), 200
       else:
           return jsonify({'message': 'Nothing to update.'}), 400
   
   # Eliminar Estudiante
   @app.route('/estudiantes/<username>', methods=['___'])
   @jwt_required()
   def eliminar_estudiante(username):
       if username not in estudiantes:
           return jsonify({'message': 'Student not found.'}), 404
       
       del estudiantes[username]
       return jsonify({'message': 'Student deleted successfully.'}), 200
   
   @app.errorhandler(404)
   def not_found(error):
       return jsonify({'error': 'Resource not found.'}), 404
   
   @app.errorhandler(405)
   def method_not_allowed(error):
       return jsonify({'error': 'Method not allowed.'}), 405
   
   if __name__ == '__main__':
       app.run(debug=True)
