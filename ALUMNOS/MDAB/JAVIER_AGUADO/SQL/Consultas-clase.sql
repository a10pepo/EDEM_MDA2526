CREATE DATABASE myFirstDB;
CREATE TABLE IF NOT EXISTS employees (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date   VARCHAR(100) NOT NULL,
    first_name   VARCHAR(100) NOT NULL,
    last_name      VARCHAR(255) UNIQUE NOT NULL     
);
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES ('2025/05/28', 'Javier', 'Aguado', 'data engineer', '2000/01/01');

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES 
('1990/03/15', 'Marina', 'López', 72000, 'data analyst', '2018/06/01'),
('1988/07/22', 'Carlos', 'Ruiz', 95000, 'senior data engineer', '2015/09/10'),
('1995/12/05', 'Lucía', 'Gómez', 68000, 'data scientist', '2020/03/01'),
('1982/11/18', 'Andrés', 'Martínez', 102000, 'project manager', '2013/01/15'),
('1993/09/09', 'Sofía', 'Fernández', 75000, 'data engineer', '2019/02/20'),
('1997/04/11', 'David', 'Castro', 64000, 'junior data analyst', '2022/07/01'),
('1989/10/30', 'Laura', 'Navarro', 88000, 'data architect', '2016/05/12'),
('1991/01/27', 'Pablo', 'Ortega', 79000, 'data engineer', '2018/09/01'),
('1994/06/08', 'Marta', 'Sánchez', 71000, 'data scientist', '2021/01/01'),
('1985/02/19', 'Héctor', 'Jiménez', 93000, 'senior data analyst', '2014/11/10'),
('1992/08/23', 'Elena', 'Morales', 78000, 'data engineer', '2019/04/03'),
('1990/10/05', 'Raúl', 'Pérez', 97000, 'machine learning engineer', '2017/08/14'),
('1996/07/13', 'Nerea', 'Domínguez', 66000, 'data analyst', '2021/10/01'),
('1987/12/01', 'Adrián', 'Torres', 99000, 'data manager', '2016/12/12');

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

SELECT * FROM employees;

UPDATE employees SET first_name = 'Elisa' WHERE id = 7;
DELETE FROM employees WHERE id = 5;
SELECT * FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES 
('1998/03/12', 'Alba', 'Martín', 5000, 'intern data assistant', '2024/01/15'),
('1996/07/28', 'Luis', 'Carrillo', 12000, 'junior data analyst', '2023/09/01'),
('1993/02/10', 'Clara', 'Romero', 18000, 'data assistant', '2022/06/12'),
('1989/09/21', 'Andrés', 'Moreno', 26000, 'data technician', '2020/11/05'),
('1991/11/04', 'Patricia', 'Navas', 33000, 'data analyst', '2021/08/09'),
('1997/12/16', 'Mario', 'Rojas', 41000, 'data engineer', '2020/04/01'),
('1985/05/19', 'Lucía', 'Crespo', 49000, 'data scientist', '2018/02/14'),
('1994/06/07', 'Julián', 'Serrano', 56000, 'data engineer', '2019/09/10'),
('1992/01/25', 'Sofía', 'Prieto', 63000, 'data analyst', '2019/03/18'),
('1988/08/13', 'Raúl', 'Castillo', 71000, 'data architect', '2017/12/01'),
('1990/03/09', 'Nerea', 'Campos', 79000, 'data scientist', '2016/06/22'),
('1987/04/17', 'Víctor', 'Rey', 85000, 'project manager', '2015/10/01'),
('1995/10/30', 'Isabel', 'Garrido', 91000, 'senior data engineer', '2014/05/11'),
('1986/12/02', 'Hugo', 'Domínguez', 97000, 'data architect', '2013/02/27'),
('1984/09/29', 'Carmen', 'Santos', 100000, 'head of data', '2010/01/01');

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT * FROM employees;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS name FROM employees WHERE id = 17;
SELECT * FROM employees WHERE first_name LIKE 'N%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT title, AVG(salary) FROM employees GROUP BY title;
SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, ROUND(salary,2) AS salary_rounded FROM employees;

-- SQL II

