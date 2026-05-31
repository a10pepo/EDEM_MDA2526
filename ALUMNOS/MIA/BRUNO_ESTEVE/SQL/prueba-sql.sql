-- Creacion de la base de datos
CREATE DATABASE my_company_database;

-- Creacion de la tabla empleados
CREATE TABLE employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_day DATE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

-- Anadir columnas a la tabla empleados
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

-- Insertar datos en la tabla empleados
-- TRUNCATE TABLE employees;
INSERT INTO employees (birth_day, first_name, last_name, salary, title, title_date)
VALUES
    ('2003-06-30', 'Bruno',  'Esteve',   50000.00, 'Data-Analist',        '2025-06-30'),
    ('1998-11-12', 'Alex',   'García',   27500.00, 'Data Analyst',         '2020-03-15'),
    ('1995-05-05', 'Alex',   'López',    18000.00, 'BI Developer',         '2020-07-22'),
    ('1992-01-20', 'Alex',   'Martín',   36000.00, 'Data Engineer',        '2020-10-10'),
    ('1988-02-14', 'Marta',  'Ruiz',     23000.75, 'Project Manager',      '2019-12-03'),
    ('1999-09-09', 'Lucía',  'Pérez',    32000.00, 'Security Specialist',  '2020-08-08'),
    ('1994-03-28', 'Carlos', 'Sánchez',  15000.25, 'Network Engineer',     '2021-11-17'),
    ('1997-07-31', 'Daniel', 'Gómez',    41500.00, 'QA Analyst',           '2020-04-29'),
    ('1990-10-22', 'Elena',  'Torres',    9800.00, 'Product Owner',        '2022-02-01'),
    ('1985-12-11', 'Javier', 'Navarro',   5200.00, 'HR Specialist',        '2020-05-05'),
    ('2000-04-07', 'Paula',  'Romero',   27500.00, 'Finance Analyst',      '2023-09-18'),
    ('1993-06-19', 'Sergio', 'Castillo', 45500.00, 'Full-Stack Developer', '2018-01-27'),
    ('1996-08-25', 'Nuria',  'Vidal',    12500.00, 'DevOps Engineer',      '2021-06-12'),
    ('1991-03-03', 'Irene',  'Campos',    5000.00, 'UX Designer',          '2020-03-20'),
    ('1989-01-16', 'David',  'Ortiz',    34000.00, 'Support Technician',   '2024-07-14');

-- Consulta la informacion de la tabla empleados
SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

-- Actualizacion de datos de la tabla empleados
UPDATE employees SET first_name = 'Sergio' WHERE id = 7;

-- Borrar datos en la tabla empleados 
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;

-- BETWEEN 
SELECT * 
FROM employees 
WHERE salary BETWEEN 14000 AND 50000;

-- ORDER BY 
SELECT * 
FROM employees 
ORDER BY birth_day DESC;

-- DISTINC 
SELECT DISTINCT first_name 
FROM employees;

-- CONCAT
SELECT first_name || ' ' || last_name AS nombre_completo
FROM employees 
WHERE id = 20;

-- LIKE / NOT LIKE 
SELECT * 
FROM employees
WHERE first_name LIKE '%P';

SELECT * 
FROM employees
WHERE first_name LIKE '%a%';

-- FUNCIONES SELECT 
SELECT COUNT(*)
FROM employees;

SELECT first_name, last_name, salary
FROM employees
WHERE salary in (SELECT MAX(salary) FROM employees);

-- ROUND 
SELECT first_name, ROUND (salary,2) AS salario
FROM employees;

-- EXTRA
SELECT 
    first_name
    , salary 
    , ROUND(salary * 0.21, 2) AS impuestos
    , ROUND(salary - ROUND(salary * 0.21, 2), 2) AS salario_neto
FROM 
    employees;


-- DIA 2 

-- Crear tabla departments
CREATE TABLE departments(
    id_dep INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name_dep VARCHAR(100)
);

-- Alterar la tabla de empleados para añadir la foreign key
ALTER TABLE employees
ADD COLUMN id_dep INTEGER;

ALTER TABLE employees 
ADD CONSTRAINT fk_employees_department
FOREIGN KEY (id_dep)
REFERENCES departments(id_dep);

-- Insertar dos departamentos
SELECT * FROM departments;
INSERT INTO departments (name_dep) VALUES
('Engineering'),
('Marketing');

-- Actualiza tres empleados 
UPDATE employees
SET id_dep = 3
WHERE id = 31 or id = 32;

