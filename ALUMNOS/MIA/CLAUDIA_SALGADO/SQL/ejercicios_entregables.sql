
-- CLASE 1
CREATE TABLE IF NOT EXISTS employees (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  birth_date     DATE,
  first_name     VARCHAR(100) NOT NULL,
  last_name      VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (first_name, last_name, birth_date, salary,title,title_date) 
VALUES 
  ('Claudia','Salgado','2003-04-30',50000,'CEO','2025-1-1'),
  ('Alex',   'Gomez',   '1998-03-12', 18000, 'Analyst',            '2020-05-10'),
  ('Alex',   'Rivera',  '1997-07-22', 32000, 'Engineer',           '2020-09-01'),
  ('Alex',   'Perez',   '1995-11-05', 27000, 'Support Specialist', '2021-02-15'),
  ('Marta',  'Lopez',   '1999-01-30', 45000, 'Manager',            '2020-03-20'),
  ('Luis',   'Torres',  '2000-06-18',  5000, 'Intern',             '2020-12-01'),
  ('Irene',  'Ruiz',    '1996-09-09', 41000, 'Data Scientist',     '2020-07-07'),
  ('Diego',  'Vidal',   '1994-04-14', 23000, 'QA Engineer',        '2019-11-11'),
  ('Sara',   'Marin',   '1998-08-02', 38000, 'Product Manager',    '2021-06-30'),
  ('Julia',  'Ortiz',   '1993-02-27', 12500, 'HR Specialist',      '2020-01-15'),
  ('Pablo',  'Cano',    '1990-10-10', 34000, 'DevOps Engineer',    '2022-05-05'),
  ('Nuria',  'Vera',    '2001-12-12', 29000, 'UX Designer',        '2023-09-09'),
  ('Miguel', 'Soler',   '1992-05-25', 47000, 'CFO',                '2020-10-10'),
  ('Bruno',  'Serra',   '1989-03-03', 36000, 'CTO',                '2024-04-04'),
  ('Elena',  'Rios',    '1997-07-07', 15000, 'Marketing Lead',     '2020-02-02');

SELECT * FROM employees;
SELECT first_name, salary from employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET first_name = 'Pepita' WHERE id=7;

-- DELETE FROM employees WHERE id = 5;
-- DELETE FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;

SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT *
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

-- EXTRA
SELECT title, ROUND(AVG(salary),2) AS salario_medio FROM employees GROUP BY title;
SELECT title, MAX(salary) AS salario_max, MIN(salary) AS salario_min FROM employees GROUP BY title;

SELECT first_name, ROUND(salary,2) AS salario FROM employees;

-- EXTRA
SELECT first_name, 
    salary,
    ROUND(salary*0.21,2) AS impuestos,
    ROUND(salary-ROUND(salary*0.21,2),2) AS salario_neto 
FROM employees;

-- CLASE 2
CREATE TABLE IF NOT EXISTS departments (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name     VARCHAR(100)
);

ALTER TABLE employees ADD COLUMN IF NOT EXISTS department_id  INTEGER REFERENCES departments(id);

INSERT INTO departments (name)
VALUES 
  ('Engineering'),
  ('Marketing');

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name='Engineering')
WHERE id IN (1,2);

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name='Marketing')
WHERE id IN (3);

SELECT employees.first_name || ' ' || employees.last_name AS Nombre,
departments.name AS Departamento
FROM employees
LEFT JOIN departments
ON departments.id = employees.department_id;

-- CLASE 3
INSERT INTO departments (name) VALUES ('Cleaning');

SELECT * FROM departments;

INSERT INTO employees (first_name, last_name, department_id) VALUES ('Guzman', 'González',2);

SELECT * FROM employees;

SELECT employees.first_name, departments.name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;

-- EXTRA
SELECT employees.first_name, departments.name
FROM employees
LEFT JOIN departments
ON employees.department_id = departments.id;