CREATE TABLE IF NOT EXISTS departments (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO departments (name)
VALUES ('Engineering'),
('Marketing');

SELECT * FROM departments;

ALTER TABLE employees ADD COLUMN departments_id INT REFERENCES departments(id);

UPDATE employees SET departments_id = 1 WHERE id = 25;
UPDATE employees SET departments_id = 1 WHERE id = 2;
UPDATE employees SET departments_id = 2 WHERE id = 3;

SELECT * FROM employees;

UPDATE employees SET departments_id = 2 WHERE id in (16,17,18);

SELECT * FROM employees;


-- DIFERENCIAS ENTRE INNER JOIN y LEFT JOIN
-- INNER se utiliza cuando quiero solo los que coincidan la condición del ON
-- LEFT se utiliza cuando quiero toda la tabla de origen de la consulta

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.
SELECT employees.first_name, employees.last_name, departments.name
FROM employees 
INNER JOIN departments
ON departments.id = employees.departments_id;

-- EXTRA: Muestra todos los empleados con sus departamentos independientemente de si tienen departamento o no
SELECT employees.first_name, employees.last_name, departments.name
FROM employees 
LEFT JOIN departments
ON departments.id = employees.departments_id;



-- RELACIONES PARTE 2
-- Crear tabla users
CREATE TABLE IF NOT EXISTS users (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password        TEXT NOT NULL,                         
    register_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);
INSERT INTO users (first_name, last_name, email, password)
    VALUES ('Ada','Lovelace','ada@example.com','123456')
    VALUES ('Javier','Lovelace','javier@example.com','123456');

-- Crear tabla posts
CREATE TABLE posts (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    title           VARCHAR(100) NOT NULL,
    body            TEXT,                              
    publish_date    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO posts(user_id, title, body) 
    VALUES (1, 'Post One', 'This is post one');
    
-- Crear tabla comments
CREATE TABLE comments (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    post_id     INTEGER NOT NULL REFERENCES posts(id),
    user_id     INTEGER NOT NULL REFERENCES users(id),
    body        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
INSERT INTO comments(post_id, user_id, body) 
    VALUES(1, 1, 'This is comment one')
    VALUES(1, 1, 'This is comment two')
    VALUES(1, 2, 'Me gusta!');

-- La idea aquí es obtener todos los comentarios 
-- con el título de la publicación en la que se encuentra ese comentario 
-- y también estamos obteniendo la persona que dejó el comentario.
SELECT comments.body, comments.created_at, posts.title, users.first_name
FROM comments
INNER JOIN posts
ON posts.id = comments.post_id
INNER JOIN users
ON users.id = comments.user_id;

-- EXTRA
--- Inserta departamentos. Inserta al menos 6 departamentos con estos nombres (idénticos):
-- Engineering
-- Marketing
-- Sales
-- HR
-- R&D
-- Legal	

INSERT INTO departments (name)
VALUES  ('Sales'),
        ('HR'),
        ('R&D'),
        ('Legal');
SELECT * FROM departments;


-- Inserta empleados (mínimo 12). Con los siguientes requisitos:
-- Distribución por departamento:
-- Engineering: 4 empleados
-- Marketing: 3 empleados
-- Sales: 2 empleados
-- HR: 1 empleado
-- Sin departamento (department_id = NULL): 2 empleados(para diferenciar INNER JOIN vs LEFT JOIN)
UPDATE employees SET departments_id = 2 WHERE id = 19;
UPDATE employees SET departments_id = 1 WHERE id = 20;
UPDATE employees SET departments_id = 1 WHERE id = 21;
UPDATE employees SET departments_id = 1 WHERE id = 22;
UPDATE employees SET departments_id = 3 WHERE id = 23;
UPDATE employees SET departments_id = 3 WHERE id = 24;
UPDATE employees SET departments_id = 4 WHERE id = 25;

-- Lista solo empleados que tienen departamento (INNER JOIN).
SELECT * 
FROM employees
INNER JOIN departments
ON employees.departments_id = departments.id;

-- Muestra departamentos sin empleados (LEFT JOIN + IS NULL).
SELECT departments.name AS nombre_departamento
FROM departments
LEFT JOIN employees
ON employees.departments_id = departments.id 
WHERE employees.departments_id IS NULL;

-- Cuenta cuántos empleados hay por departamento (nombre y COUNT).
SELECT departments.name, COUNT(*)
FROM departments
LEFT JOIN employees
ON employees.departments_id = departments.id
GROUP BY departments.name;

-- Empleados del departamento ‘Engineering’ (por nombre de dept).
SELECT *
FROM employees
INNER JOIN departments
ON employees.departments_id = departments.id
WHERE departments.name LIKE 'Engineering';

-- Salario medio por departamento (nombre y AVG(salary)).
SELECT departments.name, AVG(employees.salary)
FROM departments
LEFT JOIN employees
ON employees.departments_id = departments.id
GROUP BY departments.id;

-- Salario máximo por departamento y qué departamento lo tiene.
SELECT departments.name, MAX(employees.salary)
FROM departments
LEFT JOIN employees
ON employees.departments_id = departments.id
GROUP BY departments.id;

-- Número de títulos distintos por departamento.
SELECT departments.name, COUNT(DISTINCT employees.title)
FROM departments
LEFT JOIN employees
ON employees.departments_id = departments.id
GROUP BY departments.id;

-- Empleados con su departamento, ordenado por department.name y last_name.
SELECT departments.name, employees.last_name, employees.first_name
FROM employees
LEFT JOIN departments
ON employees.departments_id = departments.id
ORDER BY departments.name, employees.last_name;

-- Top 3 departamentos con más empleados.

