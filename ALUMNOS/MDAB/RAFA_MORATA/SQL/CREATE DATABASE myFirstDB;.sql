
CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL
);

    ALTER TABLE employees ADD COLUMN salary NUMERIC(10, 2);
    ALTER TABLE employees ADD COLUMN title VARCHAR;
    ALTER TABLE employees ADD COLUMN  title_date DATE NOT NULL;

    -- las consultas de una en una se separan con ;
    -- SELECT * FROM employees;
    -- SELECT last_name FROM employees;
    -- SELECT * FROM employees WHERE age = 17; trae el que cumpla eso

INSERT INTO employees (birth_date, first_name, last_name, title, salary, title_date)
VALUES
('2000-01-20', 'Carlos', 'Gomez', 'Data-Analyst', 20000, '2020-03-15'),
('2001-01-20', 'Carlos', 'Perez', 'Software-Engineer', 30000, '2020-07-20'),
('2003-01-20', 'Carlos', 'Lopez', 'System-Administrator', 18000, '2021-06-10'),
('2007-01-20', 'Lucia', 'Martinez', 'Project-Manager', 45000, '2020-01-12'),
('2002-01-20', 'Lucia', 'Jimenez', 'UX-Designer', 27000, '2022-02-05'),
('2000-01-20', 'Lucia', 'Ruiz', 'QA-Tester', 22000, '2020-09-19'),
('2000-01-20', 'Javier', 'Santos', 'DevOps-Engineer', 35000, '2019-04-10'),
('2000-01-20', 'Javier', 'Fernandez', 'Database-Admin', 32000, '2020-11-22'),
('2000-01-20', 'Javier', 'Diaz', 'Frontend-Developer', 26000, '2021-05-13'),
('2000-01-20', 'Marta', 'Lopez', 'Backend-Developer', 24000, '2023-03-07'),
('2000-01-20', 'Marta', 'Serrano', 'Data-Scientist', 50000, '2022-08-25'),
('2000-01-20', 'Marta', 'Ortega', 'Security-Analyst', 48000, '2020-12-01'),
('2000-01-20', 'Raul', 'Garcia', 'Technical-Support', 15000, '2021-09-09'),
('2002-01-20', 'Elena', 'Vega', 'Cloud-Architect', 46000, '2020-04-17'),
('2001-01-20', 'Sofia', 'Moreno', 'HR-Specialist', 12000, '2023-01-14');
SELECT * FROM employees;
DROP TABLE employees;
SELECT * FROM employees WHERE id = 2;

SELECT * 
FROM employees
WHERE salary > 20000;

SELECT * 
FROM employees
WHERE salary <= 10000;

UPDATE employees SET first_name = 'RAFA' WHERE id = 7;


DELETE FROM employees WHERE id = 5;

DELETE FROM employees WHERE salary  < 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS name FROM employees;

SELECT *  FROM employees WHERE first_name LIKE 'C%';
SELECT *  FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) FROM employees GROUP BY title;
SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, salary,
ROUND(salary,2)
FROM employees;

SELECT first_name, salary, 
ROUND (salary * 0.21,2) AS impuestos
FROM employees;

SELECT first_name, salary,
ROUND(salary * 0.79,2) AS salario_neto
FROM employees;

SELECT 
    first_name,
    salary,
    ROUND(salary * 0.21, 2) AS impuestos,
    ROUND(salary * 0.79, 2) AS salario_neto
FROM employees;

SELECT DISTINCT birth_date FROM employees;

