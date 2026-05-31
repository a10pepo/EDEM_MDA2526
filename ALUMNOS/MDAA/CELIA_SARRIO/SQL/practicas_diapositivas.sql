-- Clase 20/10/2025

-- Práctica (Diapo. 25)

-- Configura PostgreSQL en tu proyecto siguiendo estos pasos: Instrucciones
-- La base de datos debe llamarse my_company_database.

CREATE DATABASE my_company_database; 

-- Práctica (Diapo. 27)

-- Crea una tabla llamada employees que contenga los siguientes campos:

-- Id
-- birth_date
-- first_name
-- last_name

-- Importante: los campos id, first_name y last_name deben ser NOT NULL, y id debe ser la clave primaria de la tabla.

CREATE TABLE IF NOT EXISTS employees (
    id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date  DATE NOT NULL,
    first_name  VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL
);

-- Práctica (Diapo. 29)

-- Añade tres columnas a la tabla employees:
-- - salary: tipo NUMERIC(10,2)
-- - title: tipo VARCHAR de máximo 100 caracteres.
-- - title_date: tipo DATE

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2), 
ADD COLUMN title VARCHAR(100), 
ADD COLUMN title_date DATE;

-- Práctica (Diapo. 33)

-- Inserta al menos 15 empleados nuevos en la tabla employees, que cumplan los siguientes criterios: 
-- - Al menos 3 empleados deben tener el mismo nombre.
-- - Los salarios deben variar entre 5000 y 50.000.
-- - Todos los empleados deben tener un título.
-- - Al menos 5 empleados deben tener title_date del año 2020.

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) 
VALUES ('1985-03-15', 'Juan', 'Pérez', 45000.00, 'Manager', '2019-06-01'),
('1990-07-22', 'María', 'Gómez', 38000.00, 'Developer', '2020-03-15'),
('1988-11-30', 'Carlos', 'López', 52000.00, 'Analyst', '2021-01-20'),
('1992-05-10', 'Ana', 'Martínez', 29000.00, 'Designer', '2020-08-25'),
('1983-12-05', 'Luis', 'Rodríguez', 47000.00, 'Consultant', '2018-11-30'),
('1995-09-18', 'Sofía', 'Hernández', 32000.00, 'Developer', '2020-05-10'),
('1987-04-27', 'Juan', 'Ramírez', 41000.00, 'Manager', '2019-09-15'),
('1991-02-14', 'Elena', 'Díaz', 36000.00, 'Analyst', '2020-12-01'),
('1984-08-09', 'Miguel', 'Torres', 55000.00, 'Director', '2017-07-20'),
('1993-10-23', 'Laura', 'Vargas', 28000.00, 'Intern', '2020-02-28'),
('1986-06-12', 'Juan', 'Sánchez', 43000.00, 'Manager', '2019-04-10'),
('1994-01-29', 'Patricia', 'Cruz', 5000.00, 'Developer', '2020-11-15'),
('1989-03-03', 'Javier', 'Flores', 46000.00, 'Consultant', '2018-05-05'),
('1996-12-19', 'Carmen', 'Morales', 5500.00, 'Designer', '2020-09-30'),
('1982-07-07', 'Diego', 'Jiménez', 5000.00, 'Manager', '2019-01-15');

-- Práctica (Diapo. 36)

-- Selecciona todos tus empleados.
-- Selecciona todos tus empleados mostrando solamente el first_name y salary.

SELECT * FROM employees;

SELECT first_name, salary FROM employees;

-- Práctica (Diapo. 39)

-- Muestra el empleado cuyo id sea 2

SELECT * FROM employees WHERE id = 2;

-- Selecciona todos los empleados con un salario superor a 20000

SELECT * FROM employees WHERE salary > 20000;

-- Selecciona todos los empleados con un salario inferior o igual a 10000

SELECT * FROM employees WHERE salary <= 10000;

-- Práctica (Diapo. 42)

-- Actualiza el first_name del empleado cuyo id sea 7

UPDATE employees SET first_name = 'Pepe' WHERE id = 7;

-- Práctica (Diapo. 44)

-- Elimina al empleado cuyo id sea 5

DELETE FROM employees WHERE id = 5;

-- Elimina a todos los empleados con un salario super a 20000

DELETE FROM employees WHERE salary = 20000;

-- Práctica (Diapo. 47)

-- Selecciona todos los empleados con un salario entre 14.000 y 50.000

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

-- Ordena los empleados por birth_date de forma descendiente

SELECT * FROM employees ORDER BY birth_date DESC;

-- Práctica (Diapo. 51)

-- Muestra los first_name de los empleados sin repetir

SELECT DISTINCT first_name FROM employees;

-- Muestrame el nombre completo del empleado como “nombre_completo” cuyo id 9 

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

