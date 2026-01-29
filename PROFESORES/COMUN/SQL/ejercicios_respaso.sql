1. Creación de base de datos y tabla

Crea una base de datos llamada university_db.
Dentro de ella, crea una tabla llamada students con los siguientes campos:

id  
first_name 
last_name 
enrollment_date (fecha de inscripción)
grade de tipo NUMERIC(4,2) (la nota del estudiante)

2. Modificación de tabla

Añade una columna city de tipo VARCHAR(100).

Modifica grade para que sea tipo INTEGER.


3. Inserción de datos

Inserta al menos 10 estudiantes, cumpliendo:

    - Al menos 2 tengan el mismo first_name.

    - Las fechas de inscripción (enrollment_date) deben estar entre 2018 y 2024.

    - Las notas (grade) deben variar entre 50 y 100.

4. Consultas básicas 

Muestra todos los estudiantes.

Muestra solo los first_name y grade de los estudiantes con nota superior a 80.

Muestra los estudiantes inscritos antes de 2021.

Muestra el estudiante cuyo id sea 4.

5. Actualizar y eliminar

Actualiza la nota (grade) del estudiante con id 3 a 95.

Elimina el estudiante cuyo id sea 7.

Elimina todos los estudiantes con nota inferior a 70.

6. Orden y rangos

Muestra todos los estudiantes ordenados por enrollment_date de más reciente a más antiguo.

Muestra los estudiantes con grade entre 70 y 90.

7. DISTINCT y concatenación

Muestra los nombres (first_name) sin repetir.

Muestra el nombre completo concatenando first_name y last_name como alias nombre_completo.

8. LIKE y NOT LIKE

Muestra los estudiantes cuyo apellido contenga la letra “e”.

Muestra los estudiantes cuyo nombre termine en “a”.

Muestra los estudiantes cuyo nombre no contenga la letra “o”.

9. Funciones agregadas y GROUP BY

Muestra el número total de estudiantes.

Muestra la nota media (AVG) de todos los estudiantes.

Muestra la nota más alta y la más baja.

Agrupa por grade y muestra cuántos estudiantes tienen cada nota.

10. Cálculos con columnas y ROUND()

Añade una columna scholarship (NUMERIC(10,2)).(BECA)
Actualiza esta columna con un valor calculado: el 10% del grade (por ejemplo: grade * 0.10).

Haz una consulta que muestre:

first_name, grade,

una columna calculada bonus que sea grade * 0.05

una columna total_grade que sea grade + bonus, redondeada a 2 decimales.

Usa alias claros: bonus y total_grade.

---------------

SOLUCIÓN:

1. Creación de base de datos y tabla

CREATE DATABASE university_db;

CREATE TABLE students (
    student_id BIGSERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    enrollment_date DATE NOT NULL,
    grade NUMERIC(4,2)
);

2. Modificación de tabla

ALTER TABLE students ADD COLUMN city VARCHAR(100);

ALTER TABLE students ALTER COLUMN grade TYPE INTEGER;

ALTER TABLE students DROP COLUMN city;

3. Inserciones
INSERT INTO students (first_name, last_name, enrollment_date, grade)
VALUES
('Lucía', 'Gómez', '2020-09-12', 82),
('Carlos', 'Muñoz', '2023-01-08', 91),
('Marina', 'Lopez', '2019-07-22', 75),
('Pablo', 'Santos', '2021-03-30', 68),
('Lucía', 'Fernández', '2022-05-19', 95),
('Jorge', 'Ramírez', '2018-11-01', 55),
('Laura', 'Martínez', '2024-02-10', 88),
('Sergio', 'Ortiz', '2020-06-25', 92),
('Ana', 'Blasco', '2021-09-18', 77),
('David', 'Castro', '2023-04-02', 65);

4. Consultas básicas (SELECT / WHERE)

SELECT * FROM students;

SELECT first_name, grade FROM students WHERE grade > 80;

SELECT * FROM students WHERE enrollment_date < '2021-01-01';

SELECT * FROM students WHERE student_id = 4;

5. Actualizar y eliminar

UPDATE students SET grade = 95 WHERE student_id = 3;

DELETE FROM students WHERE student_id = 7;

DELETE FROM students WHERE grade < 60;

6. Orden y rangos

SELECT * FROM students ORDER BY enrollment_date DESC;

SELECT * FROM students WHERE grade BETWEEN 70 AND 90;

7. DISTINCT y concatenación

SELECT DISTINCT first_name FROM students;

SELECT first_name || ' ' || last_name AS nombre_completo FROM students;

8. LIKE y NOT LIKE

SELECT * FROM students WHERE last_name LIKE '%e%';

SELECT * FROM students WHERE first_name LIKE '%a';

SELECT * FROM students WHERE first_name NOT LIKE '%o%';

9. Funciones agregadas y GROUP BY
SELECT COUNT(student_id) AS total_estudiantes FROM students;

SELECT AVG(grade) AS nota_media FROM students;

SELECT MAX(grade) AS nota_maxima, MIN(grade) AS nota_minima FROM students;

SELECT grade, COUNT(*) AS cantidad
FROM students
GROUP BY grade
ORDER BY grade ASC;

10. Cálculos con columnas y ROUND()
ALTER TABLE students ADD COLUMN scholarship NUMERIC(10,2);

UPDATE students SET scholarship = grade * 0.10;

SELECT
    first_name,
    grade,
    ROUND(grade * 0.05, 2) AS bonus,
    ROUND(grade + (grade * 0.05), 2) AS total_grade
FROM students;