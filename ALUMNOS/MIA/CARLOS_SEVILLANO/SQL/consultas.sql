-- -- CREATE TABLE IF NOT EXISTS users (
-- --      id                   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
-- --      first_name           VARCHAR(100) NOT NULL,
-- --      last_name            VARCHAR(100) NOT NULL,
-- --      email                VARCHAR(255) UNIQUE NOT NULL,
-- --      password    TEXT NOT NULL,                            
-- --      register_date   TIMESTAMPTZ NOT NULL DEFAULT now()
-- -- );

-- -- ALTER TABLE users ADD COLUMN age VARCHAR(3);
-- -- ALTER TABLE users ALTER COLUMN age TYPE INTEGER USING age::integer;
-- -- ALTER TABLE users DROP COLUMN age;


-- -- CREATE TABLE IF NOT EXISTS users (
-- --      id                    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
-- --      birth_date            DATE,
-- --      first_name            VARCHAR(100) NOT NULL,
-- --      last_name            VARCHAR(100) NOT NULL
-- -- );

-- -- ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
-- -- ALTER TABLE employees ADD COLUMN title VARCHAR(100);
-- -- ALTER TABLE employees ADD COLUMN title_date DATE;

-- -- INSERT INTO users (first_name, last_name, email, password,age)
-- -- VALUES ('Ada','Lovelace','ada@example.com','123456',36);

-- -- INSERT INTO users (first_name, last_name, email, password,age) 
-- -- values ('Luffy', 'Monkey D.', 'luffy@mugiwara.com', '123456',17), 
-- -- ('Zoro', 'Roronoa', 'zoro@mugiwara.com', '123456',21),
-- -- ('Sanji', 'Vinsmoke', 'sanji@mugiwara.com', '123456',22);


-- -- INSERT INTO employees(birth_date,first_name,last_name,salary,title,title_date)
-- -- VALUES ('2002-10-13','Carlos','Sevillano Torres',37000,'Matemática Computacional','2025-12-12'),
-- -- ('1992-04-21','Carlos','López García',48000,'Ingeniería de Software','2020-03-10'),
-- -- ('1988-07-11','Carlos','Martínez Pérez',22000,'Análisis de Datos','2020-06-15'),

-- -- ('1995-09-30','Lucía','Fernández Ruiz',15000,'Estadística Aplicada','2021-05-01'),
-- -- ('1998-11-05','María','Sánchez Torres',32000,'Matemática Computacional','2020-11-20'),
-- -- ('1989-02-13','Pablo','Jiménez López',27000,'Ciencia de Datos','2020-01-18'),
-- -- ('1993-06-08','Sofía','Morales Díaz',18000,'Ingeniería de Sistemas','2020-07-22'),
-- -- ('1991-10-22','Ana','Ramírez Cruz',49000,'Optimización Numérica','2023-03-15'),

-- -- ('1997-12-12','Miguel','Ortega Ruiz',14000,'Matemática Financiera','2021-09-09'),
-- -- ('1990-03-03','Laura','Gómez Torres',5000,'Estadística Aplicada','2022-10-10'),
-- -- ('1987-08-14','Diego','Navarro Pérez',41000,'Inteligencia Artificial','2025-04-04'),
-- -- ('1994-05-25','Elena','Castro Molina',35000,'Programación Científica','2023-08-08'),
-- -- ('1999-01-19','Javier','Domínguez León',28000,'Modelado Matemático','2024-02-20'),
-- -- ('2000-07-17','Isabel','Rey Muñoz',45000,'Aprendizaje Automático','2025-09-09'),
-- -- ('1996-09-27','Andrés','Vega Castillo',26000,'Simulación Numérica','2020-12-01');

-- -- SELECT *
-- -- FROM employees;

-- -- SELECT first_name, salary
-- -- FROM employees;

-- -- SELECT * FROM users WHERE age=17;

-- -- SELECT *
-- -- FROM employees
-- -- WHERE id=1;

-- -- SELECT *
-- -- FROM employees
-- -- WHERE salary>20000;

-- -- SELECT *
-- -- FROM employees
-- -- WHERE salary<=10000;

-- -- UPDATE users SET age = 19 WHERE id = 2;

-- -- UPDATE employees SET first_name='Jorge' WHERE id=7;