UPDATE employees
SET id_dep = 4
WHERE id = 33;

-- Consulta join
SELECT e.*, d.name_dep
FROM employees e
LEFT JOIN departments d
ON e.id_dep = d.id_dep;

-- EXTRA I
-- Insert de departamentos
INSERT INTO departments (name_dep) VALUES
('Sales'),
('HR'),
('R&D'),
('Legal');

SELECT * FROM departments;

-- Inserta empleados
INSERT INTO employees (birth_day, first_name, last_name, salary, title, title_date, id_dep) VALUES
('1990-05-15', 'Ana', 'Lopez', 45000, 'Software Engineer', '2022-01-10', 3),
('1987-09-23', 'Luis', 'Martinez', 48000, 'DevOps Engineer', '2021-11-05', 3),
('1992-12-11', 'Sofia', 'Gonzalez', 42000, 'QA Engineer', '2023-03-15', 3),
('1985-07-30', 'Jorge', 'Hernandez', 50000, 'Data Scientist', '2020-06-20', 3),
('1993-03-22', 'Marta', 'Sanchez', 35000, 'Marketing Specialist', '2022-09-12', 4),
('1991-11-14', 'Pablo', 'Ramirez', 37000, 'Content Strategist', '2021-08-30', 4),
('1989-04-18', 'Elena', 'Diaz', 36000, 'SEO Analyst', '2023-02-25', 4),
('1994-06-05', 'Carlos', 'Vargas', 30000, 'Sales Executive', '2022-12-01', 13),
('1995-08-29', 'Lucia', 'Molina', 32000, 'Account Manager', '2021-10-14', 13),
('1988-10-10', 'Sergio', 'Castro', 28000, 'HR Coordinator', '2020-04-18', 14),
('1996-01-15', 'Isabel', 'Ortiz', 40000, 'Business Analyst', '2023-05-22', NULL),
('1997-02-20', 'Diego', 'Silva', 39000, 'Project Coordinator', '2022-07-09', NULL);

-- EXTRA II
-- Inner join
SELECT employees.*, departments.name_dep
FROM employees 
INNER JOIN departments
ON employees.id_dep = departments.id_dep;

-- Left join
SELECT DISTINCT(d.name_dep) FROM departments d
LEFT JOIN employees e
ON e.id_dep = d.id_dep
WHERE e.id_dep is NULL;

-- COUNT
SELECT d.name_dep, count(*) as num_empleados
FROM employees e
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep;

-- Empleados del departamento 'Engineering'
SELECT e.*, d.name_dep 
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
WHERE d.name_dep like 'Engineering';

-- Salario medio por departamento
SELECT d.name_dep, ROUND(AVG(e.salary)) as salario_medio
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep;


-- Salario máximo por departamento
SELECT d.name_dep, ROUND(MAX(e.salary)) as salario_medio
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep;

-- Salario máximo por departamento (quien lo tiene)
SELECT d.name_dep, ROUND(MAX(e.salary)) as salario_medio
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep
ORDER BY 2 DESC;

-- Titulos distintos por departamento
SELECT d.name_dep, COUNT(DISTINCT title) as n_titulos
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep
ORDER BY 2 DESC;

-- Empleados con su departamento 
SELECT e.*, d.name_dep 
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
ORDER BY d.name_dep, e.last_name;

-- TOP tres empleados con mas departamentos
SELECT d.name_dep, COUNT(*) as n_empleados
FROM employees e 
INNER JOIN departments d
ON d.id_dep = e.id_dep
GROUP BY d.name_dep
ORDER BY 2 DESC
LIMIT 3;


-- Practica clase III

-- Insertar un departamento
INSERT INTO departments (name_dep) VALUES
('Artificial Intelligence');

-- Mostrar todos departamentos
SELECT * FROM departments;

-- Insertar un empleado con departamento
INSERT INTO employees (birth_day, first_name, last_name, salary, title, title_date, id_dep) VALUES
('2004-08-28', 'Carla', 'Garcia', 25000, 'Graphic designer', '2025-06-30', 4);

-- Mostrar todos los empleados
SELECT * FROM employees;

-- Mostrar empleados junto con el nombre del departamento al que pertenecen
SELECT e.*, d.name_dep
FROM employees e
INNER JOIN departments d
ON e.id_dep = d.id_dep;

-- EXTRA
SELECT e.*, d.name_dep
FROM employees e
LEFT JOIN departments d
ON e.id_dep = d.id_dep;


SELECT * FROM employees;
SELECT * FROM departments;




