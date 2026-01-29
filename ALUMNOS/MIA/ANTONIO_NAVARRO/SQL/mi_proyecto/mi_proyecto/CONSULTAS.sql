CREATE TABLE IF NOT EXISTS employees (
  id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name      VARCHAR(100) NOT NULL,
  last_name       VARCHAR(100) NOT NULL,
  birth_date      DATE               
);

ALTER TABLE employees ADD COLUMN salary NUMERIC (10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR (100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
VALUES 
('Luffy', 'Monkey D.', '2003-11-23', 40000.59, 'Telecommunications engineer', '2024-07-25'),
('Zoro', 'Roronoa', '2001-11-11', 38000.00, 'Network administrator', '2024-05-12'),
('Nami', 'Cat Burglar', '2002-07-03', 42000.75, 'Data analyst', '2024-03-15'),
('Usopp', 'Sniper King', '2001-04-01', 37000.20, 'Support technician', '2024-06-10'),
('Sanji', 'Vinsmoke', '2000-03-02', 45000.00, 'Software developer', '2021-08-01'),
('Chopper', 'Tony Tony', '2006-12-24', 31000.50, 'Medical technician', '2020-09-05'),
('Robin', 'Nico', '1998-02-06', 42000.00, 'Data scientist', '2020-02-18'),
('Franky', 'Cyborg', '1995-03-09', 48000.25, 'Mechanical engineer', '2024-04-10'),
('Luffy', 'Soul King', '1988-04-03', 43000.90, 'Musical engineer', '2022-05-20'),
('Jinbe', 'Knight of the Sea', '1985-08-30', 54000.10, 'Marine biologist', '2024-07-10'),
('Shanks', 'Red Hair', '1983-03-09', 60000.00, 'Project manager', '2020-01-01'),
('Luffy', 'The Clown', '1989-09-17', 5000.75, 'Logistics coordinator', '2024-04-22'),
('Law', 'Trafalgar D.', '1996-10-06', 50000.40, 'Surgeon', '2020-03-12'),
('Kidd', 'Eustass', '1997-01-15', 7000.80, 'Mechanical designer', '2024-06-25'),
('Yamato', 'Kaido Jr.', '2002-09-29', 49000.30, 'Systems analyst', '2023-07-19');

-- TRUNCATE employees;

SELECT * FROM employees;
SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 77;
SELECT * FROM employees WHERE salary > 20000;
SELECT * FROM employees WHERE salary <= 10000;

UPDATE employees SET first_name = 'Messi' where id = 82;
DELETE FROM employees WHERE id=90;
DELETE FROM employees WHERE salary > 48000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;
SELECT first_name || ' ' || last_name AS name FROM employees;

SELECT * FROM employees WHERE first_name LIKE 'K%';
SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;
SELECT * FROM employees ORDER BY salary DESC LIMIT 1;

SELECT first_name, ROUND(salary,2) FROM employees;


----------------------------EXTRA---------------------------------------

SELECT first_name , salary*(0.79) AS salario_neto FROM employees;
------------------------------------------------------------------------
SELECT 
    first_name,
    salary,
    ROUND(salary * 0.21, 2) AS impuestos,
    ROUND(salary - (salary * 0.21), 2) AS salario_neto
FROM employees;
------------------------------------------------------------------------

CREATE TABLE departments (
    department_id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name    VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN department_id INTEGER;

INSERT INTO departments (name)
VALUES 
('Marketing'),
('Engineering');

SELECT * FROM DEPARTMENTS;
SELECT * FROM EMPLOYEES;

UPDATE employees SET department_id= 2 where id = 20 ;
UPDATE employees SET department_id= 2 where id = 27 ;
UPDATE employees SET department_id= 1 where id = 17 ;

SELECT employees.first_name, departments.name FROM employees LEFT JOIN departments ON employees.department_id = departments.department_id;

----------------EXTRA---------------------
INSERT INTO departments (name)
VALUES 
('Marketing'),
('Engineering'),
('Sales'),
('HR'),
('R&D'),
('Legal');

DELETE FROM departments WHERE department_id=3;
DELETE FROM departments WHERE department_id=4;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date, department_id)
VALUES 
('Luffy', 'Monkey D.', '2003-11-23', 40000.59, 'Telecommunications engineer', '2024-07-25', 2),
('Zoro', 'Roronoa', '2001-11-11', 38000.00, 'Network administrator', '2024-05-12',2),
('Nami', 'Cat Burglar', '2002-07-03', 42000.75, 'Data analyst', '2024-03-15',2),
('Usopp', 'Sniper King', '2001-04-01', 37000.20, 'Support technician', '2024-06-10',2),
('Sanji', 'Vinsmoke', '2000-03-02', 45000.00, 'Software developer', '2021-08-01',1),
('Chopper', 'Tony Tony', '2006-12-24', 31000.50, 'Medical technician', '2020-09-05',1),
('Robin', 'Nico', '1998-02-06', 42000.00, 'Data scientist', '2020-02-18',1),
('Franky', 'Cyborg', '1995-03-09', 48000.25, 'Mechanical engineer', '2024-04-10',5),
('Luffy', 'Soul King', '1988-04-03', 43000.90, 'Musical engineer', '2022-05-20',5),
('Jinbe', 'Knight of the Sea', '1985-08-30', 54000.10, 'Marine biologist', '2024-07-10',6),
('Shanks', 'Red Hair', '1983-03-09', 60000.00, 'Project manager', '2020-01-01',7);

SELECT employees.first_name, departments.name FROM employees INNER JOIN departments ON employees.department_id = departments.department_id;

SELECT departments.name FROM departments LEFT JOIN employees ON employees.department_id = departments.department_id WHERE employees.department_id IS NULL;

SELECT departments.name, COUNT(employees.id) AS nºempleados FROM departments INNER JOIN employees ON employees.department_id = departments.department_id GROUP BY departments.name;

SELECT departments.name, COUNT(employees.id) AS nºempleados FROM departments 
INNER JOIN employees ON employees.department_id = departments.department_id 
WHERE departments.name = 'Engineering' GROUP BY departments.name;

SELECT departments.name, ROUND(AVG(employees.salary),2) AS media_salario FROM departments 
INNER JOIN employees ON employees.department_id = departments.department_id GROUP BY departments.name;

SELECT departments.name, MAX(employees.salary) AS maxim FROM departments 
INNER JOIN employees ON employees.department_id = departments.department_id WHERE departments.name IN 
(SELECT departments.name FROM departments) GROUP BY departments.name ORDER BY maxim DESC;


---------------------------------------------------
-- Table employees {
--   id integer [primary key]
--   first_name varchar
--   last_name varchar
--   birth_date timestamp
--   salary float
--   title varchar
--   title_date timestamp
--   department_id integer
-- }

-- Table departments {
--   id integer [primary key]
--   name varchar
-- }

-- Ref dep_employees: employees.department_id > departments.id // many-to-one

---------------------------------------------------------------------

INSERT INTO departments (name)
VALUES 
('RRHH');

SELECT departments.department_id,departments.name FROM departments;

INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date, department_id)
VALUES 
('Cristiano', 'Ronaldo', '1985-11-23', 70000.59, 'Futbolista', '2024-07-25', 7);

SELECT * FROM employees;

SELECT employees.first_name, employees.last_name, departments.name FROM employees INNER JOIN departments ON employees.department_id = departments.department_id;
SELECT employees.first_name, employees.last_name, departments.name FROM employees LEFT JOIN departments ON employees.department_id = departments.department_id;