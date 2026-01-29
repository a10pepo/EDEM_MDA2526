CREATE TABLE IF NOT EXISTS employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN IF NOT EXISTS salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title VARCHAR(100);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES
('1990-06-12', 'Alex',      'García',     42000, 'Software Engineer',        '2020-02-14'),
('1988-11-03', 'Alex',      'Santos',     38000, 'Data Analyst',             '2020-05-21'),
('1985-04-22', 'Alex',      'Navarro',    45000, 'DevOps Engineer',          '2020-09-07'),
('1982-09-15', 'Lucía',     'Martínez',   48000, 'Product Manager',          '2020-01-30'),
('1982-09-15', 'Lucía',     'Martínez',   50000, 'Product Manager',          '2020-01-30'),
('1995-01-08', 'Diego',     'Ruiz',       27000, 'QA Engineer',              '2019-11-12'),
('1992-12-27', 'María',     'López',      36000, 'UX Designer',              '2021-03-18'),
('2002-05-14', 'Sofía',     'Hernández',  18000, 'Support Specialist',       '2018-07-22'),
('1980-02-02', 'Javier',    'Iglesias',   49000, 'Solutions Architect',      '2022-04-01'),
('1978-07-09', 'Elena',     'Vidal',      22000, 'Technical Writer',         '2017-10-05'),
('1999-03-30', 'Pablo',     'Serrano',    15000, 'IT Technician',            '2016-06-15'),
('1990-10-10', 'Nuria',     'Cano',       34000, 'Business Analyst',         '2023-02-09'),
('1970-01-20', 'Raúl',      'Ortega',     12000, 'SysAdmin',                 '2015-12-19'),
('1994-08-03', 'Carla',     'Benítez',    26000, 'Marketing Specialist',     '2024-08-27'),
('2001-11-25', 'Hugo',      'Molina',      8000, 'Junior Developer',         '2022-10-11');

SELECT * FROM employees;
SELECT first_name, salary FROM employees;
SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary = 2000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Javier' WHERE id = 7;

DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary >= 200000;

SELECT * FROM employees ORDER BY salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id= 9;

SELECT * FROM employees WHERE first_name LIKE 'P%';

SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) FROM employees GROUP BY title;


SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, ROUND(salary, 2) FROM employees;

SELECT
    first_name,
    ROUND(salary, 2) AS salary,
    ROUND(salary * 0.21, 2) AS impuestos,
    ROUND(salary - ROUND(salary * 0.21, 2), 2) AS salario_neto
FROM employees;



CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO departments (name) VALUES
('Ingeniería'),
('Recursos Humanos'),
('Finanzas'),
('Marketing'),
('Ventas');

SELECT * FROM departments;

ALTER TABLE employees ADD COLUMN IF NOT EXISTS department_id BIGINT;

INSERT INTO employees (
    birth_date, first_name, last_name, salary, title, title_date, department_id
) VALUES (
    '1993-07-21', 'Ana', 'Ruiz', 32000, 'Backend Developer', '2024-01-02',
    (SELECT id FROM departments WHERE name = 'Ingeniería' LIMIT 1)
);

SELECT * FROM employees;

SELECT e.*, d.name AS department
FROM employees e
JOIN departments d ON e.department_id = d.id;

SELECT e.*, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;