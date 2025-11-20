
-- REPASO CLASE 1 (practica_c1_1)


CREATE DATABASE practica_c1_1;

CREATE TABLE IF NOT EXISTS users (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password TEXT NOT NULL, 
register_date TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- elimina: tabla + datos
DROP TABLE users; 

-- elimina: datos
TRUNCATE users;

-- alterando la tabla
ALTER TABLE users ADD COLUMN age VARCHAR(3);
ALTER TABLE users ALTER COLUMN age TYPE INTEGER USING age::integer;
ALTER TABLE users DROP COLUMN age;

-- introducir valores
INSERT INTO users (first_name, last_name, email, password,age)
VALUES ('Ada','Lovelace','ada@example.com','123456',36);

INSERT INTO users (first_name, last_name, email, password,age) 
VALUES ('Luffy', 'Monkey D.', 'luffy@mugiwara.com', '123456',17), 
('Zoro', 'Roronoa', 'zoro@mugiwara.com', '123456',21),
('Sanji', 'Vinsmoke', 'sanji@mugiwara.com', '123456',22);

-- select
SELECT * FROM users;

SELECT first_name, email FROM users;

-- where
SELECT * FROM users WHERE age=22;

-- delete and update
UPDATE users SET age = 19 WHERE id = 2;

DELETE FROM users WHERE id = 3;

-- order by and between
SELECT * FROM users ORDER BY id DESC;
SELECT * FROM users ORDER BY id ASC;
SELECT * FROM users WHERE age BETWEEN 20 AND 25;

-- distinct and concatenate
SELECT first_name || ' ' || last_name AS name FROM users;
SELECT DISTINCT age FROM users;

-- like and not like
SELECT * FROM users WHERE last_name LIKE '%a%';
SELECT * FROM users WHERE first_name LIKE 'S%';
SELECT * FROM users WHERE first_name LIKE '%o';
SELECT * FROM users WHERE last_name NOT LIKE '%r%';

-- funciones select
SELECT COUNT(id) FROM users;
SELECT MAX(age) FROM users;
SELECT MIN(age) FROM users;
SELECT SUM(age) FROM users;
SELECT AVG(age) FROM users;

SELECT age, COUNT(age) FROM users GROUP BY age;

-- mas funciones
SELECT first_name, age, age + 5 AS age_in_5_years
FROM users;

ALTER TABLE users ADD COLUMN salary NUMERIC(10,2);

UPDATE users
SET salary = CASE id
    WHEN 7 THEN 1234.10
    WHEN 8 THEN 1500.50
    WHEN 11 THEN 900.00
    ELSE 1100.75
END;

SELECT first_name, salary,
    salary * 0.12 AS ahorro_mensual
FROM users;

SELECT first_name, salary,
    salary * 0.12 AS ahorro_mensual,
     ROUND((salary * 0.12) * 3, 2) AS total_ahorrado_aproximado
FROM users;

-- CLASE 2 (practica_c1_1)

-- “En una red social un usuario puede crear varias publicaciones. 
-- Las publicaciones tienen comentarios y esos comentarios los 
-- hacen los usuarios.”

CREATE TABLE posts (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    title           VARCHAR(100) NOT NULL,
    body            TEXT,
    publish_date    TIMESTAMPTZ NOT NULL DEFAULT NOW() 
);

INSERT INTO posts(user_id, title, body)
VALUES (1, 'Post One', 'This is post one');

SELECT *
FROM users
INNER JOIN posts ON users.id = posts.user_id;

CREATE TABLE comments (
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
post_id INTEGER NOT NULL REFERENCES posts(id),
user_id INTEGER NOT NULL REFERENCES users(id),
body TEXT NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO comments(post_id, user_id, body) 
VALUES (1, 1, 'This is comment one');

SELECT
comments.body,
posts.title,
users.first_name,
users.last_name
FROM comments
INNER JOIN posts ON posts.id = comments.post_id
INNER JOIN users ON users.id = comments.user_id;

-- REPASO CLASE 1 (practica_c1_2)

CREATE DATABASE practica_c1_2;

CREATE TABLE IF NOT EXISTS employees (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE NOT NULL,  
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(255) NOT NULL
);

ALTER TABLE employees
ADD COLUMN salary NUMERIC(10, 2),
ADD COLUMN title VARCHAR(100),
ADD COLUMN title_date DATE;

INSERT INTO employees 
    (birth_date, first_name, last_name, salary, title, title_date)
VALUES
    ('1990-05-15', 'Ana', 'Torres', 45000.50, 'Project Manager', '2020-01-10'),
    ('1988-02-20', 'Luis', 'Gomez', 48000.00, 'Senior Developer', '2020-03-15'),
    ('1995-11-30', 'Sofia', 'Chen', 32000.75, 'Data Analyst', '2020-06-01'),
    ('1992-07-14', 'Carlos', 'Ruiz', 39000.00, 'Marketing Specialist', '2020-09-20'),
    ('1985-09-05', 'Maria', 'Fernandez', 49500.00, 'HR Manager', '2020-11-05'),
    ('1993-01-25', 'David', 'Garcia', 41000.00, 'Software Engineer', '2021-02-15'),
    ('1991-04-12', 'David', 'Lopez', 42000.00, 'Systems Administrator', '2021-05-10'),
    ('1994-08-19', 'David', 'Kim', 41500.00, 'Software Engineer', '2022-01-30'),
    ('1996-03-08', 'Elena', 'Perez', 36000.00, 'UX/UI Designer', '2021-07-22'),
    ('1987-12-01', 'Javier', 'Martin', 47000.00, 'Senior Developer', '2019-10-01'),
    ('1998-06-22', 'Laura', 'Sanchez', 29000.00, 'Junior Developer', '2023-01-15'),
    ('1990-10-17', 'Miguel', 'Gonzalez', 34000.00, 'Data Analyst', '2022-03-10'),
    ('1989-05-29', 'Lucia', 'Diaz', 33000.00, 'Marketing Specialist', '2021-11-01'),
    ('1997-02-11', 'Pablo', 'Moreno', 31000.00, 'QA Tester', '2022-08-14'),
    ('1993-07-07', 'Carmen', 'Alvarez', 43000.00, 'Product Owner', '2021-04-05'),
    ('1986-04-10', 'Sergio', 'Ramos', 46000.00, 'Project Manager', '2021-03-15'),
    ('1991-08-22', 'Clara', 'Vega', 44500.00, 'Project Manager', '2022-05-20'),
    ('1989-11-11', 'Pedro', 'Ortega', 48500.00, 'Senior Developer', '2021-01-30'),
    ('1996-01-05', 'Isabel', 'Jimenez', 33000.00, 'Data Analyst', '2023-02-01'),
    ('1994-06-30', 'Roberto', 'Navarro', 38500.00, 'Marketing Specialist', '2022-04-10'),
    ('1984-03-18', 'Monica', 'Blanco', 49000.00, 'HR Manager', '2019-12-01'),
    ('1990-09-09', 'Jorge', 'Sanz', 48000.00, 'HR Manager', '2022-07-15'),
    ('1995-12-25', 'Raquel', 'Molina', 41800.00, 'Software Engineer', '2023-01-10'),
    ('1987-10-02', 'Marcos', 'Iglesias', 43000.00, 'Systems Administrator', '2020-08-08'),
    ('1992-02-14', 'Beatriz', 'Santos', 41500.00, 'Systems Administrator', '2022-10-25'),
    ('1997-04-03', 'Daniel', 'Cruz', 37000.00, 'UX/UI Designer', '2022-06-12'),
    ('1993-11-20', 'Natalia', 'Prieto', 36500.00, 'UX/UI Designer', '2021-09-05'),
    ('1999-01-15', 'Oscar', 'Vidal', 29500.00, 'Junior Developer', '2023-03-01'),
    ('2000-07-28', 'Eva', 'Romero', 28800.00, 'Junior Developer', '2023-04-20'),
    ('1994-09-16', 'Hector', 'Gil', 31500.00, 'QA Tester', '2023-01-20'),
    ('1995-08-01', 'Silvia', 'Castillo', 30500.00, 'QA Tester', '2022-11-30'),
    ('1990-06-06', 'Ivan', 'Arias', 44000.00, 'Product Owner', '2022-02-18'),
    ('1992-10-31', 'Sara', 'Flores', 43500.00, 'Product Owner', '2021-12-10');

SELECT * FROM employees;

SELECT id, first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;

SELECT * FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Aisha' WHERE id = 7;

DELETE FROM employees WHERE id= 5;

DELETE FROM employees WHERE salary BETWEEN 30000.00 AND 31000.00;

SELECT first_name, last_name, salary FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT id, birth_date FROM employees ORDER BY birth_date ASC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;

SELECT * FROM employees WHERE first_name LIKE 'L%';

SELECT * FROM employees WHERE first_name LIKE '%L%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT id, first_name, last_name, salary 
FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

SELECT title, AVG(salary) FROM employees GROUP BY title;

SELECT title, MAX(salary), MIN(salary)
FROM employees
GROUP BY title;

SELECT first_name, salary,
ROUND((salary * 0.12), 2) AS ahorro_mensual
FROM employees;

SELECT first_name, salary,
ROUND((salary * 0.21), 2) AS impuestos,
ROUND(salary - (salary * 0.21), 2) AS salario_neto
FROM employees;


-- CLASE 2 (practica_c1_2)
CREATE TABLE departments (
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name TEXT NOT NULL
);

INSERT INTO departments(name) 
VALUES ('Engineering'),
('Marketing');

SELECT *
FROM departments;

ALTER TABLE employees
ADD COLUMN department_id INTEGER REFERENCES departments(id);

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Engineering')
WHERE id=1 OR id=2;

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Marketing')
WHERE id=3;

SELECT *
FROM employees;


SELECT
    employees.first_name,
    employees.last_name,
    departments.name 
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id;

-- de esta forma me sale el id del departamento
SELECT first_name, last_name , title, department_id
FROM employees;

-- de esta forma me sale el nombre del departamento
SELECT
    employees.first_name,
    employees.last_name,
    departments.name 
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id;

INSERT INTO departments(name) 
VALUES ('Sales'),
('R&D'),
('Legal'),
('HR');

SELECT *
FROM departments;


-- añadimos los nuevos datos para los ejercicios extras

TRUNCATE employees;

SELECT * 
FROM employees;

INSERT INTO employees
    (birth_date, first_name, last_name, salary, title, title_date, department_id)
VALUES
    -- 4 Engineering
    ('1998-05-10', 'Elena', 'Vega', 42000.00, 'Backend Engineer', '2023-03-15', (SELECT id FROM departments WHERE name = 'Engineering')),
    ('1996-11-20', 'Marco', 'Silva', 55000.00, 'Frontend Engineer', '2024-01-20', (SELECT id FROM departments WHERE name = 'Engineering')),
    ('1995-02-05', 'Laura', 'Gimenez', 63500.00, 'Data Engineer', '2023-06-01', (SELECT id FROM departments WHERE name = 'Engineering')),
    ('1997-07-30', 'Javier', 'Muñoz', 75000.00, 'DevOps', '2024-05-10', (SELECT id FROM departments WHERE name = 'Engineering')),

    -- 3 Marketing
    ('2000-01-15', 'Sofia', 'Reyes', 33000.00, 'SEO Specialist', '2023-02-10', (SELECT id FROM departments WHERE name = 'Marketing')),
    ('1999-04-25', 'Daniel', 'Ortega', 39500.00, 'Content Manager', '2024-03-01', (SELECT id FROM departments WHERE name = 'Marketing')),
    ('1996-08-12', 'Lucia', 'Campos', 48000.00, 'Brand Manager', '2023-11-15', (SELECT id FROM departments WHERE name = 'Marketing')),
    
    -- 2 Sales
    ('2001-03-03', 'Pablo', 'Molina', 28000.00, 'Sales Rep', '2024-07-20', (SELECT id FROM departments WHERE name = 'Sales')),
    ('1998-10-18', 'Carla', 'Suarez', 52000.00, 'Account Executive', '2023-01-30', (SELECT id FROM departments WHERE name = 'Sales')),
    
    -- 1 HR
    ('1995-06-07', 'Roberto', 'Frias', 31000.00, 'HR Generalist', '2025-01-05', (SELECT id FROM departments WHERE name = 'HR')),

    -- 2 Sin Departamento (NULL)
    ('2003-09-22', 'Ana', 'Perez', 24000.00, 'Intern', '2024-09-01', NULL),
    ('2002-12-01', 'David', 'Gomez', 27000.00, 'Support', '2023-10-10', NULL);


SELECT
    employees.first_name,
    employees.last_name,
    departments.name 
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id;

SELECT
    employees.first_name,
    employees.last_name,
    departments.name 
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id;


SELECT
    departments.name,
    count(employees.id) 
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id 
GROUP BY 
    departments.id;


SELECT
    departments.name,
    count(employees.id) 
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id 
WHERE 
    department_id = (SELECT id FROM departments WHERE name = 'Engineering')
GROUP BY 
    departments.name;


SELECT
    departments.name,
    AVG(employees.salary) AS average_salary
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id 
GROUP BY 
    departments.name;


SELECT
    departments.name,
    MAX(employees.salary) AS max_salary
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id
GROUP BY
    departments.name
ORDER BY
    max_salary DESC
LIMIT 1;

-- otra forma seria usando subconsultas:
SELECT
    departments.name,
    employees.salary AS max_salary
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id
WHERE
    employees.salary = (
        SELECT MAX(salary) FROM employees
    );


SELECT
    departments.name,
    COUNT(DISTINCT employees.title)
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id
GROUP BY
    departments.name;

SELECT
    employees.first_name,
    employees.last_name,
    departments.name AS department_name
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id
ORDER BY
    departments.name ASC,
    employees.last_name ASC;

-- respuesta CHATGPT
SELECT
    departments.name,
    STRING_AGG(employees.last_name || ', ' || employees.first_name, '; ' ORDER BY employees.last_name) AS employee_list
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id
GROUP BY
    departments.name
ORDER BY
    departments.name ASC;


SELECT
    departments.name,
    COUNT(employees.title)
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id
GROUP BY
    departments.name
LIMIT 3;


-- ver la estructura que tiene una tabla
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'employees';

-- EJERCICIOS EXTRA PROPUESTOS POR CHATGPT
-- 1.Encuentra todos los empleados cuyo salario es mayor que el salario promedio de su departamento.
SELECT 
    e.first_name, 
    e.last_name, 
    e.salary, 
    d.name AS department_name
FROM 
    employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
);

-- 2.Asigna un ranking a los empleados de cada departamento según su salario, siendo 1 el salario más alto.
SELECT 
    e.first_name,
    e.last_name,
    e.salary,
    d.name AS department_name,
    RANK() OVER(
        PARTITION BY e.department_id 
        ORDER BY e.salary DESC
    ) AS salary_rank
FROM employees e
JOIN departments d ON e.department_id = d.id;

-- partition: los grupos que hace; order by: cómo los ordena

-- 3.Muestra, para cada empleado, cuánto gana por encima o por debajo del salario promedio de su departamento.
SELECT 
    e.first_name,
    e.last_name,
    e.salary,
    d.name AS department_name,
    e.salary - AVG(e.salary) OVER(PARTITION BY e.department_id) AS salary_diff
FROM employees e
JOIN departments d ON e.department_id = d.id;

-- se calcula el promedio del salario al que pertenece


-- 4.Encuentra el departamento que tiene el salario promedio más alto.
SELECT 
    d.name AS department_name,
    AVG(e.salary) OVER(PARTITION BY e.department_id) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
LIMIT(1);

SELECT 
    d.name AS department_name, 
    AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
ORDER BY avg_salary DESC
LIMIT 1;

-- 5.Encuentra los departamentos que solo tienen un empleado y dime quienes son.
SELECT 
    e.first_name,
    e.last_name,
    e.salary,
    d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.department_id IN (
    SELECT department_id
    FROM employees
    GROUP BY department_id
    HAVING COUNT(*) = 1
);

-- solo selecciona aquellos cuyo department_id este dentro de la subconsulta


-- 6.Encuentra los departamentos que tienen más de 3 empleados y cuyo salario promedio es mayor a 40,000.
SELECT 
    e.first_name,
    e.last_name,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.department_id IN (
    SELECT department_id
    FROM employees
    GROUP BY department_id
    HAVING COUNT(*) = 3
) AND e.salary > 40000;
-- me dice a la persona que cumple con esos requisitos, no el departamento.

SELECT 
    d.name AS department_name, 
    COUNT(e.id) AS total_employees, 
    AVG(e.salary) AS avg_salary
FROM departments d
JOIN employees e ON e.department_id = d.id
GROUP BY d.name
HAVING COUNT(e.id) > 3 AND AVG(e.salary) > 40000;

-- 7.Muestra el último empleado añadido (según title_date) de cada departamento.
SELECT 
    e.first_name,
    e.last_name,
    e.title_date,
    d.name AS department_name
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.title_date = (
    SELECT MIN(e2.title_date)
    FROM employees e2
    WHERE e2.department_id = e.department_id
);

SELECT DISTINCT ON (e.department_id) 
    e.first_name, 
    e.last_name, 
    d.name AS department_name, 
    e.title_date
FROM employees e
JOIN departments d ON e.department_id = d.id
ORDER BY e.department_id, e.title_date DESC;

-- permite DISTINCT ON (columna) para seleccionar solo una fila por cada valor distinto de esa columna.
-- En este caso: una fila por cada department_id.
-- Pero cuál fila se escoge depende del ORDER BY.


-- 8. Muestra cada departamento con el salario máximo, mínimo y la diferencia entre ambos, ordenado por mayor dispersión.
SELECT 
    d.name AS department_name,
    MAX(e.salary) AS max_salary,
    MIN(e.salary) AS min_salary,
    MAX(e.salary) - MIN(e.salary) AS dif_salary
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
ORDER BY dif_salary DESC;


-- 9.Encuentra todos los empleados cuyo título contiene la letra 'i' y que ganan más que el salario promedio de su departamento.

SELECT 
    e.first_name,
    e.last_name,
    e.title,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.title ILIKE '%i%'
    AND e.salary > (
    SELECT AVG(salary)
    FROM employees
    WHERE department_id = e.department_id
    );

-- poner ILIKE para que no nos distinga entre mayúsculas y minúsculas


-- 10.Cuenta cuántos empleados tienen cada título dentro de cada departamento.
SELECT 
    d.name AS department_name,
    e.title,
    COUNT(e.id) AS total_employees
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name, e.title
ORDER BY d.name, total_employees DESC;



