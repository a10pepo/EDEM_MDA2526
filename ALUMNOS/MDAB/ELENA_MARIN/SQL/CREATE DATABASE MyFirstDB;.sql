CREATE DATABASE nueva_db;

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL

);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees(birth_date, first_name, last_name, salary, title, title_date)
VALUES('1980-12-01', 'María', 'Perez', 30000, 'Medico', '2010-01-21'),
('1990-03-15', 'María', 'Gonzalez', 45000, 'Medico', '2018-06-10'),
('1985-07-22', 'Carlos', 'Ramirez', 32000, 'Enfermero', '2020-02-15'),
('1992-11-03', 'Ana', 'Lopez', 28000, 'Administrativo', '2019-08-20'),
('1988-09-10', 'Jorge', 'Martinez', 50000, 'Cirujano', '2020-05-12'),
('1995-04-25', 'Lucia', 'Fernandez', 15000, 'Auxiliar', '2021-03-01'),
('1993-12-30', 'María', 'Torres', 36000, 'Medico', '2020-07-07'),
('1998-06-19', 'Pedro', 'Sanchez', 12000, 'Recepcionista', '2017-11-14'),
('1991-02-08', 'María', 'Rojas', 47000, 'Pediatra', '2020-09-23'),
('1987-10-12', 'Andres', 'Vega', 22000, 'Farmacéutico', '2016-05-19'),
('1994-01-17', 'Camila', 'Diaz', 38000, 'Enfermera', '2020-12-30'),
('1989-08-05', 'Sergio', 'Morales', 26000, 'Técnico', '2015-04-10'),
('1996-03-29', 'Laura', 'Jimenez', 42000, 'Odontóloga', '2020-01-05'),
('1997-07-14', 'Fernando', 'Ruiz', 18000, 'Paramédico', '2019-09-25'),
('1986-11-20', 'Natalia', 'Castro', 31000, 'Psicóloga', '2018-02-18');

SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET salary=40000 WHERE id=1;
SELECT * FROM employees where id=1;

DELETE FROM employees WHERE id=5;
SELECT * FROM employees;

SELECT * FROM employees ORDER BY id DESC;

SELECT * FROM employees WHERE salary BETWEEN 15000 AND 30000;

UPDATE employees SET first_name= 'Marta' WHERE id=7;
SELECT * FROM employees;

DELETE FROM employees WHERE id=6;

DELETE FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT first_name || ' ' || last_name AS NOMBRE_COMPLETO from employees;
SELECT DISTINCT salary FROM employees;

SELECT * FROM employees WHERE first_name LIKE '%a%';
SELECT * FROM employees WHERE last_name NOT LIKE '%r%';

-- Muestra los first_name de los empleados sin repetir

SELECT DISTINCT first_name FROM employees;

-- Muestrame el nombre completo del empleado como nombre_completo cuyo id=21

SELECT first_name || ' ' || last_name AS NOMBRE_COMPLETO from employees WHERE id=21;

--  Muestra los empleados cuyo nombre empiece por P

SELECT * FROM employees WHERE first_name LIKE 'P%';

-- Muestra los empleados cuyo nombre contenga la a

SELECT * FROM employees WHERE first_name LIKE '%a%'


SELECT COUNT(id) FROM employees;
SELECT salary, COUNT(salary) FROM employees GROUP BY salary;

-- Muestra el número total de empleados
SELECT COUNT(id) FROM employees;
SELECT COUNT(*) FROM employees;

-- Muestra el empleado con el salario más alto
SELECT MAX (salary) FROM employees;

-- Muestra el salario medio por titulo
SELECT title, AVG(salary) FROM employees GROUP BY title;

-- Muestra el salario máximo y mínimo por título
SELECT title, MIN(salary), MAX(salary) FROM employees GROUP BY title;

-- Calcular valores con columnas numéricas
SELECT first_name, salary,
    salary * 0.12 AS ahorro_mensual
FROM employees;

-- Muestra el first_name y salary de cada empleado redondeando a 2 decimales
SELECT first_name, salary, 
    ROUND(salary,2) AS salario_redondeado
FROM employees

-- EJERCICIO EXTRA. Escribe una consulta SQL que, a partir de la tabla employees, 
-- calcule el importe de impuestos aplicando un 21 % sobre el salario bruto 
-- y obtenga el salario neto (bruto − impuestos), 
-- mostrando los resultados con 2 decimales y usando alias (AS) claros.

SELECT salary, salary*0.21 AS importe_de_impuestos FROM employees;

-- Calcular la columna impuestos como el 21 % del salario (salary * 0.21) y redondearla a 2 decimales.
-- Calcular la columna salario_neto como salary - impuestos, también redondeada a 2 decimales.
-- Usar alias (AS) exactamente con los nombres: impuestos y salario_neto

SELECT
    salary AS "Salario_Bruto",
    ROUND(salary * 0.21, 2) AS "Impuesto_21%",
    ROUND(salary - (salary * 0.21), 2) AS "Salario_Neto"
FROM
    employees;


-- PRACTICA 2

-- Crea una tabla llamada departments que contenga un campo llamado name.

CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL

);

-- TABLA EMPLOYEES (ya creada pero no me aparecía, por tanto, la he vuelto a crear)

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL

);

-- Inserta dos departamentos en la nueva tabla departments, por ejemplo:
    -- Engineering
    -- Marketing

-- Inserta 1 departamento.
-- Muestra todos los departamentos.

SELECT * FROM employees
SELECT * FROM departments

INSERT INTO departments(department_name)
VALUES ('engineering'), ('marketing')

SELECT * FROM departments 

--Modifica tu tabla de employees y añade la FK department_id que haga referencia al id de la tabla departments.

ALTER TABLE employees
ADD COLUMN department_id INT REFERENCES departments(id); -- añadir una columna que haga referencia a la columna departments(id)

--Actualiza tres empleados en la tabla employees:
    --Asigna dos empleados al departamento Engineering.
    -- Asigna un empleado al departamento Marketing.

UPDATE employees SET department_id = 2 where id = 1; -- department_id = 2 ES EL ID DEL DEPARTAMENTO
UPDATE employees SET department_id = 2 where id = 2;

SELECT * FROM employees;

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.

SELECT e.first_name, d.department_name
FROM employees AS e
INNER JOIN departments as d
ON e.department_id = d.id; -- e. y d. son ALIAS que corresponden a employees y a department

SELECT * FROM employees;



