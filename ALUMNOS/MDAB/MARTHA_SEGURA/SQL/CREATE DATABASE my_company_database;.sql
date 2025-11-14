CREATE DATABASE my_company_database;

--práctica1
--Crea una tabla llamada employees que contenga los siguientes campos:
--Id
--birth_date
--first_name
--last_name
--Importante: los campos id, first_name y last_name deben ser NOT NULL, y id debe ser la clave primaria de la tabla.

CREATE TABLE IF NOT EXISTS employees (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE,
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL
);

--práctica 2. 
--Añade tres columnas a la tabla employees:
-- salary: tipo NUMERIC(10,2)
-- title: tipo VARCHAR de máximo 100 caracteres.
-- title_date: tipo DATE

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

--práctica 3
-- Inserta al menos 15 empleados nuevos en la tabla employees, que cumplan los siguientes criterios: 
-- Al menos 3 empleados deben tener el mismo nombre.
-- Los salarios deben variar entre 5000 y 50.000.
-- Todos los empleados deben tener un título.
-- Al menos 5 empleados deben tener title_date del año 2020.
-- Selecciona todos tus empleados
-- Selecciona todos tus empleados mostrando solamente el first_name y salary

INSERT INTO employees (birth_date,first_name, last_name, salary,title,title_date)
VALUES ('1998-03-11','Martha','Segura',40.000,'Journalist','2025-10-24');
SELECT * FROM employees;

INSERT INTO employees (birth_date,first_name, last_name, salary,title,title_date)
VALUES ('1995-07-22','Martha','López',35000,'Editor','2020-05-12'),

('1989-02-15','Martha','Ruiz',27000,'Content Manager','2020-09-18'),
('1992-08-03','Daniel','Martínez',18000,'Photographer','2021-04-07'),
('1988-11-30','Lucía','Gómez',42000,'Copywriter','2023-07-15'),
('1999-05-25','Alejandro','Pérez',15000,'Social Media Specialist','2020-02-20'),
('1990-01-10','Laura','Fernández',5000,'Designer','2024-09-10'),
('1985-12-19','Sergio','Torres',47000,'Video Producer','2022-12-02'),
('1993-04-08','Andrea','Morales',39000,'Marketing Analyst','2020-06-29'),
('1996-09-27','Javier','Santos',21000,'Camera Operator','2025-02-01'),
('1997-06-12','Elena','Navarro',12000,'Public Relations','2023-03-11'),
('1991-10-05','Carlos','Jiménez',31000,'Sound Engineer','2020-01-10'),
('1987-08-22','Patricia','Castro',48000,'Creative Director','2024-08-18'),
('1994-02-20','Raúl','Vega',26000,'Assistant Editor','2020-11-23'),
('2000-12-14','Isabel','Ortega',8000,'Community Manager','2023-10-09');

SELECT * FROM employees;

--práctica 4
-- Muestra el empleado cuyo id sea 2
-- Selecciona todos los empleados con un salario superor a 20000
-- Selecciona todos los empleados con un salario inferior o igual a 10000
SELECT * FROM employees WHERE id = 2; 
SELECT * FROM employees WHERE salary >= 20000;
SELECT * FROM employees WHERE salary <= 10000;

--práctica 5
-- Actualiza el first_name del empleado cuyo id sea 7
-- Elimina al empleado cuyo id sea 5
-- Elimina a todos los empleados con un salario super a 20000
-- Selecciona todos los empleados con un salario entre 14.000 y 50.000
-- Ordena los empleados por birth_date de forma descendiente

UPDATE employees SET first_name= "Fina" WHERE id=7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;
SELECT * FROM employees;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

--práctica6
-- Muestra los first_name de los empleados sin repetir
-- Muestrame el nombre completo del empleado como “nombre_completo” cuyo id 9
-- Muestra los empleados cuyo nombre empiece por P
-- Muestra los empleados cuyo nombre contenga la a

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=1;
SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

--práctica 7
-- Muestra el número total de empleados
-- Muestra el empleado con el salario más alto
SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT AVG (salary)FROM employees;
SELECT title, MAX (salary), MIN (salary) FROM employees GROUP BY title;

--práctica 8
--Muestra el first_name y salary de cada empleado redondeando a 2 decimales

SELECT  first_name, 
    ROUND(salary, 2) AS salary_redondeado
FROM employees;

--práctica 9 (extra)

--clase 31/10 SQL 
-- Práctica 2.1
--crea una tabla llamada departments que contenga un campo llamado name
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT 
);
SELECT * FROM departments;

--inserta dos departamentos en la nueva tabla departments, por ejemplo engineering y marketing
INSERT INTO departments (name)
VALUES ('Marketing');
INSERT INTO departments (name)
VALUES ('Engineering');
SELECT * FROM departments;

--Práctica 2.2 
--Modifica tu tabla de employees y añade la FK department_id que haga referencia al id de la tabla departments.
ALTER TABLE employees ADD COLUMN department_id INTEGER;
SELECT * FROM employees;

--Actualiza tres empleados en la tabla employees: 
--Asigna dos empleados al departamento Engineering , 
--Asigna un empleado al departamento Marketing.

UPDATE employees SET department_id = 2 WHERE id =1;
UPDATE employees SET department_id = 2 WHERE id =4;
UPDATE employees SET department_id = 1 WHERE id =7;
SELECT * FROM employees;

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.
SELECT 
employees.id,
employees.first_name,
employees.last_name,
employees.salary,
departments.name AS department_name
FROM employees
JOIN departments
ON employees.department_id = departments.id;
SELECT * FROM employees;

--EXTRA: Muestra todos los empleados con sus departamentos independientemente de si tienen departamento o no


