CREATE TABLE IF NOT EXISTS employees (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE NOT NULL,
    first_name  VARCHAR(100) NOT NULL,
    last_lame   VARCHAR(110) NOT NULL
);


ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

SELECT * FROM employees;

INSERT INTO employees (birth_date, first_name, last_lame, salary, title, title_date)
VALUES 
('1999-10-21', 'Morata', 'Sanchez', 30500.75, 'Ingeniero Industrial', '2020-03-15'),
('1999-10-21', 'Morata', 'Sanchez', 27800.40, 'Licenciado en Administracion', '2020-11-22'),
('1999-10-21', 'Torres', 'Gomez',45000.00, 'Arquitecto Tecnico', '2020-07-09'),
('1999-10-21', 'Torres', 'Gomez', 12000.20, 'Graduado en Derecho', '2020-02-27'),
('1999-10-21', 'Lopez', 'Martinez', 32000.90, 'Ingeniero Informatico', '2023-05-11'),
('1999-10-21', 'Lopez', 'Martinez', 41500.60, 'Economista', '2022-10-30'),
('1999-10-21', 'Fernandez', 'Ruiz', 22700.80, 'Licenciado en Química', '2021-06-14'),
('1999-10-21', 'Garcia', 'Perez', 37500.00, 'Graduado en Educacion Primaria', '2024-04-09'),
('1999-10-21', 'Navarro', 'Hernandez', 16800.45, 'Arquitecto', '2019-09-25'),
('1999-10-21', 'Diaz', 'Serrano', 25500.33, 'Ingeniero Civil', '2021-01-19'),
('1999-10-21', 'Castro', 'Vega', 48500.10, 'Licenciado en Física', '2018-12-03'),
('1999-10-21', 'Gil', 'Cortes', 16700.70, 'Graduado en Psicología', '2023-03-12'),
('1999-10-21', 'Ramos', 'Flores', 5090.25, 'Tecnico en Mantenimiento', '2022-02-08'),
('1999-10-21', 'Iglesias', 'Cano', 29800.80, 'Graduado en Matemáticas', '2024-08-20');

SELECT * FROM employees;
SELECT *FROM employees WHERE id = 2;

SELECT *
FIRST employees
WHERE salary > 20000;

SELECT *
FROM employees
WHERE salary <= 10000;
SELECT * FROM users WHERE id = 2;

UPDATE employees SET first_name = 'Carlos' WHERE id = 7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary  >= 20000;
SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name ||' '|| last_lame AS nombre_completo FROM employees;
SELECT * FROM employees WHERE first_name LIKE 'S%';
SELECT * FROM employees WHERE first_name LIKE '%a%';
SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT AVG(salary) FROM employees;
SELECT title,MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, ROUND(salary, 2) FROM employees;

CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);
INSERT INTO departments (name)
VALUES
('engineering'),
('marketing');


SELECT * FROM departments;
DROP TABLE departments;

ALTER TABLE employees ADD COLUMN departments_id INTEGER;
SELECT * FROM employees

UPDATE employees
SET departments_id = (SELECT id FROM departments WHERE name = 'engineering')
WHERE id IN (1,2)

UPDATE employees
SET departments_id = (SELECT id FROM departments WHERE name = 'marketing')
WHERE id IN (1,2)

ALTER TABLE employees ADD COLUMN departments_id INTEGER

CREATE TABLE characters (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    status TEXT,
    species TEXT,
    type TEXT,
    gender TEXT,
    origin_name TEXT,
    location_game TEXT,
    image TEXT,
    url TEXT,
    created TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);
INSERT INTO departments (name)
VALUES
('engineering'),
('marketing');


SELECT * FROM departments;
DROP TABLE departments;

CREATE TABLE IF NOT EXISTS employees (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE NOT NULL,
    first_name  VARCHAR(100) NOT NULL,
    last_lame   VARCHAR(110) NOT NULL
);
DROP DATABASE departments;