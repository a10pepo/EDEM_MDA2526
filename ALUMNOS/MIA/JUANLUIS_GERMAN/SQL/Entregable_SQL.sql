CREATE TABLE IF NOT EXISTS users(
id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name      VARCHAR(100) NOT NULl,
last_name       VARCHAR(100) NOT NULl,
email           VARCHAR(255) UNIQUE NOT NULl, 
password   TEXT NOT NULL,              
register_date   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS employees(
    id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date VARCHAR (8),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (first_name,last_name,salary,title,title_date)
VALUES ('Juan','Gonzalez','500','Data intern','01-02-2024');


INSERT INTO employees (first_name, last_name, salary, title, title_date)
VALUES 
('Juan', 'Gonzalez', 15000, 'Data Analyst', '2024-02-01'),
('Juan', 'Martinez', 20000, 'Data Scientist', '2023-06-15'),
('Juan', 'Lopez', 12000, 'Data Engineer', '2020-09-10'),
('Maria', 'Fernandez', 18000, 'HR Specialist', '2020-04-21'),
('Carlos', 'Perez', 25000, 'Software Developer', '2021-11-30'),
('Ana', 'Ruiz', 22000, 'Marketing Manager', '2020-01-17'),
('Lucia', 'Sanchez', 31000, 'Financial Analyst', '2022-03-22'),
('Miguel', 'Torres', 27000, 'Project Manager', '2020-10-12'),
('Laura', 'Vega', 45000, 'Operations Director', '2024-07-09'),
('Sergio', 'Navarro', 38000, 'UX Designer', '2020-05-18'),
('Elena', 'Morales', 33000, 'Legal Advisor', '2021-02-05'),
('David', 'Castro', 5000, 'Customer Support', '2023-08-11'),
('Paula', 'Herrera', 48000, 'Business Consultant', '2022-12-01'),
('Andres', 'Diaz', 26000, 'Account Executive', '2020-03-09');

SELECT * FROM employees;

SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Pepe' where id = 7;

DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY title_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees;

SELECT * FROM employees WHERE first_name LIKE ' P%'; 
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) AS total_num_employees FROM employees;
SELECT MAX(salary) AS max_salary FROM employees;
SELECT ROUND(AVG(salary),1) AS avg_salary FROM employees;
SELECT MAX(salary) AS max_salary, MIN(salary) AS min_salary FROM employees;

SELECT first_name, ROUND(salary,2) FROM employees;

SELECT first_name AS nombre, salary AS salario, 
    ROUND(salary * 0.21,2) AS  impuestos, 
   ROUND(salary - (salary * 0.21),2) AS salario_neto
    FROM employees;


CREATE TABLE departments(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR );

ALTER TABLE employees
ADD COLUMN department_id BIGINT;

ALTER TABLE employees
ADD CONSTRAINT fk_employees_departments
FOREIGN KEY (department_id)
REFERENCES departments(id);

INSERT INTO departments (name) 
VALUES ('Engineering'),('Marketing');

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Engineering')
WHERE id IN (1, 2); 

UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Marketing')
WHERE id = 3;

INSERT INTO departments (name) VALUES ('data');

SELECT * FROM departments;

INSERT INTO employees (first_name, last_name, salary, title, title_date, department_id) 
VALUES ('David','Fuertes','35000','UX developer','2021-05-10',2);

SELECT * FROM employees;

SELECT employees.id AS id_empleados, 
departments.id AS departamento_id,
employees.first_name AS nombre_empleado,
employees.last_name AS nombre_apellidos,
departments.name AS nombre_departamento
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;

SELECT * FROM employees
LEFT JOIN departments
ON employees.department_id = departments.id;