-- Práctica (Diapo. 54)

-- Muestra los empleados cuyo nombre empiece por P

SELECT * FROM employees WHERE first_name LIKE 'P%';

-- Muestra los empleados cuyo nombre contenga la a

SELECT * FROM employees WHERE first_name LIKE '%a%';

-- Práctica (Diapo. 58)

-- Muestra el número total de empleados

SELECT COUNT(id) FROM employees;

-- Muestra el empleado con el salario más alto

SELECT MAX(salary) FROM employees;

-- EXTRA:

-- Muestra el salario medio por titulo

SELECT title, AVG(salary) FROM employees GROUP BY title;

-- Muestra el salario máximo y mínimo por título

SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

-- Práctica (Diapo. 64)

-- Muestra el first_name y salary de cada empleado redondeando a 2 decimales

SELECT first_name, salary, ROUND(salary, 2) FROM employees;

-- Práctica EXTRA (Diapo. 65)

-- Escribe una consulta SQL que, a partir de la tabla employees, calcule el importe de impuestos aplicando un 21 % sobre el salario bruto y obtenga el salario neto (bruto − impuestos), mostrando los resultados con 2 decimales y usando alias (AS) claros.

-- - Seleccionar el nombre del empleado (first_name) y su salary.
-- - Calcular la columna impuestos como el 21 % del salario (salary * 0.21) y redondearla a 2 decimales.
-- - Calcular la columna salario_neto como salary - impuestos, también redondeada a 2 decimales.
-- - Usar alias (AS) exactamente con los nombres: impuestos y salario_neto

SELECT first_name, salary,
    ROUND ((salary * 0.21), 2) AS impuestos,
    ROUND ((salary - (salary * 0.21)), 2) AS salario_neto
FROM employees;

-- Clase 22/10/2025

-- Práctica (Diapo. 40)

-- Crea una tabla llamada departments que contenga un campo llamado name.

CREATE TABLE IF NOT EXISTS departments (
    departments_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    departments_name VARCHAR(100)
); 

-- Modifica tu tabla de employees y añade la FK department_id que haga referencia al id de la tabla departments.

ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(departments_id);

-- Inserta dos departamentos en la nueva tabla departments, por ejemplo:
-- - Engineering
-- - Marketing

INSERT INTO departments (departments_name) 
VALUES ('Engineering'),
('Marketing');

-- Actualiza tres empleados en la tabla employees.
-- - Asigna dos empleados al departamento Engineering.
-- - Asigna un empleado al departamento Marketing.

UPDATE employees SET departments_id = 1 WHERE id IN (1, 2);
UPDATE employees SET departments_id = 2 WHERE id = 3;

select * from employees;

-- Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento.

SELECT e.*, d.departments_name
FROM employees e
JOIN departments d ON e.departments_id = d.departments_id;

-- Práctica EXTRA (Diapo. 41)

-- Inserta departamentos. Inserta al menos 6 departamentos con estos nombres (idénticos):
-- - Engineering
-- - Marketing
-- - Sales
-- - HR
-- - R&D
-- - Legal	

INSERT INTO departments (departments_name) 
VALUES ('Sales'),
('HR'),
('R&D'),
('Legal');

-- Inserta empleados (mínimo 12). Con los siguientes requisitos:
-- - Distribución por departamento:
-- Engineering: 4 empleados
-- Marketing: 3 empleados
-- Sales: 2 empleados
-- HR: 1 empleado
-- Sin departamento (department_id = NULL): 2 empleados(para diferenciar INNER JOIN vs LEFT JOIN)

-- - Salarios: mezcla valores para que existan medias y máximos distintos.Ejemplos por departamento:
-- Engineering: 42 000, 55 000, 63 500, 75 000
-- Marketing: 33 000, 39 500, 48 000
-- Sales: 28 000, 52 000
-- HR: 31 000
-- (los dos sin departamento: 24 000 y 27 000)

-- - Títulos (title): asegúrate de que por departamento haya varios títulos, para poder contar títulos distintos.Sugeridos:
-- Engineering: Backend Engineer, Frontend Engineer, Data Engineer, DevOps
-- Marketing: SEO Specialist, Content Manager, Brand Manager
-- Sales: Sales Rep, Account ExecutiveHR: 
-- HR Generalist
-- (sin depto): Intern, Support 

