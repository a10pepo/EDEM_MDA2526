-- 1. Creación de base de datos y tabla
CREATE DATABASE university_db;

CREATE  TABLE IF NOT EXISTS students(
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name          VARCHAR(100) NOT NULL,
    last_name           VARCHAR(100) NOT NULL,
    enrollment_date     NOT NULL,          -- Fecha de inscripción
    grade               NUMERIC(4,2) NOT NULL   -- La nota del estudiante
);

-- 2. Modificación de tabla
ALTER TABLE students ADD COLUMN city VARCHAR(100);
ALTER TABLE students ALTER COLUMN grade TYPE INTEGER;

-- 3. Inserción de datos
INSERT INTO students(first_name, last_name, enrollment_date, grade, city)
VALUES
('Miguel', 'Navarro', '2025-09-18', 9, 'Valencia'),
('Ana', 'Pérez', '2019-08-15', 85, 'Madrid'),
('Carlos', 'García', '2021-02-20', 72, 'Barcelona'),
('Lucía', 'Martínez', '2023-10-01', 95, 'Sevilla'),
('Javier', 'Sánchez', '2018-05-10', 60, 'Valencia'),
('Elena', 'Ruiz', '2024-01-25', 88, 'Bilbao'),
('Ana', 'López', '2020-11-12', 79, 'Málaga'),
('David', 'Fernández', '2022-07-30', 92, 'Zaragoza'),
('Javier', 'Alonso', '2023-04-05', 55, 'Murcia'),
('Marta', 'Díaz', '2021-09-17', 100, 'Palma'),
('Pablo', 'Gómez', '2018-03-22', 68, 'Alicante');

-- 4. Consultas básicas
SELECT * FROM students;
SELECT first_name, grade FROM students WHERE grade > 80;
SELECT * FROM students WHERE enrollment_date < '2021-01-01';
SELECT * FROM students WHERE id = 4;

-- 5. Actualizar y eliminar
UPDATE students SET grade = 95 WHERE id = 3;
DELETE FROM students WHERE id = 7;
DELETE FROM students WHERE grade < 70;

-- 6. Orden y rangos
SELECT * FROM students ORDER BY enrollment_date DESC;
SELECT * FROM students WHERE grade BETWEEN 70 AND 90;

INSERT INTO students(first_name, last_name, enrollment_date, grade, city)
VALUES ('Sofía', 'Torres', '2020-03-10', 90, 'Gijón'),
('Ricardo', 'Soto', '2022-11-25', 75, 'Granada'),
('Isabel', 'Vidal', '2018-09-01', 52, 'Toledo'),
('Jorge', 'Merino', '2023-01-15', 65, 'Logroño'),
('Andrea', 'Ramos', '2024-06-30', 81, 'Vigo'),
('Sofía', 'Romero', '2019-12-05', 98, 'A Coruña'),
('Héctor', 'Gil', '2021-04-28', 50, 'Santander'),
('Jorge', 'Vega', '2020-10-20', 100, 'Burgos'),
('Nuria', 'Peña', '2023-08-08', 70, 'Pamplona'),
('Rubén', 'Castro', '2018-07-19', 83, 'Salamanca');

-- 7. DISTINCT y concatenación
SELECT DISTINCT first_name FROM students;
SELECT first_name||' '||last_name AS full_name FROM students;

-- 8. LIKE y NOT LIKE
SELECT * FROM students WHERE last_name LIKE '%e%';
SELECT * FROM students WHERE first_name LIKE '%a';
SELECT * FROM students WHERE first_name NOT LIKE '%o%';

-- 9. Funciones agregadas y GROUP BY
SELECT COUNT(id) FROM students;
SELECT ROUND(AVG(grade),2) AS avg_grade FROM students;
SELECT MAX(grade) AS max_grade, MIN(grade) AS min_grade FROM students;
SELECT grade, COUNT(id) AS frecuency FROM students GROUP BY grade ORDER BY grade DESC;

-- 10. Cálculos con columnas y ROUND()
ALTER TABLE students ADD COLUMN scholarship NUMERIC(10,2);   -- BECA
UPDATE students SET scholarship = grade * 0.10;

SELECT
    first_name,
    grade,
    grade*0.05 AS bonus,
    ROUND(grade+(grade*0.05),2) AS total_grade
FROM students;