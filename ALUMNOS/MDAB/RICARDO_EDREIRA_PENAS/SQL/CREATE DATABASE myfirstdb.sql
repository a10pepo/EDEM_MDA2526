CREATE DATABASE myfirstdb;

CREATE TABLE IF NOT EXISTS employees (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
birth_date DATE NOT NULL,
first_name VARCHAR(20) NOT NULL,
last_name VARCHAR(20) NOT NULL,
register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
);
DROP TABLE IF EXISTS employees;
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, title, register_date, salary, title_date)
VALUES('1990-05-10', 'Carlos', 'Gómez', 'Analista de Datos', '2020-05-03', 22000, '2020-03-15'),
('1994-08-21', 'Lucía', 'Pérez', 'Desarrolladora Web', '2021-06-12', 28000, '2021-05-10'),
('1988-03-03', 'María', 'López', 'Gestora de Proyectos', '2020-07-18', 35000, '2020-07-22'),
('1992-11-15', 'María', 'Martínez', 'Bibliotecaria', '2020-03-09', 18000, '2020-02-01'),
('1995-06-27', 'María', 'Sánchez', 'Documentalista', '2020-11-01', 26000, '2020-11-10'),
('1989-01-09', 'José', 'Ramírez', 'Técnico de Archivo', '2021-09-03', 15000, '2021-09-03'),
('1987-07-30', 'Ricardo', 'Díaz', 'Administrador de Sistemas', '2019-06-12', 42000, '2019-06-12'),
('1996-10-25', 'Laura', 'Navarro', 'Especialista SEO', '2022-04-21', 33000, '2022-04-21'),
('1993-09-14', 'Andrés', 'Torres', 'Desarrollador Frontend', '2021-08-14', 29000, '2021-08-14'),
('1998-02-19', 'Sara', 'Moreno', 'Gestora Documental', '2023-02-18', 25000, '2023-02-18'),
('1985-04-11', 'Javier', 'Luna', 'Analista Financiero', '2020-05-09', 37000, '2020-05-09'),
('1991-12-03', 'Carmen', 'Vidal', 'Marketing Manager', '2023-09-30', 48000, '2023-09-30'),
('1986-06-06', 'Luis', 'Castro', 'Técnico en Bases de Datos', '2020-10-10', 31000, '2020-10-10'),
('1997-03-29', 'Clara', 'Ríos', 'Consultora de IA', '2022-11-11', 50000, '2022-11-11'),
('1999-07-02', 'David', 'Ortega', 'Community Manager', '2021-01-05', 12000, '2021-01-05');


SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary >=20000;
SELECT * FROM employees WHERE salary <=100000;

UPDATE employees SET date = 16 WHERE id = 2;
SELECT * FROM employees WHERE ID = 2;

SELECT * FROM employees ORDER BY id DESC;
SELECT * FROM employees WHERE birth_date BETWEEN '1990-01-01' AND '1995-12-31';

--practica 1
UPDATE employees SET first_name= 'Juan' WHERE id = 7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary < 20000;
SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date ASC;
--practica 2
SELECT first_name || ' ' || last_name AS name FROM employees;
--practica 3
SELECT DISTINCT birth_date FROM employees;
--practica 4
SELECT * FROM employees WHERE first_name LIKE '%a%';
--practica 5
SELECT * FROM employees WHERE first_name LIKE 'M%';
SELECT * FROM employees WHERE first_name NOT LIKE '%r%';

--practica 6

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;
--Like y not Like
SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

--Agregar funciones de agregación
SELECT birth_date, COUNT(birth_date) FROM employees GROUP BY birth_date;

--Practica :(
SELECT COUNT(*) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) FROM employees GROUP BY title;
SELECT title, MIN(salary), MAX(salary) FROM employees GROUP BY title;

--Calcular valores con columnas numéricas:
SELECT first_name, salary, 
ROUND(salary * 0.12,1) AS ahorro_mensual 
FROM employees;

ALTER TABLE employees ADD COLUMN department VARCHAR(50);

--Practicar-
SELECT first_name, salary,
salary * 0.12 AS ahorro_mensual
ROUND((salary * 0.12)*3,2) AS ahorro_mensual_trimestral
FROM employees;

--Escribe una consulta SQL que, a partir de la tabla employees, calcule el importe de impuestos aplicando un 21 % sobre el salario bruto y obtenga el salario neto (bruto − impuestos), mostrando los resultados con 2 decimales y usando alias (AS) claros.
--Seleccionar el nombre del empleado (first_name) y su salary.
--Calcular la columna impuestos como el 21 % del salario (salary * 0.21) y redondearla a 2 decimales.
--Calcular la columna salario_neto como salary - impuestos, también redondeada a 2 decimales.
--Usar alias (AS) exactamente con los nombres: impuestos y salario_neto

SELECT 
    first_name,
    salary,
    ROUND(salary * 0.21, 2) AS impuestos,
    ROUND(salary - (salary * 0.21), 2) AS salario_neto
FROM employees;