-- - Fechas: 
-- birth_date: fechas razonables (1995–2003).
-- title_date: mezcla de 2023–2025).

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('1998-04-12','Alba','Navas',42000.00,'Backend Engineer','2023-10-05',
(SELECT departments_id FROM departments WHERE departments_name='Engineering')),
('1997-09-21','Hugo','Carrasco',55000.00,'Frontend Engineer','2024-03-18',
(SELECT departments_id FROM departments WHERE departments_name='Engineering')),
('1999-02-03','Clara','Benítez',63500.00,'Data Engineer','2025-01-22',
(SELECT departments_id FROM departments WHERE departments_name='Engineering')),
('1996-12-17','Pablo','Serrano',75000.00,'DevOps','2023-07-11',
(SELECT departments_id FROM departments WHERE departments_name='Engineering'));

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('2000-06-08','Nerea','Pascual',33000.00,'SEO Specialist','2023-11-20',
(SELECT departments_id FROM departments WHERE departments_name='Marketing')),
('1998-10-15','Mario','Cuevas',39500.00,'Content Manager','2024-06-02',
(SELECT departments_id FROM departments WHERE departments_name='Marketing')),
('1997-01-29','Iris','Delgado',48000.00,'Brand Manager','2025-02-14',
(SELECT departments_id FROM departments WHERE departments_name='Marketing'));

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('2001-03-11','Sergi','Barrios',28000.00,'Sales Rep','2023-09-07',
(SELECT departments_id FROM departments WHERE departments_name='Sales')),
('1999-12-04','Raquel','Mena',52000.00,'Account Executive','2024-08-19',
(SELECT departments_id FROM departments WHERE departments_name='Sales'));

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('1998-02-22','Elena','Beltrán',31000.00,'HR Generalist','2023-12-12',
(SELECT departments_id FROM departments WHERE departments_name='HR'));

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('2002-07-23','Daniel','Acosta',24000.00,'Intern','2024-04-29',NULL),
('2001-05-02','Irene','Campos',27000.00,'Support','2025-03-08',NULL);

-- Lista solo empleados que tienen departamento (INNER JOIN).

SELECT e.*, d.departments_name
FROM employees e
JOIN departments d ON e.departments_id = d.departments_id;

-- Muestra departamentos sin empleados (LEFT JOIN + IS NULL).

SELECT d.*, e.id AS employee_id
FROM departments d
LEFT JOIN employees e ON d.departments_id = e.departments_id
WHERE e.id IS NULL;

-- Cuenta cuántos empleados hay por departamento (nombre y COUNT).

SELECT d.departments_name, COUNT(e.id) AS numero_empleados
FROM departments d
LEFT JOIN employees e ON d.departments_id = e.departments_id
GROUP BY d.departments_name;

-- Empleados del departamento ‘Engineering’ (por nombre de dept).Salario medio por departamento (nombre y AVG(salary)).

SELECT e.*, d.departments_name
FROM employees e
JOIN departments d ON e.departments_id = d.departments_id
WHERE d.departments_name = 'Engineering';

SELECT d.departments_name, AVG(e.salary) AS salario_medio
FROM departments d
JOIN employees e ON d.departments_id = e.departments_id
GROUP BY d.departments_name;

-- Salario máximo por departamento y qué departamento lo tiene.

SELECT d.departments_name, MAX(e.salary) AS salario_maximo
FROM departments d
JOIN employees e ON d.departments_id = e.departments_id
GROUP BY d.departments_name;

-- Número de títulos distintos por departamento.

SELECT d.departments_name, COUNT(DISTINCT e.title) AS numero_titulos_distintos
FROM departments d
JOIN employees e ON d.departments_id = e.departments_id
GROUP BY d.departments_name;

-- Empleados con su departamento, ordenado por department.name y last_name.

SELECT e.*, d.departments_name
FROM employees e
JOIN departments d ON e.departments_id = d.departments_id
ORDER BY d.departments_name, e.last_name;

-- Top 3 departamentos con más empleados.

SELECT d.departments_name, COUNT(e.id) AS numero_empleados
FROM departments d
JOIN employees e ON d.departments_id = e.departments_id
GROUP BY d.departments_name
ORDER BY numero_empleados DESC
LIMIT 3;

-- Clase 23/10/2025

-- Crea las siguientes consultas :

-- Inserta 1 departamento.

INSERT INTO departments (departments_name) 
VALUES ('Data');

-- Muestra todos los departamentos.

SELECT * FROM departments;

-- Inserta 1 empleado con departamento.

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departments_id) VALUES
('2002-02-22','Sonia','Colomar',71000.00,'Data Analyst','2017-12-12',
(SELECT departments_id FROM departments WHERE departments_name='Data'));

-- Muestra todos los empleados.

SELECT * FROM employees;

-- Muestra todos los empleados junto con el nombre del departamento al que pertenecen.

SELECT e.*, d.departments_name
FROM employees e
JOIN departments d ON e.departments_id = d.departments_id;

-- EXTRA: Muestra todos los empleados con sus departamentos independientemente de si tienen departamento o no.

SELECT e.*, d.departments_name
FROM employees e
LEFT JOIN departments d ON e.departments_id = d.departments_id;
