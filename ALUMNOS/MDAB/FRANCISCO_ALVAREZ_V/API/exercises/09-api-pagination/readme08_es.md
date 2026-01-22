# Ejercicio 9: Implementación de Paginación en Endpoints

## Inicio Rápido

```bash
cd exercises/09-api-pagination
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Werkzeug
python app.py
```

## Objetivo

- **Implementar Paginación en Endpoints:** Aprender a manejar grandes conjuntos de datos dividiéndolos en páginas más pequeñas.
- **Optimización de Respuestas:** Mejorar la eficiencia y usabilidad de la API al limitar la cantidad de datos retornados en cada solicitud.
- **Manejo de Parámetros de Consulta:** Utilizar parámetros de consulta para controlar la paginación.

## Descripción

En este ejercicio, implementarás la funcionalidad de paginación en la ruta `GET /estudiantes`. La paginación permitirá dividir la lista de estudiantes en páginas más pequeñas, controladas por parámetros de consulta como `page` y `per_page`.

## Requisitos

1. **Instalación de Dependencias Adicionales:**
   - Asegúrate de tener instalada la biblioteca `Flask` y las extensiones utilizadas en ejercicios anteriores.
   - Utiliza la biblioteca `math` (incluida por defecto en Python) para calcular el número total de páginas.

2. **Estructura de la API:**
   - **Ruta Paginada (`GET /estudiantes`):** Retorna una lista paginada de estudiantes, permitiendo especificar el número de página y la cantidad de estudiantes por página mediante parámetros de consulta.

3. **Implementación de Paginación:**
   - Utiliza parámetros de consulta como `page` y `per_page` para controlar la paginación.
   - Calcula los índices de inicio y fin para retornar el subconjunto correcto de estudiantes.
   - Retorna información adicional como el número total de páginas y el número actual de página.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar la paginación, solicitando diferentes páginas y tamaños de página.
   - Asegúrate de que la paginación funcione correctamente y que se manejen los errores de manera adecuada (por ejemplo, páginas fuera de rango).

## Pasos Detallados

1. **Configura la Ruta `/estudiantes`**:
   - Modifica la ruta que maneja `GET /estudiantes` para aceptar parámetros de consulta `page` y `per_page`.
   - Calcula los índices para obtener el subconjunto de estudiantes de acuerdo con la página solicitada.

2. **Calcula el Total de Páginas:**
   - Usa la fórmula `ceil(total / per_page)` para calcular el número total de páginas, asegurándote de manejar correctamente divisiones no enteras.

3. **Construye los Enlaces de Navegación:**
   - Utiliza `request.base_url` y `urlencode` para generar los enlaces `prev` y `next`.

4. **Retorna la Respuesta:**
   - Incluye la lista de estudiantes de la página solicitada, la información de paginación y los enlaces de navegación.

## Ejemplo de Código

```python
@app.route('/estudiantes', methods=['GET'])
@jwt_required()
def obtener_estudiantes():
    try:
        # Obtener los parámetros de consulta 'page' y 'per_page' con valores predeterminados
        page = request.args.get('page', 1, type=int)  # Página actual
        per_page = request.args.get('per_page', 10, type=int)  # Estudiantes por página

        # Validar el valor de 'per_page'
        if per_page <= 0 or per_page > 100:
            return jsonify({'message': 'per_page debe ser entre 1 y 100.'}), 400

        # Calcular el número total de estudiantes y páginas
        total_students = len(estudiantes)  # Total de estudiantes registrados
        total_pages = math.ceil(total_students / per_page)  # Número total de páginas

        # Validar el rango de la página solicitada
        if page < 1 or page > total_pages:
            return jsonify({'message': 'Página no encontrada.'}), 404

        # Determinar los índices de inicio y fin de la lista de estudiantes
        start = (page - 1) * per_page  # Índice inicial
        end = start + per_page  # Índice final
        students_list = list(estudiantes.keys())[start:end]  # Subconjunto de estudiantes

        # Construir enlaces para navegar entre páginas
        base_url = request.base_url  # URL base de la solicitud
        query_params = request.args.to_dict()  # Parámetros de consulta actuales

        def build_url(new_page):
            # Construye una URL con el número de página actualizado
            query_params['page'] = new_page
            return f"{base_url}?{urlencode(query_params)}"

        # Crear enlaces de navegación (prev y next)
        links = {}
        if page > 1:
            links['prev'] = build_url(page - 1)  # Enlace a la página anterior
        if page < total_pages:
            links['next'] = build_url(page + 1)  # Enlace a la página siguiente

        # Retornar la respuesta con datos paginados
        return jsonify({
            'students': students_list,  # Lista de estudiantes en la página actual
            'total_pages': total_pages,  # Número total de páginas
            'current_page': page,  # Página actual
            'per_page': per_page,  # Número de estudiantes por página
            'total_students': total_students,  # Total de estudiantes registrados
            'links': links  # Enlaces de navegación
        }), 200

    except Exception as e:
        # Manejo de errores generales
        return jsonify({'error': 'Ocurrió un error al procesar la solicitud.', 'details': str(e)}), 500
```

## Pruebas con Postman o `curl`

1. **Solicitar Página Específica:**

   ```bash
   curl -X GET "http://127.0.0.1:5000/estudiantes?page=2&per_page=5" -H "Authorization: Bearer <tu_token_jwt>"
   ```

2. **Resultado Esperado:**

   ```json
   {
     "students": ["student6", "student7", "student8", "student9", "student10"],
     "total_pages": 3,
     "current_page": 2,
     "per_page": 5,
     "total_students": 13,
     "links": {
       "prev": "http://127.0.0.1:5000/estudiantes?page=1&per_page=5",
       "next": "http://127.0.0.1:5000/estudiantes?page=3&per_page=5"
     }
   }
   ```

3. **Página Fuera de Rango:**

   ```bash
   curl -X GET "http://127.0.0.1:5000/estudiantes?page=100&per_page=5" -H "Authorization: Bearer <tu_token_jwt>"
   ```

   Respuesta:

   ```json
   {
     "message": "Página no encontrada."
   }
   ```

## Puntos a Considerar

- Ajusta los valores predeterminados y máximos de `per_page` según las necesidades de tu API.
- Asegúrate de manejar errores para solicitudes con parámetros malformados o fuera de rango.
- Documenta claramente los parámetros aceptados en tu API para que los clientes puedan usarlos correctamente.

¡Buena suerte con la implementación! Si tienes dudas, no dudes en consultar.

