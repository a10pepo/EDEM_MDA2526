-- CREATE TABLE IF NOT EXISTS employees (
--     id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     birth_date      DATE,
--     first_name      VARCHAR(100) NOT NULL,
--     last_name       VARCHAR(100) NOT NULL                            
-- );

-- ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
-- ALTER TABLE employees ADD COLUMN title VARCHAR (100);
-- ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES ('2000-08-15','Jorge','Martinez Martinez',50000,'Ingeneria aeroespacial','2020-03-14'),
('1990-03-15', 'Carlos', 'Ramirez', 12000, 'Engineer', '2020-01-10'),
('1988-07-22', 'Carlos', 'Santos', 18000, 'Senior Engineer', '2020-03-05'),
('1992-11-30', 'Carlos', 'Gomez', 11000, 'Engineer', '2021-09-22'),
('1991-05-17', 'Lucia', 'Perez', 32000, 'Manager', '2020-02-17'),
('1994-08-10', 'Lucia', 'Fernandez', 14000, 'Engineer', '2020-05-14'),
('1993-12-05', 'Lucia', 'Mendoza', 27000, 'Senior Engineer', '2022-11-30'),
('1989-04-09', 'Javier', 'Lopez', 15000, 'Engineer', '2020-01-09'),
('1995-09-18', 'Javier', 'Martinez', 8000, 'Assistant Engineer', '2021-07-18'),
('1990-01-25', 'Sofia', 'Diaz', 25000, 'Senior Engineer', '2020-08-05'),
('1992-02-14', 'Sofia', 'Blanco', 17000, 'Engineer', '2023-04-22'),
('1987-10-30', 'Diego', 'Castro', 45000, 'Manager', '2020-09-10'),
('1994-06-16', 'Elena', 'Ruiz', 9000, 'Engineer', '2024-03-16'),
('1995-03-01', 'Elena', 'Rojas', 7000, 'Assistant Engineer', '2020-06-01'),
('1991-12-22', 'Elena', 'Mora', 22000, 'Senior Engineer', '2021-02-10'),
('1989-09-11', 'Martin', 'Silva', 19500, 'Engineer', '2020-12-11');

SELECT * FROM employees;

SELECT first_name, salary
FROM employees;

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET first_name='Clara' WHERE id=7;
DELETE FROM employees WHERE id=5;
DELETE FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT *FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name  || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

SELECT * FROM employees WHERE first_name LIKE '%p';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT first_name, ROUND(salary, 2) FROM employees;

CREATE TABLE departments (
    id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);


ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

INSERT INTO departments (name) VALUES
('Engineering'),
('Marketing');

UPDATE employees SET departments_id = 1 WHERE id = 30;
UPDATE employees SET departments_id = 1 WHERE id = 14;
UPDATE employees SET departments_id = 2 WHERE id = 9;

SELECT
employees.first_name,
departments.name AS departments_name
FROM employees
RIGHT JOIN departments ON employees.departments_id = departments.id;

SELECT * FROM employees
SELECT * FROM departments
