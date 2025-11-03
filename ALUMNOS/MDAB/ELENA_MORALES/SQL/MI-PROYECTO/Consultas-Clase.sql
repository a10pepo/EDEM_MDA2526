CREATE DATABASE myFirstDB;

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;
ALTER TABLE employees ADD COLUMN register_date TIMESTAMPTZ NOT NULL DEFAULT now();

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
VALUES ('Carlos', 'Gomez', '1988-02-15', 12000, 'Analyst', '2020-03-12'),
('Carlos', 'Perez', '1990-07-22', 15000, 'Developer', '2020-07-25'),
('Carlos', 'Lopez', '1985-11-05', 18000, 'Manager', '2020-10-10'), -- 3 Carlos
('Ana', 'Martinez', '1995-04-10', 5200, 'Assistant', '2019-04-10'),
('Luis', 'Sanchez', '1989-01-05', 8000, 'Analyst', '2020-01-05'), -- año 2020
('Lucia', 'Diaz', '1984-09-22', 46000, 'Senior Developer', '2018-09-22'),
('Marta', 'Ruiz', '1992-06-14', 25000, 'HR Coordinator', '2020-06-14'), -- año 2020
('David', 'Torres', '1987-11-18', 34000, 'Team Lead', '2021-11-18'),
('Sofia', 'Ramirez', '1994-03-02', 27000, 'Accountant', '2017-03-02'),
('Jorge', 'Serrano', '1996-12-31', 5000, 'Assistant', '2020-12-31'), -- año 2020
('Elena', 'Cruz', '1983-02-20', 38000, 'Project Manager', '2020-02-20'), -- año 2020
('Ruben', 'Castillo', '1981-05-22', 49000, 'Architect', '2022-05-22'),
('Paula', 'Navas', '1997-08-11', 15000, 'Developer', '2016-08-11'),
('Hector', 'Vega', '1991-04-30', 22000, 'Designer', '2023-04-30'),
('Natalia', 'Flores', '1993-09-09', 30000, 'QA Engineer', '2020-09-09'); -- año 2020


SELECT * FROM employees;
SELECT first_name, salary FROM employees;
SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Marta' WHERE id = 7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS name FROM employees WHERE id = 10;
SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT title, AVG(salary) FROM employees GROUP BY title;
SELECT title, MAX(salary),MIN(salary) FROM employees GROUP BY title;

SELECT first_name, salary,
    salary * 0.12 AS ahorro_mensual,
    ROUND((salary * 0.12) * 3, 2) AS total_ahorrado_aproximado
FROM employees;

-- EXTRA
SELECT first_name, salary,
    salary * 0.21 AS impuestos,
    ROUND((salary * 0.21), 2) AS total_impuestos,
    ROUND(salary - (salary * 0.21), 2) AS salario_neto
FROM employees;


