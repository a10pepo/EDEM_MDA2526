CREATE DATABASE IF NOT EXISTS my_company_database;

CREATE TABLE IF NOT EXISTS users (

id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

first_name      VARCHAR(100) NOT NULL,

last_name       VARCHAR(100) NOT NULL,

email           VARCHAR(255) UNIQUE NOT NULL,

password   TEXT NOT NULL,                

register_date   TIMESTAMPTZ NOT NULL DEFAULT now()

);

ALTER TABLE users ALTER COLUMN age INTEGER;

CREATE TABLE IF NOT EXISTS employees(

    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    birth_date      DATE NOT NULL,

    first_name      VARCHAR(100) NOT NULL,

    last_name       VARCHAR(100) NOT NULL

);


ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;


INSERT INTO users (first_name, last_name, email, password,age)
VALUES ('Ada','Lovelace','ada@example.com','123456',36),
('Luffy', 'Monkey D.', 'luffy@mugiwara.com', '123456',17), 
('Zoro', 'Roronoa', 'zoro@mugiwara.com', '123456',21),
('Sanji', 'Vinsmoke', 'sanji@mugiwara.com', '123456',22);


INSERT INTO public.employees (
  birth_date,
  first_name,
  last_name,
  salary,
  title,
  title_date
)
VALUES

  ('1990-05-15', 'Alex', 'Smith', 48000, 'Senior Engineer', '2020-01-10'),
  ('1992-08-20', 'Alex', 'Johnson', 45000, 'Engineer', '2020-02-15'),
  ('1988-11-01', 'Alex', 'Brown', 47000, 'Team Lead', '2020-05-30'),
  ('1995-02-10', 'Maria', 'Garcia', 42000, 'Designer', '2020-07-22'),
  ('1993-07-07', 'David', 'Lee', 38000, 'Junior Developer', '2020-11-05'),

  -- 10 empleados adicionales
  ('1985-12-30', 'Emily', 'Davis', 49500, 'Marketing Manager', '2021-03-14'),
  ('1998-04-18', 'Michael', 'Wilson', 15000, 'Analyst', '2022-06-01'),
  ('1991-09-05', 'Sophia', 'Martinez', 41000, 'HR Specialist', '2019-10-10'),
  ('1989-01-25', 'James', 'Anderson', 46000, 'Product Manager', '2021-08-19'),
  ('1996-06-12', 'Olivia', 'Taylor', 35000, 'Content Writer', '2022-01-05'),
  ('1994-03-22', 'William', 'Thomas', 43000, 'Sales Representative', '2019-04-11'),
  ('1987-08-14', 'Isabella', 'Moore', 49000, 'Senior Analyst', '2021-11-20'),
  ('1999-11-08', 'Benjamin', 'Jackson', 30000, 'Intern', '2023-02-28'),
  ('1990-10-27', 'Mia', 'Martin', 9000, 'Support Specialist', '2022-05-16'),
  ('1986-07-19', 'Lucas', 'White', 44000, 'Operations Lead', '2021-09-03');

SELECT * FROM employees;

SELECT first_name, salary FROM employees;

SELECT * FROM employees
WHERE id = 2;

SELECT * FROM employees
WHERE salary > 20000;

SELECT * FROM employees
WHERE salary <= 10000;

UPDATE employees SET first_name='Lucas' WHERE id = 7;

-- DELETE FROM employees WHERE id = 5;
-- DELETE FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000

SELECT * FROM employees ORDER BY birth_date DESC


SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

SELECT  * FROM employees WHERE first_name LIKE 'P%';

SELECT  * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT AVG(salary) FROM employees GROUP BY title;

SELECT MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, ROUND(salary, 2) FROM employees;

SELECT current_database();


CREATE TABLE IF NOT EXISTS departments (
id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY   
);

ALTER TABLE departments ADD COLUMN nombre VARCHAR(100) NOT NULL

ALTER TABLE employees ADD COLUMN department_id INT;

ALTER TABLE employees ADD CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id);

INSERT INTO departments (nombre) VALUES ('Engineering'), ('Marketing');


SELECT * FROM departments;

SELECT * FROM employees;


UPDATE employees
SET department_id = (SELECT id FROM departments WHERE nombre = 'Engineering')
WHERE id IN (16, 18);

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE nombre = 'Marketing')
WHERE id = 20; 


SELECT 
    e.first_name, 
    e.last_name, 
    e.salary,
    d.nombre AS nombre_departamento
FROM 
    employees e
LEFT JOIN 
    departments d ON e.department_id = d.id;


INSERT INTO departments (nombre) 
VALUES ('Sales');

SELECT * FROM departments;

INSERT INTO employees (
  birth_date,
  first_name,
  last_name,
  salary,
  title,
  title_date,
  department_id
)
VALUES
  (
    '1993-08-25',
    'Carlos',
    'Gomez',
    55000,
    'Sales Manager',
    '2023-05-10',
    (SELECT id FROM departments WHERE nombre = 'Sales')
  );

SELECT * FROM employees;

SELECT 
    e.first_name, 
    e.last_name, 
    d.nombre AS nombre_departamento
FROM 
    employees e
LEFT JOIN 
    departments d ON e.department_id = d.id;


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