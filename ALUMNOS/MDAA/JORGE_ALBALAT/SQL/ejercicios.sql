CREATE DATABASE my_first_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10, 2), ADD COLUMN title VARCHAR(100), ADD COLUMN title_date DATE;

INSERT INTO employees (id, first_name, last_name, birth_date, salary, title, title_date) VALUES
(1, 'Sofía', 'Martínez', '1985-06-20', 45000.00, 'Directora de Proyecto', '2020-03-15'),
(2, 'Alejandro', 'Gómez', '1992-11-05', 28000.50, 'Analista de Datos', '2020-01-20'),
(3, 'Sofía', 'López', '1998-03-10', 35000.00, 'Desarrolladora Junior', '2020-07-01'),
(4, 'Carlos', 'Rodríguez', '1975-01-25', 50000.00, 'Gerente Senior', '2018-05-10'),
(5, 'Laura', 'Fernández', '1989-07-14', 15000.00, 'Asistente Administrativa', '2022-11-01'),
(6, 'Sofía', 'Pérez', '1995-09-03', 40000.75, 'Ingeniera de Software', '2020-04-10'),
(7, 'David', 'Sánchez', '1980-04-12', 5000.00, 'Técnico de Soporte', '2023-02-15'),
(8, 'María', 'Díaz', '2000-02-28', 18000.20, 'Becaria de RRHH', '2024-06-01'),
(9, 'Javier', 'Ruiz', '1991-12-01', 32000.00, 'Especialista en Marketing', '2021-08-20'),
(10, 'Elena', 'Torres', '1970-10-18', 48000.50, 'Consultora Financiera', '2019-12-05'),
(11, 'Pablo', 'Vargas', '1993-05-17', 22000.00, 'Diseñador Gráfico', '2020-06-15'),
(12, 'Ana', 'Ramos', '1982-08-08', 38000.00, 'Contadora', '2021-01-01'),
(13, 'Daniel', 'Molina', '1997-03-22', 25000.90, 'Técnico de Redes', '2022-03-10'),
(14, 'Isabel', 'Gil', '1978-06-01', 42000.00, 'Jefa de Equipo', '2019-09-01'),
(15, 'Miguel', 'Hernández', '1986-11-29', 12000.00, 'Vendedor', '2023-05-25');

SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Samuel' WHERE id = 7;

DELETE FROM employees WHERE id = 5;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT CONCAT(first_name, ' ', last_name) AS nombre_completo
FROM employees
WHERE id = 9;

SELECT id, first_name, last_name, title
FROM employees
WHERE first_name LIKE 'P%';

SELECT id, first_name, last_name, title
FROM employees
WHERE first_name LIKE '%a%';

SELECT COUNT(*) AS total_empleados
FROM employees;

SELECT * FROM employees ORDER BY salary DESC LIMIT 1;
SELECT first_name, ROUND(salary, 2) AS salary_redondeado FROM employees;

CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);
ALTER TABLE employees
ADD COLUMN department_id INT,
ADD CONSTRAINT fk_departmentFOREIGN KEY (department_id) REFERENCES departments(id);
INSERT INTO departments (name) VALUES ('Engineering'), ('Marketing');

UPDATE employees
SET department_id = 1
WHERE id IN (1, 2);

UPDATE employees
SET department_id = 2
WHERE id = 3;

SELECT e.id, e.first_name, e.last_name, e.title, d.name AS department_name
FROM employees e INNER JOIN departments d ON e.department_id = d.id; 

INSERT INTO departments (name) VALUES
('Recursos Humanos');
SELECT * FROM departments;
INSERT INTO employees (id, first_name, last_name, birth_date, salary, title, title_date, department_id) VALUES
(16, 'Ricardo', 'Alonso', '1990-10-10', 30000.00, 'Project Manager', '2024-01-01', 1);
SELECT * FROM employees;
SELECT e.id, e.first_name, e.last_name, e.title, d.name AS nombre_departamento
FROM employees e INNER JOIN departments d ON e.department_id = d.id ORDER BY e.id;

