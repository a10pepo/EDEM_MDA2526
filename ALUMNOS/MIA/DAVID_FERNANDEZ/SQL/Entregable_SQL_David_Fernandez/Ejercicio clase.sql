--EJERCICIO PRACTICA --

CREATE TABLE IF NOT EXISTS employees (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    birth_day    DATE NOT NULL,
    first_name   TEXT NOT NULL,
    last_name    TEXT NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;


INSERT INTO employees (birth_day, first_name, last_name, salary, title, title_date)
VALUES ('1979-07-09', 'David', 'Fernandez', 30000, 'Revenue Manager', '2015-07-12'),
('1985-08-25', 'Juan', 'Perez', 15000, 'Technician', '2019-01-10'),
('1995-03-12', 'Ana', 'Rodriguez', 5000, 'Intern', '2020-01-05'),
('1978-06-30', 'Carlos', 'Sanchez', 5000, 'Project Manager', '2022-04-20'),
('1990-09-01', 'Sofia', 'Hernandez', 25000, 'HR Specialist', '2020-10-25'),
('1983-04-18', 'Pedro', 'Gomez', 35000, 'Developer', '2021-05-10'),
('1998-12-05', 'Elena', 'Diaz', 12000, 'Junior Analyst', '2020-12-01'),
('1970-02-28', 'Luis', 'Ruiz', 49000, 'CEO', '2018-07-01'),
('1988-10-10', 'Marta', 'Vazquez', 22000, 'Sales Representative', '2023-02-14'),
('1993-07-07', 'David', 'Morales', 8000, 'Maintenance Staff', '2020-08-01'),
('1973-03-21', 'Laura', 'Gil', 40000, 'Team Lead', '2017-11-22'),
('1996-01-01', 'Raul', 'Vega', 30000, 'Marketing Assistant', '2022-09-05'),
('1980-05-15', 'Maria', 'Lopez', 45000, 'Senior Engineer', '2020-03-01'),
('1992-11-20', 'Maria', 'Garcia', 32000, 'Analyst', '2020-06-15'),
('1975-01-10', 'Maria', 'Martinez', 50000, 'Director', '2021-09-01'),
('1981-11-11', 'Patricia', 'Reyes', 28000, 'Recruiter', '2021-03-30');

SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2; 
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Antonio' WHERE id = 7;
DELETE FROM employees WHERE id = 5;
DELETE FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_day ASC;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9;
SELECT DISTINCT first_name FROM employees;

SELECT * FROM employees WHERE first_name LIKE 'P%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT first_name, ROUND (salary,2) FROM employees;

--EJERCICIO PRACTICA --


CREATE TABLE IF NOT EXISTS departments (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
first_name VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN department_id BIGINT;

INSERT INTO departments(first_name) VALUES ('Enginering');
INSERT INTO departments(first_name) VALUES ('Marketing');
SELECT * FROM employees;
UPDATE employees set salary = 5 where id = 1;
UPDATE employees set tittle = 'Traedor de cafes' where id = 1;
UPDATE employees set salary = 500000 where id = 13;
SELECT * FROM departments;

UPDATE employees
SET department_id = CASE
    WHEN id IN (1,10) THEN 1
    WHEN id IN (7, 13) THEN 2
END
WHERE id IN (1, 7, 10, 13);
SELECT employees.first_name, departments.first_name FROM employees INNER JOIN departments ON employees.department_id=departments.id;

--EJERCICIO PRACTICA --

INSERT INTO departments (first_name) VALUES ('RRHH');
SELECT * FROM departments;
INSERT INTO employees (first_name, last_name, birth_day, department_id) VALUES ('Pedro','Peruga','2020-01-05',2);
SELECT * FROM  employees;
SELECT employees.first_name,departments.first_name FROM employees INNER JOIN departments ON employees.department_id = departments.id;


