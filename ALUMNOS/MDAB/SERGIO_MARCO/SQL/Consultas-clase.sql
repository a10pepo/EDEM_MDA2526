CREATE DATABASE IF NOT EXISTS myFirstDB;
CREATE TABLE IF NOT EXISTS employees (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    birth_date      DATE,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL
);
ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES('2025/09/25','Sergio','Marco',100000,'data engineer','2000/01/01');

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES 
('1990-04-12', 'Sergio', 'López', 45000, 'backend developer', '2020-03-15'),
('1988-07-23', 'Sergio', 'García', 32000, 'frontend developer', '2020-06-01'),
('1992-11-05', 'Laura', 'Martínez', 28000, 'QA analyst', '2020-09-10'),
('1985-03-19', 'Carlos', 'Ruiz', 50000, 'system administrator', '2019-12-01'),
('1993-01-30', 'Ana', 'Torres', 47000, 'UX designer', '2020-02-20'),
('1991-06-17', 'David', 'Fernández', 39000, 'DevOps engineer', '2020-07-07'),
('1989-09-08', 'Lucía', 'Sánchez', 41000, 'cloud architect', '2018-05-01'),
('1994-12-25', 'Pablo', 'Navarro', 36000, 'support technician', '2021-01-01'),
('1995-05-14', 'Isabel', 'Moreno', 33000, 'security analyst', '2020-11-30'),
('1987-08-02', 'Raúl', 'Domínguez', 49000, 'database administrator', '2017-06-15'),
('1996-02-28', 'Patricia', 'Vargas', 27000, 'technical writer', '2022-03-01'),
('1990-10-10', 'Alberto', 'Ortega', 35000, 'network engineer', '2016-10-10'),
('1992-03-03', 'Marta', 'Castro', 42000, 'software developer', '2020-04-22'),
('1986-12-11', 'Javier', 'Gómez', 48000, 'IT manager', '2015-08-01');

SELECT * FROM employees WHERE id=2;
SELECT * FROM employees WHERE salary>20000;
SELECT * FROM employees WHERE salary<=10000;

SELECT first_name, salary FROM employees WHERE birth_date >

UPDATE employees SET first_name = 'Pepito' WHERE id = 7;
SELECT * FROM employees WHERE id=7;

DELETE FROM employees WHERE id = 5;
SELECT * FROM employees WHERE id=5;

