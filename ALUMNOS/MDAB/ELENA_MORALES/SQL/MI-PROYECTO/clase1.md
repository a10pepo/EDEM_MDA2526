# BASE DE DATOS
- Una base de datos es una **colección de datos**, que pueden estar representada por información acerca de cualquier tema. Un número telefónico, es un dato, un nombre, es un dato, un libro contiene datos.
- Lugar donde guardo info 

# SQL
- **Structured Query Lenguage** (SQL), es un lenguaje estandarizado que nos permite comunicarnos con las bases de datos relacionales. 
- Lenguaje que se usa para hablar con bases de datos.

SQL sirve para:
- Buscar datos → "Dime todos los clientes que se llaman Juan"
- Agregar datos → "Añade un nuevo cliente"
- Cambiar datos → "Cambia la dirección de este cliente"
- Borrar datos → "Elimina este cliente"


## ¿Qué tipos de bases de datos SQL existen?
- PostgreSQL , MariaDB, Microsoft SQL Server, MySQL...


### PostgreSQL --> Sistema de gestión de bases de datos RELACIONALES
PostgreSQL = un programa/tipo base de datos para guardar datos

SQL = el idioma para decirle qué hacer con esos datos


### Tablas
- Cada tabla de la base de datos tiene **columnas, filas y campos**
- **ID**: unicos, identifica a cada columna y fila. Por ej.: 1, 2, 3...
- *Campos* son los valores de cada columna y fila

### DATA TYPES en las tablas
- Integer
- Big Integer (te permite guardar numeros mas grandes)
- Boolean
- Numeric (es el decimal), *por ej. (10, 2) el primero es el numero de digitos y el segundo el numero de decimales*
- Timestamp (fecha dia/mes/año/hora/minutos/segundos)
- Date (fecha dia/mes/año)
- Text (no hay limite de caracter)
- Varchar (limite de caracter)
- Json (se usa con NoSQL)

### // Crea la base de datos
CREATE DATABASE myFirstDB;          --> para distinguir que es SQL se pone EN MAYUSCULAS
### // Elimina la base de datos
DROP DATABASE myFirstDB;            --> DROP es para eliminar

**¡¡¡¡¡¡¡¡¡¡¡AL FINAL DE CADA CONSULTA ;**


## ¡!

*DNS: TE TRADUCE LA IP EN UN NOMBRE*
*Por ejemplo: 142.251.140.238 es www.google.com*
*El comando es nslookup y la pagina web, en este caso, google.com*


services:
  db:
    image: postgres:17-alpine
    env_file:
      - .env
    volumes:
      - postgresDB:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    restart: unless-stopped

volumes:
      postgresDB:


- El icono del elefante es una interfaz para poder trabajar con la base de datos
- Comando para ver volumen: **docker volume ls**


- Variable de entorno: variables globales que tenemos en el sistema
- NOT NULL --> no puede estar en blanco 
- UNIQUE --> caracter unico
- DROP TABLE --> te elimina la tabla
- TRUNCATE --> elimina todos los datos de la tabla pero NO LA TABLA; la vacia
- ALTER --> modificar
- ADD --> añadir
- INSERT --> guardar datos en la base de datos
- SELECT --> permite que la base de datos sepa que desea recuperar datos
- WHERE --> solo debe afectar a las filas que cumplen los criterios especificados
*SELECT * FROM users WHERE age=19;*
- UPDATE SET --> actualizar una fila de algun usuario
- DELETE FROM --> eliminar toda la fila
- ORDER BY --> ordenar de manera ascendente o descendente 
- BETWEEN --> hacer rangos entre valores
- DISTINCT --> va en contra de toda la fila de TODAS las columnas, por ej.: buscame las edades que sean diferentes
- CONCATENATE --> puedes concatenar los valores mientras selecciona filas de la tabla
- El simbolo | es para unir
- LIKE & NOT LIKE --> que contenga/no contenga (%a%), que empiece por (a%), que termine por (%a)
Se usa con WHERE para buscar un patrón específico en una columna
- GROUP BY ---> agrupar filas


### FUNCIONES CON SELECT
SELECT COUNT(id) FROM
SELECT MAX(age) FROM
SELECT MIN(age) FROM
SELECT SUM(age) FROM
SELECT AVG(age) FROM 

