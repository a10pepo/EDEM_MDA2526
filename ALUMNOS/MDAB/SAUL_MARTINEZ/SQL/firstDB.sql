CREATE TABLE IF NOT EXISTS employees (
 id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 first_name   VARCHAR(100) NOT NULL,
 last_name    VARCHAR(100) NOT NULL,
 birth_date DATE, -- SE PUEDE USAR TO_DATE() PARA METER DÍA MES Y AÑO, SINO TIENE QUE SER AL REVÉS
 password  TEXT NOT NULL,        
 register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
);
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;
ALTER TABLE employees DROP COLUMN password;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
VALUES 
('Ada','Lovelace','2001-12-01',1000,'Matemática','2025-10-24'),
('Alan','Turing','1998-06-23',1200,'Criptógrafo','2025-10-24'),
('Grace','Hopper','1995-12-09',1350,'Programadora','2025-10-24'),
('Katherine','Johnson','1992-08-26',1400,'Analista de Datos','2025-10-24'),
('John','von Neumann','1990-12-28',1500,'Matemático','2025-10-24'),
('Barbara','Liskov','1988-11-07',1600,'Ingeniera de Software','2025-10-24'),
('Edsger','Dijkstra','1985-05-11',1550,'Arquitecto de Sistemas','2025-10-24'),
('Donald','Knuth','1987-01-10',1700,'Investigador','2025-10-24'),
('Margaret','Hamilton','1991-08-17',1450,'Líder de Proyecto','2025-10-24'),
('Tim','Berners-Lee','1994-06-08',1650,'Ingeniero Web','2025-10-24'),
('Linus','Torvalds','1996-12-28',1750,'Desarrollador de Sistemas','2025-10-24'),
('Sheryl','Sandberg','1993-04-28',1300,'Gerente de Producto','2025-10-24'),
('Elon','Musk','1989-06-28',1800,'Innovador','2025-10-24'),
('Steve','Wozniak','1984-08-11',1600,'Ingeniero Electrónico','2025-10-24'),
('Hedy','Lamarr','1997-11-09',1500,'Inventora','2025-10-24');

SELECT * FROM employees WHERE id NOT IN (
  SELECT MIN(id)
  FROM employees
  WHERE first_name = 'Ada' AND last_name = 'Lovelace'
);

SELECT * FROM employees WHERE id=17;
SELECT * FROM employees WHERE salary>2000;
SELECT * FROM employees WHERE salary<=1000;
DELETE FROM employees WHERE id = 17;
SELECT * FROM employees;

UPDATE employees SET first_name='Adeline' WHERE id = 17;
UPDATE employees SET first_name='Alana' WHERE id = 18;
DELETE FROM employees WHERE id=1;
DELETE FROM employees WHERE salary>=1800;
SELECT * FROM employees WHERE salary BETWEEN 1000 AND 1500;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=22;
SELECT * FROM employees WHERE first_name LIKE 'G%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

-- SELECT age, COUNT (age) FROM employees GROUP BY age; MUY ÚTIL

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;
SELECT AVG(salary) FROM employees;
SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, salary,
  salary * 0.5772615 AS bajada_salarios,
  ROUND((salary*0.5772615), 2) AS nomina_bruta
FROM employees;

SELECT first_name, salary,
  salary * 0.21 AS impuestos,
  ROUND((salary*0.5772615*0.79), 2) AS nomina_neta
FROM employees;

ALTER TABLE employees
ADD COLUMN age VARCHAR(3);
ALTER TABLE employees
 ALTER COLUMN age TYPE INTEGER USING age::integer;

UPDATE employees
SET age = CASE id
    WHEN 1 THEN 41
    WHEN 2 THEN 85
    WHEN 3 THEN 86
    WHEN 4 THEN 66
    WHEN 5 THEN 76
    WHEN 6 THEN 101
    WHEN 7 THEN 79
    WHEN 8 THEN 37
    WHEN 9 THEN 84
    WHEN 10 THEN 77
    WHEN 11 THEN 76
    WHEN 12 THEN 88
    WHEN 13 THEN 70
    WHEN 14 THEN 70
    WHEN 15 THEN 102
END;
SELECT * FROM employees WHERE age BETWEEN 18 AND 99;
SELECT * FROM employees WHERE age<=18 OR age>=100;

SELECT * FROM employees;

CREATE TABLE IF NOT EXISTS departments
 (
 id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 department_name   VARCHAR(100) NOT NULL,       
 register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO departments (department_name)
VALUES ('Engineering'),
('Marketing');

SELECT * FROM departments;
ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

UPDATE employees SET departments_id = 1 WHERE id=1;
UPDATE employees 
SET departments_id = 2 WHERE id BETWEEN 2 AND 10;
UPDATE employees 
SET departments_id = 3 WHERE id BETWEEN 11 AND 15;

SELECT 
  employees.first_name, 
  employees.last_name, 
  departments.department_name
FROM employees 
INNER JOIN departments 
  ON employees.departments_id = departments.id;
-- Solo devuelve las filas que coinciden en ambas tablas

SELECT 
  e.first_name, 
  e.last_name, 
  d.department_name
FROM employees e
LEFT JOIN departments d 
ON e.departments_id = d.id;
--El LEFT JOIN devuelve todas las filas de la tabla izquierda (employees),
--aunque no haya coincidencia en la tabla derecha (departments).