DELETE FROM employees WHERE salary>20000;
SELECT * FROM employees;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
VALUES
('1990-01-01', 'Luis', 'Gómez', 0, 'intern', '2023-01-01'),
('1985-02-02', 'Ana', 'Martínez', 2000, 'junior developer', '2022-06-15'),
('1992-03-03', 'Carlos', 'Ruiz', 5000, 'support technician', '2021-09-10'),
('1988-04-04', 'Lucía', 'Torres', 8000, 'QA analyst', '2020-03-20'),
('1995-05-05', 'David', 'Fernández', 10000, 'frontend developer', '2020-07-01'),
('1983-06-06', 'Marta', 'Sánchez', 12000, 'backend developer', '2019-11-11'),
('1991-07-07', 'Pablo', 'Castro', 15000, 'DevOps engineer', '2020-01-01'),
('1986-08-08', 'Isabel', 'Ruiz', 18000, 'system administrator', '2020-05-05'),
('1993-09-09', 'Raúl', 'Domínguez', 20000, 'network engineer', '2018-08-08'),
('1989-10-10', 'Patricia', 'Navarro', 22000, 'cloud architect', '2021-02-02'),
('1994-11-11', 'Alberto', 'Ortega', 25000, 'security analyst', '2022-03-03'),
('1987-12-12', 'Javier', 'Gómez', 27000, 'database administrator', '2020-09-09'),
('1996-01-13', 'Sergio', 'Marco', 30000, 'data engineer', '2020-01-01'),
('1990-02-14', 'Sergio', 'López', 32000, 'data engineer', '2020-06-06'),
('1985-03-15', 'Sergio', 'García', 35000, 'data engineer', '2020-12-12'),
('1992-04-16', 'Laura', 'Martínez', 37000, 'UX designer', '2019-04-04'),
('1988-05-17', 'Carlos', 'Ramírez', 40000, 'technical writer', '2021-07-07'),
('1995-06-18', 'Ana', 'Vargas', 42000, 'software developer', '2020-10-10'),
('1983-07-19', 'Lucía', 'Moreno', 45000, 'IT manager', '2017-05-05'),
('1991-08-20', 'David', 'Santos', 47000, 'project manager', '2016-06-06'),
('1986-09-21', 'Marta', 'Rojas', 50000, 'product owner', '2015-03-03'),
('1993-10-22', 'Pablo', 'León', 52000, 'team lead', '2014-02-02'),
('1989-11-23', 'Isabel', 'Cano', 55000, 'scrum master', '2013-01-01'),
('1994-12-24', 'Raúl', 'Peña', 58000, 'release manager', '2012-12-12'),
('1987-01-25', 'Patricia', 'Gil', 60000, 'test lead', '2011-11-11'),
('1996-02-26', 'Alberto', 'Molina', 62000, 'site reliability engineer', '2010-10-10'),
('1990-03-27', 'Javier', 'Núñez', 65000, 'platform engineer', '2009-09-09'),
('1985-04-28', 'Luis', 'Gómez', 67000, 'data scientist', '2008-08-08'),
('1992-05-29', 'Ana', 'Martínez', 70000, 'ML engineer', '2007-07-07'),
('1988-06-30', 'Carlos', 'Ruiz', 72000, 'AI researcher', '2006-06-06'),
('1995-07-31', 'Lucía', 'Torres', 75000, 'NLP specialist', '2005-05-05'),
('1983-08-01', 'David', 'Fernández', 77000, 'vision engineer', '2004-04-04'),
('1991-09-02', 'Marta', 'Sánchez', 80000, 'robotics engineer', '2003-03-03'),
('1986-10-03', 'Pablo', 'Castro', 82000, 'embedded systems engineer', '2002-02-02'),
('1993-11-04', 'Isabel', 'Ruiz', 85000, 'hardware engineer', '2001-01-01'),
('1989-12-05', 'Raúl', 'Domínguez', 87000, 'firmware engineer', '2000-12-12'),
('1994-01-06', 'Patricia', 'Navarro', 90000, 'network architect', '2000-11-11'),
('1987-02-07', 'Alberto', 'Ortega', 92000, 'enterprise architect', '2000-10-10'),
('1996-03-08', 'Javier', 'Gómez', 95000, 'solutions architect', '2000-09-09'),
('1990-04-09', 'Sergio', 'Marco', 97000, 'data engineer', '2000-08-08'),
('1985-05-10', 'Sergio', 'Marco', 99000, 'data engineer', '2000-07-07'),
('1992-06-11', 'Laura', 'Martínez', 100000, 'chief data officer', '2000-06-06'),
('1988-07-12', 'Carlos', 'Ramírez', 98000, 'CTO', '2000-05-05'),
('1995-08-13', 'Ana', 'Vargas', 96000, 'CIO', '2000-04-04'),
('1983-09-14', 'Lucía', 'Moreno', 94000, 'CEO', '2000-03-03'),
('1991-10-15', 'David', 'Santos', 92000, 'COO', '2000-02-02'),
('1986-11-16', 'Marta', 'Rojas', 90000, 'CFO', '2000-01-01'),
('1993-12-17', 'Pablo', 'León', 88000, 'VP Engineering', '1999-12-12'),
('1989-01-18', 'Isabel', 'Cano', 86000, 'VP Product', '1999-11-11'),
('1994-02-19', 'Raúl', 'Peña', 84000, 'VP Operations', '1999-10-10');

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date ASC;
SELECT * FROM employees;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS name FROM employees WHERE id =50;

SELECT * FROM employees WHERE first_name LIKE 'p%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT * FROM employees WHERE birth_date > '1991-10-15';

SELECT COUNT(id) FROM employees;
SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) FROM employees GROUP BY title;

SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;

SELECT first_name, ROUND(salary,2) AS salary_rounded FROM employees;


CREATE TABLE IF NOT EXISTS departments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    name            VARCHAR(100)
);

INSERT INTO departments (name)
VALUES
('Engineering'),
('Marketing');

SELECT * FROM departments;

ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

UPDATE employees SET departments_id = 2 WHERE id in (16,17,18);

SELECT * FROM employees;

SELECT employees.first_name, employees.last_name, departments.name
FROM employees
INNER JOIN departments
ON departments.id = employees.departments_id;

DROP DATABASE postgres;