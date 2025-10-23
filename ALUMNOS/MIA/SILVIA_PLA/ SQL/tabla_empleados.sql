
CREATE TABLE employees(
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
birth_date VARCHAR(100) NOT NULL,
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(255)  NOT NULL,
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES
('1985-03-10', 'Ana', 'López', 12000.50, 'Data Analyst', '2020-05-14'),
('1990-07-22', 'Ana', 'Martínez', 18000.00, 'Software Engineer', '2020-06-10'),
('1992-01-15', 'Ana', 'Pérez', 25000.75, 'Project Manager', '2021-03-09'),
('1988-12-05', 'Carlos', 'Ruiz', 32000.00, 'Backend Developer', '2019-08-20'),
('1995-06-18', 'María', 'Sanchis', 28000.50, 'Frontend Developer', '2020-02-02'),
('1993-11-11', 'María', 'García', 41000.00, 'UX Designer', '2020-09-10'),
('1991-02-20', 'María', 'Soler', 37000.25, 'QA Tester', '2022-04-11'),
('1987-04-17', 'Luis', 'Fernández', 15000.00, 'Data Scientist', '2020-01-01'),
('1996-09-07', 'Luis', 'Gómez', 22000.00, 'System Admin', '2023-05-17'),
('1989-10-30', 'Lucía', 'Navarro', 48000.00, 'DevOps Engineer', '2020-10-30'),
('1994-12-09', 'Pablo', 'Martín', 23000.00, 'Business Analyst', '2021-07-25'),
('1986-05-13', 'Clara', 'Gil', 5200.00, 'HR Specialist', '2020-12-15'),
('1992-03-27', 'Javier', 'Ortega', 33000.00, 'Scrum Master', '2020-03-20'),
('1998-08-08', 'Elena', 'Moreno', 14000.50, 'Product Designer', '2022-06-18'),
('1983-02-02', 'Diego', 'Romero', 27000.75, 'Marketing Lead', '2020-07-07');

SELECT * FROM employees;

SELECT first_name, salary FROM employees;
-- coge solo el usuario con id 2
SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>100;
SELECT * FROM employees WHERE salary <=100;

-- elimina el empleado cuyo id sea 5
DELETE FROM employees WHERE id = 5;

UPDATE employees SET first_name = 'Maria' WHERE id = 8;

DELETE FROM employees WHERE salary >20000;
SELECT * FROM users WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;


SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name FROM employees AS nombrecompleto WHERE id=2 ;

SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

-- Muestra el número total de empleados
SELECT COUNT(id) FROM employees;

-- Muestra el empleado con el salario más alto
SELECT (salary) FROM employees;

-- Muestra el salario medio por titulo
SELECT AVG(salary) FROM employees;
-- Muestra el salario máximo y mínimo por título
SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

-- Muestra el first_name y salary de cada empleado redondeando a 2 decimales

SELECT first_name, ROUND(salary, 2) AS salario_redondeado
FROM employees;

-- EXTRA
-- Seleccionar el nombre del empleado (first_name) y su salary
SELECT first_name FROM employees;
-- Calcular la columna impuestos 
-- como el 21 % del salario (salary * 0.21) 
-- y redondearla a 2 decimales.

SELECT 
    first_name,
    salary,
    ROUND(salary * 0.21, 2) AS impuestos,
    ROUND(salary - (salary * 0.21), 2) AS salario_neto
FROM employees;




CREATE TABLE IF NOT EXISTS departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

ALTER TABLE employees
ADD COLUMN department_id INTEGER REFERENCES departments(id);


INSERT INTO departments (name)
VALUES 
('Engineering'),
('Marketing');

SELECT * FROM departments;
SELECT * FROM employees;


-- Asignar dos empleados a Engineering (id = 1)
UPDATE employees
SET department_id = 1
WHERE id IN (1, 14);
-- Asignar un empleado a Marketing (id = 2)



UPDATE employees
SET department_id = 2
WHERE id = 16;


-- Realiza una consulta que muestre
-- todos los empleados junto con el nombre de su departamento.

SELECT 
    employees.first_name,
    employees.last_name,
    employees.title,
    departments.name AS department_name
FROM employees
INNER JOIN departments
ON employees.department_id = departments.id;

INSERT INTO departments (name)
VALUES 
('Human Resources'),
('Sales'),
('Finance');

SELECT * FROM departments;
UPDATE employees
SET department_id = 3
WHERE id = 16;

SELECT * FROM employees;

SELECT 
    e.first_name,
    e.last_name,
    e.title,
    d.name AS department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;



