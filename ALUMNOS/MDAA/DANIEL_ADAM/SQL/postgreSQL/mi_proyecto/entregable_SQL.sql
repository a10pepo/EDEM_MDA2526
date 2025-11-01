--CREATE DATABASE my_first_db;

CREATE TABLE IF NOT EXISTS users (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password TEXT NOT NULL,
register_date TIMESTAMPTZ NOT NULL DEFAULT now()  
);

-- DROP TABLE users

-- Modificar la tabla (no los datos)

ALTER TABLE users ADD COLUMN age VARCHAR(3);

ALTER TABLE users ALTER COLUMN age TYPE INTEGER USING age::integer;

ALTER TABLE users DROP COLUMN age;

-- Nuevo Ejercicio

CREATE TABLE IF NOT EXISTS employees (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
birth_date DATE NOT NULL,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;


INSERT INTO users (first_name, last_name, email, password, age)
VALUES ('Ada', 'Lovelace', 'ada@example.com', '123456', 36);

INSERT INTO users (first_name, last_name, email, password,age) 
VALUES ('Luffy', 'Monkey D.', 'luffy@mugiwara.com', '123456',17), 
('Zoro', 'Roronoa', 'zoro@mugiwara.com', '123456',21),
('Sanji', 'Vinsmoke', 'sanji@mugiwara.com', '123456',22);

-- Añadir 15 employees

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) 
VALUES ('1989-05-12', 'Carlos', 'Gómez', 32000, 'Senior Developer', '2020-03-12'),
('1993-08-22', 'Ana', 'Martínez', 27000, 'Marketing Manager', '2021-07-20'),
('1980-11-30', 'Carlos', 'Pérez', 45000, 'IT Manager', '2019-11-05'),
('1995-03-14', 'Laura', 'Sánchez', 5000, 'UI/UX Designer', '2020-01-15'),
('1984-06-07', 'Carlos', 'Ramírez', 38000, 'Product Owner', '2022-06-10'),
('1990-09-18', 'Diego', 'Fernández', 15000, 'QA Engineer', '2020-08-19'),
('1996-12-01', 'Lucía', 'García', 12000, 'Data Analyst', '2020-09-23'),
('1982-04-25', 'Marta', 'López', 50000, 'CTO', '2018-04-17'),
('1994-10-19', 'Jorge', 'Mendoza', 22000, 'Frontend Developer', '2021-11-12'),
('1991-02-02', 'Elena', 'Díaz', 27000, 'Backend Developer', '2020-06-05'),
('1987-07-09', 'Luis', 'Vargas', 34000, 'DevOps Engineer', '2023-01-01'),
('1992-11-11', 'Sandra', 'Ruiz', 18000, 'Scrum Master', '2022-12-03'),
('1979-03-20', 'Ricardo', 'Torres', 47000, 'Security Analyst', '2020-02-29'),
('1986-01-15', 'María', 'Ortega', 25000, 'Technical Writer', '2017-09-08'),
('1993-05-05', 'José', 'Navarro', 29500, 'Systems Administrator', '2021-10-20');

-- Consultar 

SELECT * FROM employees

SELECT first_name, salary FROM employees

-- WHERE (Filtrar)

SELECT * FROM users
WHERE age = 19;

SELECT * FROM employees
WHERE id = 2;

SELECT * FROM employees
WHERE salary > 20000;

SELECT * FROM employees
WHERE salary <= 10000;

-- UPDATE

UPDATE users SET age = 19 WHERE id = 2; -- NO se puede cambiar el orden

DELETE FROM users WHERE id = 3;

UPDATE employees SET first_name = 'Fernando' WHERE id = 7;

-- PRÁCTICA

DELETE FROM employees WHERE id = 5;

DELETE FROM employees WHERE salary > 20000;

-- ORDER BY & BETWEEN

SELECT * FROM users ORDER BY id DESC;

SELECT * FROM users ORDER BY id ASC;

SELECT * FROM users WHERE age BETWEEN 20 AND 25;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

-- CONCATENAR

SELECT first_name || ' ' || last_name AS nombre_completo FROM users;

SELECT DISTINCT age FROM users;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

-- LIKE and NOT LIKE

SELECT * FROM users WHERE last_name LIKE '%a%'; -- Contenga la a
SELECT * FROM users WHERE last_name LIKE 'D%';
SELECT * FROM users WHERE last_name NOT LIKE '%r%';

-- Práctica
SELECT * FROM employees WHERE first_name LIKE 'M%';

SELECT * FROM employees WHERE first_name LIKE '%a%';

-- Funciones con SELECT

SELECT COUNT(id) FROM users;

SELECT ROUND(AVG(age)) FROM users;

SELECT age, COUNT(age) FROM users GROUP BY age;


-- Práctica 

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) FROM employees GROUP BY title;


SELECT first_name, age, age + 5 as age_in_five_years FROM users;


-- Añadimos salary a Users
ALTER TABLE users ADD COLUMN salary NUMERIC(10,2);

