-- CREAMOS LA BASE DE DATOS
CREATE DATABASE my_company_database;

-- CREAMOS LA TABLA
CREATE TABLE IF NOT EXISTS employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

-- AÑADIMOS COLUMNAS
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

-- INSERTAR DATOS
INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES ('2003-08-19', 'Salva', 'Gisbert', 300000, 'Científico de Datos', '2025-07-08'),
('1990-05-10', 'Carlos', 'López', 25000, 'Ingeniero Industrial', '2020-03-15'),
('1988-02-21', 'Carlos', 'Pérez', 18000, 'Analista de Datos', '2020-11-02'),
('1995-07-30', 'Carlos', 'Ruiz', 45000, 'Project Manager', '2020-08-27'),

('1992-01-12', 'Ana', 'Soler', 12000, 'Científica de Datos', '2019-04-10'),
('1993-09-22', 'Lucía', 'Torres', 5000, 'Analista Junior', '2020-05-19'),
('1985-10-02', 'Luis', 'Martínez', 32000, 'Desarrollador Backend', '2018-02-11'),
('1991-04-08', 'Elena', 'Ramírez', 27000, 'Desarrolladora Frontend', '2021-01-23'),
('1996-12-14', 'Miguel', 'Ortiz', 15000, 'Data Engineer', '2020-09-03'),
('1994-03-03', 'Laura', 'Gil', 48000, 'QA Tester', '2022-07-29'),


('1990-08-17', 'Sara', 'Sánchez', 22000, 'Administrativa', '2020-06-18'),
('1987-11-27', 'David', 'Navarro', 35000, 'SCRUM Master', '2017-10-20'),
('1999-02-14', 'Marta', 'Costa', 26000, 'UX Designer', '2023-02-14'),
('1998-06-11', 'Pablo', 'Rico', 9000, 'Becario', '2020-01-07'),
('1997-05-25', 'Julia', 'Moya', 17000, 'Marketing', '2022-06-09'),
('1992-01-01', 'Adrián', 'Gómez', 39000, 'Profesor de Tecnología', '2021-03-30');

-- Muestra el empleado cuyo id sea 2
SELECT * 
FROM employees
WHERE id = 2;

-- Selecciona todos los empleados con un salario superior a 20000
SELECT *
FROM employees
WHERE salary > 20000;

-- Selecciona todos los empleados con un salario inferior o igual a 10000
SELECT *
FROM employees
WHERE salary <= 10000;

-- Actualiza el first_name del empleado cuyo id sea 7
UPDATE employees SET first_name = 'Priscilio' WHERE id = 7;

-- Elimina el empleado cuyo id sea 5
DELETE FROM employees WHERE id = 5;

-- Elimina a todos los empleados con un salario superior a 20000
DELETE FROM employees WHERE salary < 20000;

-- Selecciona todos los empleados con un salario entre 14000 y 50000
SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

-- Ordena los empleados por birth_date de forma descendente
SELECT * 
FROM employees
ORDER BY birth_date DESC;

-- Muestra los first_name de los empleados sin repetir
SELECT DISTINCT first_name
FROM employees;

-- Muestra el nombre completo del empleado como "nombre_completo" cuyo id sea 7
SELECT first_name ||' '|| last_name AS nombre_completo
FROM employees 
WHERE id = 7;

-- Muestra los empleados cuyo nombre empiece por P
SELECT *
FROM employees 
WHERE first_name LIKE 'P%';

-- Muestra los empleados cuyo nombre contenga la a
SELECT *
FROM employees
WHERE first_name LIKE '%a%';

-- Muestra el número total de empleados
SELECT COUNT(id)
FROM employees;

-- Muestra el empleado con el salario más alto
SELECT * 
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

-- Muestra el salario medio por título
SELECT title, AVG(salary)
FROM employees
GROUP BY title;

-- Muestra el salario máximo y mínimo por título
SELECT title, MAX(salary), MIN(salary)
FROM employees
GROUP BY title;

-- Muestra el first_name y salary de cada empleado redondeando a 2 decimales
SELECT first_name, ROUND(salary, 2)
FROM employees;

--
SELECT first_name ||' '|| last_name AS nombre, salary AS salario_bruto, ROUND(salary * 0.21, 2) AS impuestos,  salary -  ROUND(salary * 0.21, 2) as salario_neto
FROM employees;

-- Crea una tabla llamada departments que contenga un campo llamado name
CREATE TABLE IF NOT EXISTS departments(
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
)

-- Inserta dos departamentos en la nueva tabla departments
INSERT INTO departments(name)
VALUES('Marketing'),
    ('Engineering');

-- Muestra todos los departamentos
SELECT * 
FROM departments;

-- Modifica tu tabla de employees y añade la FK department_id que haga referencia al id de la tabla departments.
ALTER TABLE employees ADD COLUMN department_id INT REFERENCES departments(id);

-- Actualiza tres empleados en la tabla employees:
-- Asigna dos empleados al departamento Engineering.
UPDATE employees SET department_id = 2 WHERE id = 1;
UPDATE employees SET department_id = 2 WHERE id = 2;

-- Asigna un empleado al departamento Marketing.
UPDATE employees SET department_id = 1 WHERE id = 4;

-- Muestra todos los empleados.
SELECT *
FROM employees;

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.
SELECT e.first_name, d.name
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id;

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.
SELECT e.first_name, d.name
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id;

-- CREATE TABLE comments (
--     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     post_id INTEGER NOT NULL REFERENCES posts(id),
--     user_id INTEGER NOT NULL REFERENCES users(id),
--     body TEXT NOT NULL,
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

