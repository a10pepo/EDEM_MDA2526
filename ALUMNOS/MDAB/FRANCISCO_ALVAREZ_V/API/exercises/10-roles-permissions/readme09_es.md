# Ejercicio 10: Implementación de Roles y Permisos en una API Flask

## Inicio Rápido

```bash
cd exercises/10-roles-permissions
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Flask-Principal Werkzeug
python app.py
```

## Objetivo
- **Asignación de Roles y Permisos:** Implementar un sistema de control de acceso basado en roles para la API.
- **Protección de Rutas:** Asegurar que solo los usuarios con los permisos adecuados puedan acceder a rutas específicas.
- **Autenticación y Seguridad:** Utilizar JWT (JSON Web Tokens) y Flask-Principal para gestionar usuarios, roles y permisos.

---

## Requisitos Previos

1. **Instalar Dependencias:**
   Asegúrate de tener instaladas las siguientes bibliotecas:
   - Flask
   - Flask-JWT-Extended
   - Flask-Principal
   - Werkzeug

   Puedes instalarlas con:
   ```bash
   pip install Flask Flask-JWT-Extended Flask-Principal Werkzeug
   ```

2. **Clonar el Proyecto:**
   Clona el repositorio o copia el archivo `app.py` proporcionado.

3. **Ejecutar el Script:**
   Inicia la aplicación con:
   ```bash
   python app.py
   ```

---

## Funcionalidades

### **Registro de Usuarios**
Permite registrar nuevos usuarios asignándoles un rol predeterminado o personalizado.

### **Inicio de Sesión**
Autentica a los usuarios y les proporciona un token JWT que será necesario para acceder a las rutas protegidas.

### **Roles Disponibles**
1. **Admin:**
   - Acceso a todas las rutas, incluidas aquellas que gestionan usuarios.
   - Puede realizar acciones como actualizar o eliminar otros usuarios.

2. **Student:**
   - Acceso restringido a rutas específicas diseñadas para estudiantes.

### **Protección de Rutas**
El acceso a las rutas está restringido según el rol del usuario. Esto se gestiona mediante los decoradores de Flask-Principal que verifican los permisos asignados.

---

## Estructura de la API

### **Endpoints Principales**

1. **Registro de Usuarios**
   - **Método:** `POST`
   - **Ruta:** `/register`
   - **Descripción:** Registra un nuevo usuario con un rol específico.

2. **Inicio de Sesión**
   - **Método:** `POST`
   - **Ruta:** `/login`
   - **Descripción:** Autentica a un usuario y retorna un token JWT.

3. **Perfil del Usuario**
   - **Método:** `GET`
   - **Ruta:** `/perfil`
   - **Descripción:** Devuelve información del usuario autenticado.

4. **Listar Usuarios**
   - **Método:** `GET`
   - **Ruta:** `/usuarios`
   - **Descripción:** Devuelve una lista paginada de usuarios registrados.

5. **Actualizar Usuario**
   - **Método:** `PUT`
   - **Ruta:** `/usuarios/<username>`
   - **Descripción:** Actualiza información del usuario (contraseña o rol).
   - **Requiere:** Rol de administrador.

6. **Eliminar Usuario**
   - **Método:** `DELETE`
   - **Ruta:** `/usuarios/<username>`
   - **Descripción:** Elimina a un usuario.
   - **Requiere:** Rol de administrador.

7. **Dashboard de Administrador**
   - **Método:** `GET`
   - **Ruta:** `/admin/dashboard`
   - **Descripción:** Devuelve información exclusiva para administradores.

8. **Datos del Estudiante**
   - **Método:** `GET`
   - **Ruta:** `/student/data`
   - **Descripción:** Devuelve información específica del estudiante autenticado.

---

## Pruebas

### **Pruebas Básicas**
- Registra un usuario y verifica que puede iniciar sesión.
- Intenta acceder a rutas protegidas sin un token JWT y verifica que el acceso sea denegado.
- Genera un token válido e intenta acceder a rutas específicas según el rol del usuario.

### **Pruebas de Roles**
1. Crea usuarios con roles diferentes.
2. Intenta acceder a rutas restringidas con cada rol y verifica que las restricciones se aplican correctamente.

### **Errores Comunes**
- **Token Inválido:** Asegúrate de incluir el token JWT en el encabezado `Authorization` con el formato `Bearer <token>`.
- **Acceso Denegado:** Verifica que el usuario tiene el rol correcto para acceder a la ruta.

---

## Notas Adicionales
- Usa herramientas como Postman o curl para probar las rutas de la API.
- Asegúrate de que el archivo `app.py` esté configurado correctamente antes de ejecutar las pruebas.
- Puedes ajustar los roles y permisos según las necesidades de tu aplicación.

---

¡Buena suerte implementando roles y permisos en tu API Flask! 🎉
