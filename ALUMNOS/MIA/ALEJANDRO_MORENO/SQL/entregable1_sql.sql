-- creacion de la tabla employees
CREATE TABLE IF NOT EXISTS employees (
 id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
 birth_date   DATE NOT NULL, 
 first_name   VARCHAR(100) NOT NULL,
 last_name    VARCHAR(100) NOT NULL,  
 register_date  TIMESTAMPTZ NOT NULL DEFAULT now() --default now:por defecto cualcula fecha y h en ese momento
);


-- añadimos nuevas columnas
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2) NOT NULL;
ALTER TABLE employees ADD COLUMN title VARCHAR(100) NOT NULL;
ALTER TABLE employees ADD COLUMN title_date DATE NOT NULL;


-- insertamos valores 
INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES
('2003-06-02', 'Alejandro', 'Moreno', 48000, 'Data Analyst', '2025-06-10'),
('1990-07-24', 'Laura', 'Martínez', 35000, 'Project Manager', '2020-09-15'),
('1988-11-02', 'Laura', 'Ruiz', 29000, 'HR Specialist', '2019-06-22'),
('1995-01-30', 'Carlos', 'Fernández', 18000, 'Software Engineer', '2020-03-01'),
('1992-09-10', 'Carlos', 'Pérez', 41000, 'System Administrator', '2021-08-10'),
('1987-06-05', 'Carlos', 'Santos', 22000, 'Database Developer', '2020-12-01'),
('1993-04-20', 'Lucía', 'Moreno', 5200, 'Marketing Assistant', '2018-05-15'),
('1991-08-12', 'María', 'Castro', 27000, 'UX Designer', '2020-11-05'),
('1989-02-03', 'María', 'López', 33000, 'Financial Analyst', '2022-01-22'),
('1994-10-28', 'María', 'Serrano', 15000, 'Operations Coordinator', '2020-06-19'),
('1986-12-14', 'Andrés', 'Jiménez', 46000, 'Senior Developer', '2017-07-30'),
('1997-07-19', 'Lucía', 'Navarro', 12000, 'Junior Developer', '2020-02-10'),
('1998-03-09', 'Pablo', 'Ramírez', 25000, 'Account Executive', '2021-09-14'),
('1984-05-25', 'Sofía', 'Blanco', 50000, 'CTO', '2019-10-05'),
('1999-12-01', 'Hugo', 'Díaz', 8000, 'Intern Engineer', '2020-07-01');

-- creacion de la segunda tabla departamentos
CREATE TABLE departments (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);

-- insertar valores
INSERT INTO departments (nombre)
VALUES 
  ('Engineering'),
  ('Marketing');

--añadimos a la tabla employees la columna departments_id que sera la clave 
--que referenciara a departments, asi podremos unirlas si fuera necesario
ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

-- Asignar dos empleados al departamento Engineering
UPDATE employees
SET departments_id = 1
WHERE id IN (1, 2);

-- Asignar un empleado al departamento Marketing
UPDATE employees
SET departments_id = 2
WHERE id = 3;

-- algunas consultas 
--Selecciona a todos tus empleados: 
SELECT * from employees;

--Selecciona a todos tus empleados mostrando solamente el first_name y salary;
SELECT first_name, salary FROM employees;

--Muestra el empleado cuyo id sea 2.
SELECT * FROM employees WHERE id=2;

--Selecciona a todos los empleados con un salario superior a 20000;
SELECT * FROM employees WHERE salary>20000;

--Selecciona a todos los empleados con un salario inferior o igual a 10000;
SELECT * FROM employees WHERE salary<=10000;

--Actuaiza el first_name del empleado cuyo id sea 7.
UPDATE employees SET first_name = 'Marcos' WHERE id = 7;

--Elimina el emppleado cuyo id sea 5:
DELETE FROM employees WHERE id = 5;

--Elimina a todos los empleados con un salario superior a 2000.
DELETE FROM employees WHERE salary > 20000;

---Selecciona a todos los empleados con un salario entre 14000 y 50000:
SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

---Selecciona los empleados por birth_date de forma descendiente:
SELECT * FROM employees ORDER BY birth_date  DESC;

--Muestra el first_name de los empleados sin repetir:
SELECT DISTINCT first_name FROM employees;

--Muestrame el nombre completo del empleado como nombre_completo cuyo id=13.
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 4;

--Muestra los empleados cuyo nombre empieza por P:
SELECT * FROM employees WHERE first_name LIKE 'P%';

--Muestra los empleados cuyo nombre contiene una a:
SELECT * FROM employees WHERE first_name LIKE '%a%';

--Muestra el número total de empleados.
SELECT COUNT(*) FROM employees;

--Muestra el empleado con el salario más alto.
SELECT first_name, MAX(salary) FROM employees GROUP BY first_name ORDER BY MAX(salary) DESC;

--Muestra el first_name y el salary de cada empleado redondeando a 2 decimales:
SELECT first_name, salary, ROUND(salary, 2) AS salario_redondeado FROM employees;

--Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento. 
SELECT  employees.first_name, departments.nombre
FROM employees INNER JOIN departments ON employees.id = departments.id;

--Inserta 1 departamento:
INSERT INTO departments(nombre)
VALUES ('RRHH');

--Muestra todos los departamentos:
SELECT * FROM departments;

--Inserta un empleado con departamento:
UPDATE employees SET departments_id= 3 WHERE id= 4;

--Muestra todos los empleados:
SELECT*FROM employees;

--Muestra todos los empleados junto con el nombre del departamento al que pertenecen:
SELECT e.id AS employee_id,
       e.first_name AS employee_name,
       d.nombre AS department_name
FROM employees e
LEFT JOIN departments d
ON e.departments_id = d.id;




















