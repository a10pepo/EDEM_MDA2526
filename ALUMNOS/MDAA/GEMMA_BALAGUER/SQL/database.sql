-----------------------------------CLASE 1:

---Ejercicio 1:
--Configura PostgresSQL en tu proyecto.
--La base de datos debe llamarse my_company_database.
CREATE DATABASE my_company_database;

---Ejercicio 2:
--Crea una tabla llamada employees que contenga los siguientes campos:
CREATE TABLE IF NOT EXISTS employees
    (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR (100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL
    );

SELECT*FROM employees; ----- COMPROBACIÓN.

----Ejercicio 3:
--Añade tres columnas a la tabla employees:
--Salary: tipo NUMERIC (10,2)
ALTER TABLE employees ADD COLUMN salary NUMERIC NOT NULL;
--title: tipo VARCHAR de máximo 100 caracteres.
ALTER TABLE employees ADD COLUMN title VARCHAR (100) NOT NULL;
--title_date: tipo DATE
ALTER TABLE employees ADD COLUMN title_date DATE NOT NULL;

--------Ejercicio 4:
---Inserta al menos 15 empleados nuevos en la tabla employees, que cumplan los siguientes criterios: 
--Al menos 3 empleados deben tener el mismo nombre.
--Los salarios deben variar entre 5000 y 50.000.
--Todos los empleados deben tener un título.
--Al menos 5 empleados deben tener title_date del año 202

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES ('2003-03-19', 'Gemma', 'Balaguer', 40000, 'Economía', '2025-06-06'),
('1994-03-12', 'Laura', 'Martínez', 32000, 'Data Analyst', '2021-05-14'),
('1992-07-25', 'Laura', 'Gómez', 45000, 'Data Engineer', '2020-02-10'),
('1990-11-30', 'Laura', 'Pérez', 27000, 'Business Analyst', '2019-07-23'),
('1988-06-02', 'Carlos', 'Ruiz', 50000, 'Project Manager', '2020-03-17'),
('1996-09-15', 'María', 'Santos', 18000, 'Software Developer', '2020-09-12'),
('1993-01-19', 'Javier', 'López', 23000, 'Database Administrator', '2022-11-03'),
('1995-04-10', 'Sofía', 'Castro', 12000, 'Marketing Specialist', '2018-04-25'),
('1989-08-22', 'Andrés', 'Romero', 35000, 'Financial Analyst', '2020-01-09'),
('1997-02-27', 'Lucía', 'Hernández', 16000, 'Data Scientist', '2023-06-21'),
('1991-05-17', 'Miguel', 'Fernández', 28000, 'Sales Executive', '2017-08-10'),
('1994-12-03', 'Elena', 'García', 41000, 'UX Designer', '2020-12-05'),
('1990-09-09', 'Pedro', 'Ortiz', 9000, 'Cloud Engineer', '2022-03-11'),
('1998-10-28', 'Sara', 'Vidal', 14500, 'Software Developer', '2020-10-02'),
('1987-01-11', 'Jorge', 'Torres', 38000, 'Machine Learning Engineer', '2021-02-19'),
('1999-04-05', 'Claudia', 'Navas', 5000, 'HR Assistant', '2019-09-08');

----------Ejercicio 4:
--Selecciona a todos tus empleados: 
SELECT*FROM employees; 
--Selecciona a todos tus empleados mostrando solamente el first_name y salary;
SELECT first_name, salary FROM employees;

-------Ejercicio 5:
--Muestra el empleado cuyo id sea 2.
SELECT first_name, last_name FROM employees WHERE id=2;
--Selecciona a todos los empleados con un salario superior a 20000;
SELECT first_name, last_name, salary FROM employees WHERE SALARY>20000;
--Selecciona a todos los empleados con un salario inferior o igual a 10000;
SELECT first_name, last_name, salary FROM employees WHERE salary<10000;

------Ejercicio 6.
--Actuaiza el first_name del empleado cuyo id sea 7.
UPDATE employees SET first_name='Gema' WHERE id=7;
SELECT*FROM employees; ---COMPROBACIÓN

-------Ejercicio 7:
--Elimina el emppleado cuyo id sea 5:
DELETE FROM employees WHERE id=5;
--Elimina a todos los empleados con un salario superior a 2000.
DELETE FROM employees WHERE salary>20000;

---Añadimos a todos los trabajadores otra vez para poder seguir trabajando.

-----Ejercicio 8:
---Selecciona a todos los empleados con un salario entre 14000 y 50000:
SELECT first_name, last_name, salary FROM employees WHERE salary BETWEEN 14000 AND 50000;
---Selecciona los empleados por birth_date de forma descendiente:
SELECT first_name, last_name, birth_date FROM employees ORDER BY birth_date DESC;

----Ejercicio 9:
--Muestra el first_name de los empleados sin repetir:
SELECT DISTINCT first_name FROM employees;
--Muestrame el nombre completo del empleado como nombre_completo cuyo id=13.
SELECT first_name ||' '|| last_name AS nombre FROM employees WHERE id=13;

----Ejercicio 10:
--Muestra los empleados cuyo nombre empieza por P:
SELECT first_name FROM employees WHERE first_name LIKE 'P%';
--Muestra los empleados cuyo nombre contiene una a:
SELECT first_name FROM employees WHERE first_name LIKE '%a%';

-----Ejercicio 11:
--Muestra el número total de empleados.
SELECT COUNT(id) FROM employees;
--Muestra el empleado con el salario más alto.
SELECT first_name, MAX(salary) FROM employees GROUP BY first_name ORDER BY MAX (salary) DESC;
---SIMPLE: SELECT MAX(Salary) FROM employees;
--Extra:
--Muestra el salario medio por título:
SELECT title, ROUND(AVG(salary),2) FROM employees GROUP BY title ORDER BY ROUND(AVG(salary),2) DESC;
--Muestra el salario máximo y mínio por título:
SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title; 

-----Ejercicio 12:
--Muestra el first_name y el salary de cada empleado redondeando a 2 decimales:
SELECT first_name, salary, ROUND((salary),2) FROM employees;

------------------------------------------CLASE 2:

---EJERCICIO 1:
--Crea una tabla llamada departments que contenga un campo llamado name:
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
--Modifica tu tabla de employees y añade la FK department_id que haga referencia al id de la tabla de departments.
ALTER TABLE employees 
ADD COLUMN departments_id BIGINT 
REFERENCES departments(id);

SELECT*FROM employees; ------COMPROBACIÓN

--Inserta 2 departamentos en la nueva tabla departments:
INSERT INTO departments (name)
VALUES ('Engineering'),
       ('Marketing');

SELECT*FROM departments;---COMPROBACIÓN

---Actualiza tres empleados en la tabla de employees:
--Asigna dos empleados al departamento de engineering:
UPDATE employees SET departments_id =1 WHERE id=6;
UPDATE employees SET departments_id=1 WHERE id=8;

--Asigna a un empleado al departamento de marketing:
UPDATE employees SET departments_id=2 WHERE id=10;

--Realiza una consulta que muestre todos los empleados junto con el nombre de su departamento. 

SELECT e.id AS employee_id,
       e.first_name AS employee_name,
       d.name AS department_name
FROM employees e
LEFT JOIN departments d
ON e.departments_id = d.id;

--------------------CLASE 3
-------EJERCICIO 1:
--Inserta 1 departamento:
INSERT INTO departments(name)
VALUES ('RRHH');
--Muestra todos los departamentos:
SELECT * FROM DEPARTMENTS;
--Inserta un empleado con departamento:
UPDATE employees SET departments_id=3 WHERE id=20;
--Muestra todos los empleados:
SELECT*FROM employees;
--Muestra todos los empleados junto con el nombre del departamento al que pertenecen:
SELECT e.id AS employee_id,
       e.first_name AS employee_name,
       d.name AS department_name
FROM employees e
LEFT JOIN departments d
ON e.departments_id = d.id;