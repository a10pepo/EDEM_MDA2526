--Creación de la tabla
CREATE TABLE IF NOT EXISTS users (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password TEXT NOT NULL,
register_date TIMESTAMPTZ NOT NULL DEFAULT now()
);
DROP TABLE users;

TRUNCATE users;

--Práctica 1
CREATE TABLE IF NOT EXISTS employees (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
birth_date DATE NOT NULL,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL);

--Práctica 2
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

--Práctica 3
INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
VALUES 
('Mario', 'García', '2000-08-20', 100, 'Data Engineer', '2022-06-01'),
('Ana', 'López', '1998-03-15', 120, 'Data Analyst', '2021-09-10'),
('Carlos', 'Fernández', '1995-11-02', 150, 'Backend Developer', '2020-02-05'),
('Lucía', 'Martínez', '1999-07-27', 130, 'Frontend Developer', '2023-01-18'),
('Javier', 'Torres', '1990-12-09', 180, 'Project Manager', '2019-04-01'),
('Sofía', 'Hernández', '2001-05-30', 95, 'Junior Data Scientist', '2023-08-25'),
('Pablo', 'Ruiz', '1997-09-11', 110, 'QA Engineer', '2021-07-14'),
('Marta', 'Navarro', '1996-01-23', 140, 'UX Designer', '2020-10-03'),
('Hugo', 'Santos', '1994-02-06', 200, 'Tech Lead', '2018-03-12'),
('Elena', 'Vega', '1993-06-19', 160, 'Product Owner', '2019-09-28'),
('Raúl', 'Castro', '1998-10-08', 125, 'Data Engineer', '2021-11-11'),
('Clara', 'Mendoza', '1992-04-05', 175, 'Scrum Master', '2018-06-02'),
('Andrés', 'Jiménez', '1999-12-21', 115, 'DevOps Engineer', '2022-09-07'),
('Patricia', 'Silva', '1997-01-10', 135, 'Business Analyst', '2020-05-22'),
('Diego', 'Morales', '1995-03-29', 155, 'Database Administrator', '2019-07-16'),
('Laura', 'Ortega', '2000-09-13', 105, 'Data Engineer', '2023-01-05');

--Práctica 4
SELECT * 
FROM employees;

SELECT first_name, salary
FROM employees;

--Práctica 5
SELECT *
FROM employees
WHERE id=2;

SELECT *
FROM employees
WHERE salary>20000;

SELECT *
FROM employees
WHERE salary<=10000;

--Práctica 6
UPDATE employees SET first_name='David' WHERE id = 7;
SELECT * FROM employees;

--Práctica 7
DELETE FROM employees WHERE id = 5;
SELECT * FROM employees;

DELETE FROM employees WHERE salary>20000;
SELECT * FROM employees;


--Práctica 8
SELECT * FROM employees WHERE salary BETWEEN 14000 and 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

--Práctica 9
SELECT DISTINCT first_name FROM employees ;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;

--Práctica 10
SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

--Práctica 11
SELECT COUNT(id) FROM employees;
SELECT * FROM employees
WHERE salary = (
    SELECT MAX(salary)
    FROM employees
);


--EXTRA
SELECT AVG(salary) FROM employees GROUP BY title;
SELECT MAX(salary),MIN(salary),title FROM employees GROUP BY title;

--Práctica 12
SELECT first_name, ROUND(salary,2) FROM employees;

--EXTRA
SELECT first_name,salary, ROUND(salary*0.21,2) AS impuestos, 
ROUND(salary-ROUND(salary*0.21,2),2) AS salario_neto
FROM employees;




---------
--DÍA 2
---------
--Práctica 1
CREATE TABLE IF NOT EXISTS departments (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(100) NOT NULL);

SELECT *
FROM employees;

ALTER TABLE employees
ADD COLUMN id_dep INTEGER;

ALTER TABLE employees
ADD CONSTRAINT fk_employees_department
FOREIGN KEY (id_dep)
REFERENCES departments(id);

INSERT INTO departments(name) VALUES
('Engineering'),('Markting');

UPDATE employees
SET id_dep=1
WHERE id=9 or id=10;

UPDATE employees
SET id_dep=2
WHERE id=12;

SELECT departments.name,employees.first_name, employees.last_name
FROM employees INNER JOIN departments on employees.id_dep=departments.id;

--EXTRA 1
INSERT INTO departments(name) VALUES
('Sales'),('HR'),('R&D'),('LEGAL');

SELECT *
FROM employees;
INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, id_dep)
VALUES
('1990-04-15', 'Carlos', 'Pérez', 4500.00, 'Engineer', '2020-05-10', 1),
('1988-11-02', 'Laura', 'Gómez', 4800.00, 'Senior Engineer', '2019-03-15', 1),
('1992-07-21', 'Andrés', 'Ruiz', 4200.00, 'Engineer', '2021-01-25', 1),
('1985-12-09', 'Marta', 'López', 5000.00, 'Tech Lead', '2018-10-30', 1),
('1993-06-18', 'Sofía', 'Martínez', 3700.00, 'Marketing Specialist', '2021-04-12', 2),
('1989-09-07', 'Javier', 'Torres', 3900.00, 'SEO Analyst', '2020-07-19', 2),
('1995-01-30', 'Elena', 'Castro', 3600.00, 'Content Manager', '2022-02-10', 2),
('1991-03-25', 'Pablo', 'Fernández', 4100.00, 'Sales Executive', '2020-11-03', 4),
('1987-10-14', 'Natalia', 'Vega', 4300.00, 'Account Manager', '2019-06-28', 4),
('1990-08-05', 'Raúl', 'Sánchez', 3800.00, 'HR Specialist', '2021-09-14', 5),
('1994-02-16', 'Lucía', 'Morales', 3500.00, 'Support', '2022-05-05', NULL),
('1986-07-22', 'Diego', 'Navarro', 3300.00, 'Assistant', '2023-01-20', NULL);

--EXTRA 2
SELECT em.first_name,em.last_name,dep.name 
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id;

SELECT em.first_name,em.last_name
FROM employees em 
LEFT JOIN departments dep 
ON em.id_dep=dep.id
WHERE dep.id IS NULL;

SELECT count(em.first_name),dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
GROUP BY dep.name;

SELECT em.first_name,em.last_name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
WHERE dep.name='Engineering';

SELECT ROUND(AVG(em.salary),2),dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
WHERE dep.name IS NOT NULL
GROUP BY dep.name;

SELECT MAX(em.salary),2,dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
WHERE dep.name IS NOT NULL
GROUP BY dep.name;

SELECT COUNT(DISTINCT(em.title)),dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
GROUP BY dep.name;

SELECT em.first_name,em.last_name,dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
ORDER BY dep.name,em.last_name;

SELECT COUNT(em.first_name),dep.name
FROM employees em 
INNER JOIN departments dep 
ON em.id_dep=dep.id
GROUP BY dep.name
LIMIT 3;


---------
--DÍA 3
---------
--Práctica 1
INSERT INTO departments(name) VALUES
('IA');

SELECT *
FROM departments;

SELECT *
FROM employees;

INSERT INTO employees(birth_date,first_name,last_name,salary,title,title_date,id_dep)
VALUES ('2003-02-21','Ana','Martínez',500,'IA Engineer','2024-06-01','3')

SELECT *
FROM employees;

SELECT employees.first_name,employees.last_name,departments.name 
FROM employees 
INNER JOIN departments ON employees.id_dep=departments.id;

--EXTRA
SELECT employees.*,departments.name
FROM employees 
LEFT JOIN departments ON employees.id_dep=departments.id;