-- En myFirstDB (donde tenía creada la tabla de employees)

CREATE TABLE IF NOT EXISTS departments (
    id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name    VARCHAR NOT NULL
);

INSERT INTO departments (name)
VALUES
('Engineering'),
('Marketing')
;

SELECT * FROM departments;

ALTER TABLE employees ADD COLUMN department_id BIGINT REFERENCES departments(id);

SELECT * FROM departments; -- 1: Engineering; 2: Marketing;

INSERT INTO employees(birth_date, first_name, last_name, salary, title, title_date, department_id)
VALUES
('2011-11-11', 'Perico', 'Palotes', 25000.00, 'Analista de Datos', '2024-07-01', 1),
('2010-07-11', 'Pepito', 'Toledo', 20000.00, 'Analista de Datos', '2023-10-03', 1),
('2007-04-21', 'Raúl', 'Navarro', 35000.00, 'Fisioterapeuta', '2025-10-10', 2)
;

UPDATE employees SET department_id = 2 WHERE id = 8;
UPDATE employees SET department_id = 2 WHERE id = 9;
UPDATE employees SET department_id = 1 WHERE id = 11;

SELECT * FROM employees;

SELECT *
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id;

SELECT CONCAT(e.first_name, e.last_name) AS full_name, d.name AS department
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id;


-- EXTRA Práctica from Diapo 39/47 (SQL II)
SELECT CONCAT(e.first_name, e.last_name) AS full_name, d.name
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id;


-- EXTRA Práctica from Diapo 43/47 (SQL II)
-- Inserta departamentos
INSERT INTO departments(name)
VALUES 
('Sales'),
('HR'),
('R&D'),
('Legal')
;

SELECT id, department_id FROM employees;

-- Asigno departamentos a empleados
UPDATE employees
SET department_id = CASE id
WHEN 13 THEN 1         -- 4 into Engineering
WHEN 17 THEN 1
WHEN 18 THEN 1
WHEN 21 THEN 1
WHEN 19 THEN 2         -- 3 into Marketing
WHEN 22 THEN 2
WHEN 14 THEN 2
WHEN 26 THEN 3         -- +2 into Sales
WHEN 16 THEN 3
WHEN 27 THEN 4         -- +1 into HR
WHEN 23 THEN 5         -- +1 into R&D
WHEN 20 THEN 6         -- +1 into Legal
END;

SELECT e.id, e.department_id, d.id, d.name
FROM employees AS e 
LEFT JOIN departments as d
ON e.department_id = d.id
ORDER BY d.id ASC;

-- Salarys per department
UPDATE employees
SET salary = CASE id
WHEN 18 THEN 42000
WHEN 17 THEN 55000
WHEN 13 THEN 63500
WHEN 21 THEN 75000
WHEN 14 THEN 33000
WHEN 19 THEN 39500
WHEN 22 THEN 48000
WHEN 16 THEN 28000
WHEN 26 THEN 52000
WHEN 27 THEN 31000
WHEN 11 THEN 24000
WHEN 24 THEN 27000
ELSE salary
END;

SELECT e.id, e.department_id, d.name, e.salary
FROM employees AS e 
LEFT JOIN departments as d
ON e.department_id = d.id
ORDER BY d.id ASC;

-- Title
UPDATE employees
SET title = CASE id
WHEN 18 THEN 'Backend Engineer'
WHEN 17 THEN 'Frontend Engineer'
WHEN 13 THEN 'Data Engineer'
WHEN 21 THEN 'DevOps'
WHEN 14 THEN 'SEO Specialist'
WHEN 19 THEN 'Content Manager'
WHEN 22 THEN 'Brand Manager'
WHEN 16 THEN 'Sales Rep'
WHEN 26 THEN 'Account Executive'
WHEN 27 THEN 'HR Generalist'
WHEN 23 THEN 'Support'
WHEN 20 THEN 'Support'
WHEN 11 THEN 'Intern'
WHEN 24 THEN 'Support'
ELSE title
END;

SELECT e.id, e.title, d.name, e.salary
FROM employees AS e 
LEFT JOIN departments as d
ON e.department_id = d.id
ORDER BY d.id ASC;

-- Dates
-- birth_date between 1995 and 2003
-- title_date between 2023 and 2025
UPDATE employees
SET birth_date = CASE
WHEN birth_date NOT BETWEEN '1995-01-01' AND '2003-12-31'
THEN (TIMESTAMP '1995-01-01' + RANDOM() * (TIMESTAMP '2003-12-31' - TIMESTAMP '1995-01-01'))::DATE
ELSE birth_date
END;

UPDATE employees
SET title_date = CASE
WHEN title_date NOT BETWEEN '2023-01-01' AND '2025-12-31'
THEN (TIMESTAMP '2023-01-01' + RANDOM() * (TIMESTAMP '2025-12-31' - TIMESTAMP '2023-01-01'))::DATE
ELSE title_date
END;

SELECT id, birth_date, title_date FROM employees
WHERE birth_date NOT BETWEEN '1995-01-01' AND '2003-12-31'
OR title_date NOT BETWEEN '2023-01-01' AND '2025-12-21'
;

-- Lista solo empleados que tienen departamento (INNER JOIN).
SELECT * FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id;

-- Muestra departamentos sin empleados (LEFT JOIN + IS NULL).
SELECT * FROM departments AS d
LEFT JOIN employees AS e
ON e.department_id IS NULL;

-- Cuenta cuántos empleados hay por departamento (nombre y COUNT).
SELECT d.name AS Department, COUNT(e.id)
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
GROUP BY d.id
ORDER BY d.id ASC
;

-- Empleados del departamento ‘Engineering’ (por nombre de dept).Salario medio por departamento (nombre y AVG(salary)).
SELECT d.name AS Department, ROUND(AVG(e.salary), 2)
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
GROUP BY d.id
ORDER BY d.id ASC;

-- Salario máximo por departamento y qué departamento lo tiene.
SELECT d.name AS Department, MAX(e.salary)
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
GROUP BY d.id
ORDER BY d.id ASC;

-- Número de títulos distintos por departamento.
SELECT d.name AS Departmente, COUNT(DISTINCT e.title)
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
GROUP BY d.id
ORDER BY d.id ASC;

-- Empleados con su departamento, ordenado por department.name y last_name.
SELECT e.id, first_name, last_name, d.name AS Department
FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id
ORDER BY d.name ASC, last_name;

-- Top 3 departamentos con más empleados.
SELECT d.name AS Department, COUNT(e.id)
FROM employees AS e
INNER JOIN departments AS d
ON e.department_id = d.id
GROUP BY d.id
ORDER BY COUNT(e.id) DESC
LIMIT 3;