UPDATE users
SET salary = CASE id
 WHEN 7 THEN 1234.10
 WHEN 8 THEN 1500.50
 WHEN 11 THEN 900.00
 ELSE 1100.75
END;

SELECT first_name, salary, salary * 0.12 AS ahorro_mensual, ROUND((salary*0.12)*3, 2) AS total_ahorro_aproximado FROM employees;

-- Práctica
SELECT first_name, ROUND((salary),2) FROM employees;

-- FIN DEL ENTREGABLE

-- EJERCICIO EXTRA DISPONIBLE

SELECT first_name, salary, round(salary*0.21,2) AS impuestos, ROUND(salary *0.79,2) as salario_neto
FROM employees;  


-- CLASE 2 ------------------------------------------------------------------------------------------------------

CREATE TABLE posts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    body TEXT,                                     
    publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()            
);

INSERT INTO posts(user_id, title, body) VALUES (1, 'Post One', 'This is post one'),
(3, 'Post Two', 'This is post two'),
(1, 'Post Three', 'This is post three'),
(2, 'Post Four', 'This is post four'),
(1, 'Post Five', 'This is post five'),
(2, 'Post Six', 'This is post six'),
(1, 'Post Seven', 'This is post seven'),
(3, 'Post Eight', 'This is post eight');


--Inner Join

SELECT *
FROM users
INNER JOIN posts
ON users.id = posts.user_id;

SELECT users.first_name, posts.body
FROM users
INNER JOIN posts -- Con INNER me muestra solos los matches, los que tienen publicación
ON users.id = posts.user_id;

SELECT users.first_name, posts.body
FROM users
LEFT JOIN posts --Con LEFT me muestra todos los usuarios de la tabla users tengan o no publicación
ON users.id = posts.user_id;

-- Añadimos ahora los comments (ya teniamos users y posts)

CREATE TABLE comments (
  id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  post_id  INTEGER NOT NULL REFERENCES posts(id),
  user_id  INTEGER NOT NULL REFERENCES users(id),
  body    TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO comments(post_id, user_id, body) VALUES
(1, 3, 'This is comment one'),
(2, 1, 'This is comment two'),
(5, 3, 'This is comment three'),
(2, 2, 'This is comment four'),
(1, 2, 'This is comment five');

-- EJEMPLO

SELECT
comments.body,
posts.title,
users.first_name,
users.last_name
FROM comments
INNER JOIN posts ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id;

-- PRACTICA

CREATE TABLE departments (
  id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name  VARCHAR
);

ALTER TABLE employees ADD COLUMN department_id INTEGER REFERENCES departments(id);


INSERT INTO departments (name) VALUES
('Engineering'), 
('Marketing');

UPDATE employees
SET department_id = CASE id
 WHEN 2 THEN 1
 WHEN 3 THEN 1
 WHEN 4 THEN 2
END;


SELECT first_name || ' ' || last_name as NOMBRE, departments.name
FROM employees
LEFT JOIN departments ON departments.id = employees.department_id;

-- CLASE 3 (REPASO) -------------------------------------------------------------------------------------------
-- DBDIAGRAM

SELECT * FROM employees;

-- Nueva base de datos
CREATE DATABASE repasoDB;

CREATE TABLE IF NOT EXISTS users (
   id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   first_name VARCHAR(100) NOT NULL,
   last_name VARCHAR(100) NOT NULL,
   email VARCHAR(255) UNIQUE NOT NULL,
   password TEXT NOT NULL,                    
   register_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO users (first_name, last_name, email, password)
VALUES ('Ada','Lovelace','ada@example.com','123456');

CREATE TABLE posts (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  title VARCHAR(100) NOT NULL,
  body TEXT,               
  publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()     
);

SELECT * FROM users;

SELECT * FROM posts;

INSERT INTO posts (user_id, title, body)
VALUES (1, 'Post One', 'This is post one')

SELECT posts.title, users.first_name || ' ' || users.last_name
FROM posts
RIGHT JOIN users
ON posts.user_id = users.id;


INSERT INTO users (first_name, last_name, email, password)
VALUES ('Ada2','Lovelace2','ada2@example.com','123456');

CREATE TABLE comments (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  post_id INTEGER NOT NULL REFERENCES posts(id),
  user_id INTEGER NOT NULL REFERENCES users(id),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO comments(post_id, user_id, body) 
VALUES (1, 1, 'This is comment one');

SELECT posts.title, users.first_name
FROM posts
INNER JOIN users ON posts.user_id = users.id;

SELECT comments.body AS comentario,
posts.title AS titulo_publicacion 
FROM comments
LEFT JOIN posts
ON posts.id = comments.post_id;

-- Cambio a DB my_first_db

SELECT * FROM employees


SELECT * FROM departments

INSERT INTO departments (name) VALUES ('Accounting');

DELETE FROM departments 
WHERE name ='accounting';

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, department_id)
VALUES ('1985-04-12', 'María', 'González', 32000, 'Contable', '2022-06-01', 4);

SELECT employees.first_name || ' ' || employees.last_name as nombre, departments.name
FROM employees
LEFT JOIN departments
ON departments.id = employees.department_id;


