CREATE TABLE IF NOT EXISTS employees (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date   DATE NOT NULL,
    first_name    VARCHAR(50) NOT NULL,
    last_name      VARCHAR(100) NOT NULL,       
    register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
    );
DROP TABLE employees;        --- BORRA LA TABLA EMPLOYEES SI EXISTE
-- cada vez que quieras crear una nueva tabla necesitas borrar la anterior con "DROP TABLE"

-- AGREGA LAS NUEVAS COLUMNAS A LA TABLA EMPLOYEES
-- Se comprueba que las columnas no existen antes de agregarlas
-- Esto es útil para evitar errores si el script se ejecuta múltiples veces
-- Se comprueba de una en una para mayor claridad con el fin de facilitar el mantenimiento futuro, CONTROL + SHIFT + ENTER.  ACCESS
-- CONTROL + SHIFT + ENTER.
-- CONTROL + SHIFT + ENTER.
-- VAS DE UNO EN UNO -------> 

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
AlTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

-- Inserta al menos 15 empleados nuevos en la tabla employees, que cumplan los siguientes criterios: 
-- Al menos 3 empleados deben tener el mismo nombre.
-- Los salarios deben variar entre 5000 y 50.000.
-- Todos los empleados deben tener un título.
-- Al menos 5 empleados deben tener title_date del año 2020.
-- Selecciona todos tus empleados
-- Selecciona todos tus empleados mostrando solamente el first_name y salary

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) 
VALUES  ('1985-01-15', 'John', 'Doe', 6000.00, 'Software Engineer', '2020-03-15'),
('1990-06-22', 'Jane', 'Smith', 7500.00, 'Data Analyst', '2019-11-20'),
('1988-09-10', 'John', 'Brown', 12000.00, 'Project Manager', '2021-01-05'),
('1975-12-30', 'Emily', 'Davis', 45000.00, 'Senior Developer', '2020-07-18'),
('1992-04-14', 'Michael', 'Wilson', 30000.00, 'UX Designer', '2020-02-25'),
('1983-11-05', 'Sarah', 'Johnson', 5200.00, 'QA Engineer', '2018-09-30'),
('1995-08-19', 'David', 'Lee', 15000.00, 'DevOps Engineer', '2020-12-12'),
('1987-03-03', 'John', 'Garcia', 8000.00, 'Business Analyst', '2019-05-22'),
('1991-10-28', 'Laura', 'Martinez', 27000.00, 'Marketing Specialist', '2021-04-10'),
('1984-07-16', 'James', 'Rodriguez', 35000.00, 'Sales Manager', '2020-09-14'),
('1979-02-11', 'Linda', 'Hernandez', 40000.00, 'HR Manager', '2017-06-01'),
('1993-05-25', 'Robert', 'Lopez', 22000.00, 'Content Writer', '2020-11-30'),
('1986-12-08', 'Patricia', 'Gonzalez', 28000.00, 'Graphic Designer', '2019-08-19'),
('1994-09-17', 'Charles', 'Wilson', 5000.00, 'Intern', '2020-01-15'),
('1982-04-02', 'Barbara', 'Anderson', 48000.00, 'Product Manager', '2021-03-08');

SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary >=20000;
SELECT * FROM employees WHERE salary <=10000;

UPDATE employees SET first_name = 'Alexandra' WHERE id = 7;

DELETE FROM employees WHERE id = 5;

DELETE FROM employees WHERE salary <= 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;


SELECT first_name || ' ' || last_name AS name FROM employees; -- || Son para separar || ACUERDATE QUE VAS CON COMILLAS SIMPLES ' ' SQL

SELECT * FROM employees WHERE firts_name LIKE '%a%';

--Practicas

SELECT DISTINCT first_name FROM employees; 

SELECT * FROM employees WHERE first_name LIKE 'P%';

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

SELECT * FROM employees WHERE last_name NOT LIKE '%a%';

SELECT salary, COUNT(salary) FROM employees GROUP BY salary;

--Practicas avanzadas

--Muestra el número total de empleados
--Muestra el empleado con el salario más alto


--EXTRA:
--Muestra el salario medio por titulo
--Muestra el salario máximo y mínimo por título


SELECT COUNT(id) FROM employees;
SELECT COUNT(*) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) AS salario_medio FROM employees GROUP BY title;
SELECT title, MAX(salary) AS salario_maximo, MIN(salary) AS salario_minimo FROM employees GROUP BY title;

--Extra practica en clase

SELECT first_name, salary, salary+5000 AS Salario_en_5_años 
FROM employees;

SELECT first_name, salary,
        salary * 0.12 AS ahorro_mensual,
        ROUND((salary * 0.12)*3, 2) AS total_ahorrado_en_3_meses_redondeado
FROM employees;

-- Practicas finales -- 

SELECT first_name, salary, 
        ROUND((salary),2)
FROM employees;

SELECT first_name, salary,
        salary *1.21 AS salario_neto,
        salary *0.21 AS impuesto,
        ROUND(salary *1.21,2) AS salario_neto_redondeado
FROM employees;