-- -- DELETE FROM users WHERE id = 3;

-- -- DELETE FROM employees WHERE id=5;
-- -- DELETE FROM employees WHERE salary>20000;



-- -- SELECT * FROM users ORDER BY id DESC;

-- -- SELECT * FROM users ORDER BY id ASC;

-- -- SELECT * FROM users WHERE age BETWEEN 20 AND 25;


-- -- SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

-- -- SELECT * FROM employees ORDER BY birth_date DESC;


-- -- SELECT first_name || ' ' || last_name AS name FROM users;

-- -- SELECT DISTINCT age FROM users;

-- -- SELECT DISTINCT first_name FROM employees;

-- -- SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;

-- -- SELECT * FROM employees WHERE first_name LIKE 'P%';

-- -- SELECT * FROM employees WHERE first_name LIKE '%a%';

-- -- SELECT COUNT(*) as empleados FROM employees;

-- -- SELECT MAX(salary)
-- -- FROM employees;

-- -- SELECT title, ROUND(AVG(salary),2)
-- -- FROM employees
-- -- GROUP BY title;

-- -- SELECT title, MAX(salary) AS max, MIN(salary) as min
-- -- FROM employees
-- -- GROUP BY title;

-- -- SELECT first_name, ROUND(salary,2)
-- -- FROM employees;

-- -- SELECT first_name, salary,
-- --     ROUND(salary*0.21,2) as impuestos, ROUND(salary-ROUND(salary*0.21,2),2) as salario_neto
-- -- FROM employees

-- -- CREATE TABLE IF NOT EXISTS posts (
--      -- id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--      -- user_id INTEGER NOT NULL REFERENCES users(id),
--      -- title VARCHAR(100) NOT NULL,
--      -- body TEXT,
--      -- publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- -- );


-- -- INSERT INTO posts(user_id, title, body) VALUES (1, 'Post One', 'This is post one'),
-- -- (3, 'Post Two', 'This is post two'),
-- -- (1, 'Post Three', 'This is post three'),
-- -- (2, 'Post Four', 'This is post four'),
-- -- (1, 'Post Five', 'This is post five'),
-- -- (2, 'Post Six', 'This is post six'),
-- -- (1, 'Post Seven', 'This is post seven'),
-- -- (3, 'Post Eight', 'This is post eight');


-- -- CREATE TABLE IF NOT EXISTS departments (
-- --      id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
-- --      name VARCHAR(100) NOT NULL
-- -- );


-- ALTER TABLE employees ADD COLUMN department_id INTEGER REFERENCES departments(id);

-- INSERT INTO departments (name)
-- VALUES 
--     ('Engineering'),
--     ('Marketing');

-- UPDATE employees SET department_id=2 WHERE id=4 or id=10;

-- SELECT e.*,d.name
-- FROM employees as e 
-- JOIN departments as d 
-- ON d.id = e.department_id

-- SELECT *
-- FROM employees

-- CREATE TABLE comments (
--   id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--   post_id  INTEGER NOT NULL REFERENCES posts(id),
--   user_id  INTEGER NOT NULL REFERENCES users(id),
--   body    TEXT NOT NULL,
--   created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

-- INSERT INTO posts(user_id, title, body) 
-- VALUES (1, 'Post One', 'This is post one');

-- select * from posts;

-- INSERT INTO comments(post_id, user_id, body) 
-- VALUES(17, 1, 'This is comment one');

-- SELECT comments.body as comentario,
-- posts.title as titulo_publicitario,
-- users.first_name
-- FROM comments
-- INNER JOIN posts ON posts.id = comments.post_id
-- INNER JOIN users ON users.id = comments.user_id;


-- INSERT INTO departments (name)
-- VALUES 
--     ('Logistic');

-- SELECT * from departments;

-- INSERT INTO employees(birth_date,first_name,last_name,salary,title,title_date,department_id)
-- VALUES ('1999-10-12','Carlos','Almagro Rodriguez',33000,'ADE','2023-02-02', 3)

-- SELECT * FROM employees;

-- SELECT e.*,d.name
-- FROM employees as e 
-- INNER JOIN departments as d 
-- ON d.id = e.department_id;

-- SELECT e.*,d.name
-- FROM employees as e 
-- LEFT JOIN departments as d 
-- ON d.id = e.department_id;

