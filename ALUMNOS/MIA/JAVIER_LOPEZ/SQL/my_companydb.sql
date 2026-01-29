CREATE DATABASE IF NOT EXISTS my_company_database


CREATE TABLE IF NOT EXISTS users (

id                     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name             VARCHAR(100) NOT NULL,
last_name              VARCHAR(100) NOT NULL,
email                  VARCHAR(255) UNIQUE NOT NULL,
password          TEXT NOT NULL,
register_date     TIMESTAMP NOT NULL DEFAULT now()

);

CREATE TABLE IF NOT EXISTS employees (

id                     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
birth_date             DATE NOT NULL,
first_name              VARCHAR(100) NOT NULL,
last_name                  VARCHAR(100) NOT NULL

);


ALTER TABLE employees ADD COLUMN IF NOT EXISTS salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title VARCHAR(100);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title_date DATE;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
VALUES
('Javi', 'Lopez', '2002-04-12', 1000, 'senior developer', '2015-04-24'),
('Paco', 'Martinez', '2002-04-15', 900, 'junior developer', '2020-05-24'),
('manolo', 'gimenez', '2002-04-15', 30000, 'ceo', '2020-05-24'),
('Lucía', 'Fernández', '1990-03-10', 1200, 'project manager', '2018-07-01'),
('Carlos', 'Torres', '1985-11-25', 950, 'data analyst', '2019-10-15'),
('Ana', 'Ruiz', '1992-08-30', 1100, 'UX designer', '2021-03-12'),
('Miguel', 'Sánchez', '1988-01-20', 850, 'QA tester', '2020-11-20'),
('Laura', 'García', '1995-06-14', 1050, 'frontend developer', '2022-06-01'),
('David', 'López', '1991-02-17', 2000, 'backend developer', '2019-04-20'),
('Marta', 'Romero', '1987-12-05', 1500, 'HR specialist', '2016-09-10'),
('Sergio', 'Navarro', '1993-09-22', 1300, 'IT support', '2017-01-05'),
('Clara', 'Martínez', '1996-05-18', 1800, 'marketing lead', '2020-02-27'),
('Raúl', 'Jiménez', '1990-07-07', 2200, 'DevOps engineer', '2018-08-13');



SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET first_name='Perico' WHERE id = 2;

DELETE FROM employees WHERE id=5;
DELETE FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;

SELECT  * FROM employees WHERE first_name LIKE 'P%';
SELECT  * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT AVG(salary) FROM employees GROUP BY title;
SELECT MAX(salary), MIN(salary) FROM employees GROUP BY title;


SELECT first_name, salary,
    ROUND(salary,2) AS salario_redondeado
FROM employees;

SELECT current_database();


CREATE TABLE IF NOT EXISTS departments (


id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,    


);
ALTER TABLE departments ADD COLUMN nombre VARCHAR(100) NOT NULL

ALTER TABLE employees ADD COLUMN department_id INT;
ALTER TABLE employees ADD CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id);
INSERT INTO departments (nombre) VALUES ('Engineering'), ('Marketing');

SELECT * FROM departments;
SELECT * FROM employees;

UPDATE employees SET department_id = 1 WHERE id = 1;
UPDATE employees SET department_id = 1 WHERE id = 2;
UPDATE employees SET department_id = 2 WHERE id = 3;

INSERT INTO departments (nombre)
VALUES ('Sales');

SELECT * FROM departments;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, department_id)
VALUES ('1998-10-20', 'Maria', 'Gomez', 1100.00, 'junior engineer', '2023-01-10', 1);

SELECT * FROM employees;

SELECT 
    e.*, 
    d.nombre AS nombre_departamento
FROM 
    employees e
LEFT JOIN 
    departments d ON e.department_id = d.id;


-- EJERCICIO OPCIONAL
CREATE DATABASE university_db;

CREATE TABLE students(
id           INTEGER PRIMARY KEY,
first_name   VARCHAR(100),
last_name    VARCHAR(100),
enrollment_da  TIMESTAMP,
grade         NUMERIC(4,2)

)

ALTER TABLE students ADD COLUMN city VARCHAR(100);


ALTER TABLE students ALTER COLUMN grade TYPE INTEGER;