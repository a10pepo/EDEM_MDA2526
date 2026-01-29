CREATE TABLE IF NOT EXISTS users (
id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name      VARCHAR(100) NOT NULL,
last_name       VARCHAR(100) NOT NULL,
email           VARCHAR(255) UNIQUE NOT NULL,
password TEXT NOT NULL,
register_date TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE users ADD COLUMN age VARCHAR(3);

ALTER TABLE users ALTER COLUMN age TYPE INTEGER USING age::integer;

ALTER TABLE users DROP COLUMN age;


CREATE TABLE IF NOT EXISTS employees (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    birth_date      TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2) DEFAULT 0.00 NOT NULL;

ALTER TABLE employees ADD COLUMN title VARCHAR(100) NOT NULL;

ALTER TABLE employees DROP COLUMN title_date;

ALTER TABLE employees ADD COLUMN title_date DATE NOT NULL DEFAULT now();

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date) VALUES
('John', 'Doe', '1988-03-22', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Engineer', '2020-05-10'),
('Jane', 'Smith', '1992-11-30', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Analyst', '2019-08-15'),
('Alice', 'Johnson', '1980-07-14', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Designer', '2021-01-20'),
('Bob', 'Brown', '1975-04-18', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Engineer', '2020-03-12'),
('Charlie', 'Davis', '1983-10-09', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Analyst', '2018-11-25'),
('Eve', 'Wilson', '1995-02-28', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Designer', '2020-06-30'),
('Frank', 'Miller', '1987-09-17', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Engineer', '2019-12-05'),
('Grace', 'Taylor', '1991-05-23', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Analyst', '2020-09-14'),
('Hank', 'Anderson', '1979-01-11', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Designer', '2021-03-08'),
('Ivy', 'Thomas', '1984-08-29', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Engineer', '2017-07-19'),
('John', 'Doe', '1993-12-02', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Analyst', '2020-10-22'),
('Jane', 'Smith', '1986-06-06', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Designer', '2019-04-16'),
('Alice', 'Johnson', '1994-03-15', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Engineer', '2020-01-05'),
('Kevin', 'White', '1982-11-20', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Analyst', '2018-02-28'),
('Laura', 'Harris', '1990-04-12', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Designer', '2020-08-03');


SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary >= 20000;
SELECT * FROM employees WHERE salary < 10000;


UPDATE employees SET first_name = 'Paquito' WHERE id = 7;

DELETE FROM employees WHERE id = 5
DELETE FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER by birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name as nombre FROM employees WHERE id = 34;

SELECT * FROM employees WHERE first_name LIKE 'J%';
SELECT * FROM employees WHERE first_name LIKE '%a%';


SELECT COUNT(*) FROM employees;
SELECT * FROM employees where salary = (SELECT MAX(salary) FROM employees LIMIT 1);

SELECT title, AVG(salary) FROM employees group by title;
SELECT title, MAX(salary), MIN(salary) FROM employees group by title;

SELECT first_name, ROUND(salary, 2) FROM employees

SELECT first_name, ROUND(salary * 0.21, 2) AS impuestos, ROUND(salary-(salary * 0.21), 2) AS salario_neto FROM employees;

CREATE TABLE IF NOT EXISTS departments (
id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name            VARCHAR(100) NOT NULL
);

-- department id must be a foreign key referencing departments table

ALTER TABLE employees ADD COLUMN department_id BIGINT REFERENCES departments(id);

INSERT INTO departments (name) VALUES
('Engineering'),
('Human Resources'),
('Marketing'),
('Sales'),
('Finance');

UPDATE employees SET department_id = 1 WHERE title = 'Engineer';
UPDATE employees SET department_id = 2 WHERE title = 'Analyst';
UPDATE employees SET department_id = 3 WHERE title = 'Designer';

SELECT * FROM employees
SELECT * FROM departments

SELECT employees.first_name, employees.last_name, departments.name as department from employees
INNER join departments on employees.department_id = departments.id;



INSERT INTO departments(name) VALUES('IT');
SELECT * FROM departments;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date, department_id) VALUES
('Zara', 'Khan', '1990-12-15', round(LEAST(GREATEST((25000 + 8000 * (sqrt(-2*ln(random())) * cos(2*pi()*random())))::numeric, 0), 50000), 2), 'Developer', '2021-09-01', 4);

SELECT * from employees;

SELECT employees.first_name, departments.name FROM employees LEFT join departments on employees.department_id = departments.id;

