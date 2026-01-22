# Ejercicio 4: Autenticación Básica

## Objetivo
Implementar autenticación básica (Basic Auth) en una API REST utilizando Python y Flask.

## Descripción
En este ejercicio, desarrollarás una API REST sencilla que maneja recursos de "usuarios". Implementarás la autenticación básica para proteger ciertas rutas, asegurando que solo usuarios autenticados puedan acceder a ellas.

## Inicio Rápido

```bash
cd exercises/04-basic_authentication
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-HTTPAuth Werkzeug
python app.py
```

## Requisitos
1. **Configuración del Proyecto:**
   - Inicializa un entorno virtual.
   - Instala las dependencias necesarias (`Flask`, `Flask-HTTPAuth`, `Werkzeug`).

2. **Estructura de la API:**
   - Crea una ruta para registrar nuevos usuarios (`POST /usuarios`).
   - Crea una ruta para obtener la lista de usuarios (`GET /usuarios`), protegida con autenticación básica.

3. **Implementación de Autenticación Básica:**
   - Utiliza `Flask-HTTPAuth` para manejar la autenticación.
   - Almacena las contraseñas de forma segura utilizando `Werkzeug` para hashear las contraseñas.
   - Protege las rutas que requieren autenticación, verificando las credenciales proporcionadas.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar las rutas protegidas con y sin credenciales válidas.

## Instrucciones:

En el espacio _____, utiliza la función adecuada de Werkzeug para hashear la contraseña proporcionada por el usuario.
También, observa los espacios dentro del código para hacer el set-up de los métodos HTTP adecuados para cada función .
Una vez esté corregido, ejecuta el script y realiza las pruebas desde Postman.

## Pasos Sugeridos

1. **Inicializa el Proyecto:**
   ```bash
   mkdir api-autenticacion-basica
   cd api-autenticacion-basica
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   pip install Flask Flask-HTTPAuth Werkzeug
