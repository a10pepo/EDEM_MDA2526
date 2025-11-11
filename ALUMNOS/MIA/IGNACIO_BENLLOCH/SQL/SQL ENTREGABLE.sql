--CREATE TABLE IF NOT EXISTS users (
--id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--first_name   VARCHAR(100) NOT NULL,
--last_name    VARCHAR(100) NOT NULL,
--email      VARCHAR(255) UNIQUE NOT NULL,
--password  TEXT NOT NULL,        
--register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
--);

--CREATE TABLE IF NOT EXISTS employees (
--id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--birth_date   DATE,
--first_name  VARCHAR(100) NOT NULL,
--last_name VARCHAR(100)  NOT NULL
--);
--ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
--ALTER TABLE employees ADD COLUMN title VARCHAR (100);
--ALTER TABLE employees ADD COLUMN title_date DATE;

/*
INSERT INTO employees(birth_date, first_name, last_name, salary, title, title_date)
VALUES ('2002-07-01', 'Ignacio', 'Benlloch', '49999', 'Recursos Humanos', '2020-08-09'),
('1998-03-12', 'Laura', 'Martínez', 25000, 'Analista de Datos', '2020-05-14'),
('1995-11-02', 'Laura', 'Gómez', 27000, 'Administrativa', '2020-09-22'),
('1999-07-23', 'Laura', 'Ruiz', 31000, 'Coordinadora de Ventas', '2021-01-10'),
('1988-05-11', 'Carlos', 'Sánchez', 42000, 'Jefe de Producción', '2020-03-18'),
('1990-02-27', 'Marta', 'López', 19000, 'Diseñadora Gráfica', '2020-12-01'),
('1997-09-15', 'Javier', 'Pérez', 15500, 'Asistente de Marketing', '2021-04-07'),
('1985-01-09', 'Lucía', 'Fernández', 50000, 'Directora Financiera', '2019-11-25'),
('1993-08-30', 'Andrés', 'Torres', 37500, 'Supervisor de Logística', '2022-06-14'),
('1991-12-22', 'Beatriz', 'Navarro', 22000, 'Recepcionista', '2023-02-01'),
('1994-04-19', 'Diego', 'Muñoz', 48000, 'Gerente de Operaciones', '2020-07-20'),
('2000-06-04', 'Sofía', 'Castillo', 14500, 'Atención al Cliente', '2021-09-10'),
('1989-10-10', 'Pablo', 'Herrera', 33000, 'Especialista en Calidad', '2020-10-05'),
('1996-01-28', 'Elena', 'Domínguez', 29500, 'Técnica de Recursos Humanos', '2023-05-11'),
('1992-03-03', 'Mario', 'Gil', 18500, 'Auxiliar Contable', '2022-11-30');
*/
/*
SELECT * FROM employees;
SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;



SELECT * FROM employees;
TRUNCATE employees ;

UPDATE employees *
SET first_name  = 'Lorena' 
WHERE id = 7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;
SELECT * FROM employees;
*/
/*
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT * FROM employees WHERE salary BETWEEN 14000 and 50000;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees;
SELECT DISTINCT age FROM users;


SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees


SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE last_name LIKE '%a%';
*/
--TRUNCATE employees ;
/*
SELECT COUNT(title) FROM employees;
SELECT MAX(salary) FROM employees;
*/


-- Muestra el first_name y salary de cada empleado redondeando a 2 decimales
/*
SELECT first_name, ROUND(salary,2)
FROM employees;
*/

-- CREATE TABLE posts (
--    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--    user_id INTEGER NOT NULL REFERENCES users(id),
--    title VARCHAR(100) NOT NULL,
--   body TEXT,               
--   publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()     
-- );
/*
INSERT INTO posts(user_id, title, body) VALUES (1, 'Post One', 'This is post one'),
(3, 'Post Two', 'This is post two'),
(1, 'Post Three', 'This is post three'),
(6, 'Post Four', 'This is post four'), 
(1, 'Post Five', 'This is post five'),
(7, 'Post Six', 'This is post six'),
(1, 'Post Seven', 'This is post seven'),
(3, 'Post Eight', 'This is post eight');
*/
/*
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    title VARCHAR
);

INSERT INTO departments ("id", "title") 
VALUES(2, 'engineering'),
(4, 'engineering'),
(6, 'marketing');
*/
-- ALTER TABLE employees ADD COLUMN departments VARCHAR;
/*
UPDATE employees
set title = 'engineering' WHERE id = 183;  
UPDATE employees
set title = 'engineering' WHERE id = 185;
UPDATE employees
set title = 'marketing' WHERE id = 186;    

SELECT *
FROM employees
INNER JOIN departments
ON employees.title = departments.title;
*/
-- select * from employees;

-- select * from departments



