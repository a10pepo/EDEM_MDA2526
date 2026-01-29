CREATE DATABASE myFirstDB;

CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE
);
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE DEFAULT now();

INSERT INTO employees (first_name, last_name, birth_date) 
VALUES ('German','Devis','2002-12-17');


SELECT * FROM employees;

INSERT INTO employees (first_name, last_name, birth_date) 
VALUES 
('Ana', 'Torres', '1995-03-15'),
('Luis', 'García', '1988-11-20'),
('María', 'Rodríguez', '1992-07-01'),
('David', 'Martínez', '1979-05-10'),
('Laura', 'Sánchez', '2000-01-30'),
('Carlos', 'Pérez', '1998-09-05'),
('Sofía', 'Gómez', '1985-04-22'),
('Javier', 'Fernández', '1991-06-12'),
('Carmen', 'Ruiz', '1975-10-08'),
('Miguel', 'López', '2001-02-19'),
('Elena', 'Díaz', '1993-08-25'),
('Pablo', 'Moreno', '1982-12-03'),
('Lucía', 'Álvarez', '1997-07-14'),
('Jorge', 'Romero', '1990-11-28');



UPDATE employees SET salary = 45000.50, title = 'Senior Developer', title_date = '2020-05-15' 
WHERE first_name = 'German' AND last_name = 'Devis';

UPDATE employees SET salary = 32000.00, title = 'Project Manager', title_date = '2021-02-10' 
WHERE first_name = 'Ana' AND last_name = 'Torres';

UPDATE employees SET salary = 48000.00, title = 'Data Scientist', title_date = '2020-05-20' 
WHERE first_name = 'Luis' AND last_name = 'García';

UPDATE employees SET salary = 28000.75, title = 'UX/UI Designer', title_date = '2022-11-01' 
WHERE first_name = 'María' AND last_name = 'Rodríguez';

UPDATE employees SET salary = 49500.00, title = 'Sales Manager', title_date = '2020-06-01' 
WHERE first_name = 'David' AND last_name = 'Martínez';

UPDATE employees SET salary = 24000.00, title = 'Junior Developer', title_date = '2023-06-30' 
WHERE first_name = 'Laura' AND last_name = 'Sánchez';

UPDATE employees SET salary = 26500.00, title = 'Marketing Specialist', title_date = '2022-09-05' 
WHERE first_name = 'Carlos' AND last_name = 'Pérez';

UPDATE employees SET salary = 31000.00, title = 'HR Specialist', title_date = '2020-10-10' 
WHERE first_name = 'Sofía' AND last_name = 'Gómez';

UPDATE employees SET salary = 42000.00, title = 'Senior Developer', title_date = '2021-07-19' 
WHERE first_name = 'Javier' AND last_name = 'Fernández';

UPDATE employees SET salary = 38000.00, title = 'Business Analyst', title_date = '2020-08-01' 
WHERE first_name = 'Carmen' AND last_name = 'Ruiz';

UPDATE employees SET salary = 25000.00, title = 'Junior Developer', title_date = '2023-01-20' 
WHERE first_name = 'Miguel' AND last_name = 'López';

UPDATE employees SET salary = 33000.00, title = 'UX/UI Designer', title_date = '2022-04-14' 
WHERE first_name = 'Elena' AND last_name = 'Díaz';

UPDATE employees SET salary = 47000.00, title = 'Project Manager', title_date = '2021-03-05' 
WHERE first_name = 'Pablo' AND last_name = 'Moreno';

UPDATE employees SET salary = 29000.00, title = 'Marketing Specialist', title_date = '2023-10-01' 
WHERE first_name = 'Lucía' AND last_name = 'Álvarez';

UPDATE employees SET salary = 43000.00, title = 'Data Scientist', title_date = '2021-11-28' 
WHERE first_name = 'Jorge' AND last_name = 'Romero';

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;
SELECT * FROM employees;



UPDATE employees SET first_name = 'Eustaquio' WHERE id = 7;
DELETE FROM employees WHERE salary > 48000;
SELECT * FROM employees WHERE salary BETWEEN 24000 AND 30000;
SELECT * FROM employees ORDER BY id ASC;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id= 9;


SELECT * FROM employees WHERE first_name LIKE 'P%';

SELECT * FROM employees WHERE first_name LIKE 'G%';
SELECT * FROM employees WHERE first_name LIKE '%a%';


-- ESTA FÓRMULA SE USA MUCHO
-- SELECT age, COUNT(age) FROM users GROUP BY age;

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, salary,
    ROUND(salary, 2)
FROM employees;


SELECT first_name, salary,
    ROUND(salary - (salary*0.21), 2) AS salario_neto
FROM employees; 

SELECT * FROM employees;

CREATE TABLE departments (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    -- employees_id INTEGER NOT NULL REFERENCES employees(id),
    descript TEXT,
    aditional_info VARCHAR(1000));

INSERT INTO departments (dept_name, descript, aditional_info)
VALUES ('Engineering','Engineers work here','blablablabla');


INSERT INTO departments (dept_name, descript, aditional_info)
VALUES ('Marketing','Weird people tend to work here','bliblibli');

ALTER TABLE departments DROP COLUMN employees_id;

SELECT * FROM departments;

-- INSERT INTO departments (dept_name, descript, aditional_info)
-- VALUES ('Data','I want to work here!','blublublu');


ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);
-- ALTER TABLE employees DROP COLUMN departments_id;



SELECT * FROM employees;

UPDATE employees SET departments_id = 4
WHERE first_name = 'Carmen' AND last_name = 'Ruiz';

UPDATE employees SET departments_id = 4
WHERE first_name = 'Laura' AND last_name = 'Sánchez';

UPDATE employees SET departments_id = 5
WHERE first_name = 'German' AND last_name = 'Devis';

SELECT employees.first_name, employees.last_name, departments.dept_name
FROM employees
INNER JOIN departments
ON employees.departments_id = departments.id;




