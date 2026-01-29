CREATE TABLE IF NOT EXISTS employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR(100);
ALTER TABLE employees ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, title, title_date, salary) 
VALUES
('1995-03-14','Raúl','Santos','Junior Engineer','2020-02-10',28000),
('1992-07-22','Raúl','Gómez','Data Analyst','2020-05-18',31000),
('1990-01-09','Raúl','López','Project Engineer','2019-09-01',36000),
('1988-11-03','Ana','Pérez','Senior Engineer','2020-03-01',45000),
('1996-04-28','María','Ruiz','HR Specialist','2021-07-10',27000),
('1993-09-17','Carlos','Díaz','QA Engineer','2020-11-20',26000),
('2000-02-02','Lucía','Martín','Intern','2020-07-01',5000),
('1989-06-12','Javier','Torres','DevOps Engineer','2018-04-15',18000),
('1991-12-21','Sofía','Navarro','Product Manager','2020-01-20',19000),
('1994-08-30','Pablo','Romero','Finance Analyst','2017-08-30',24000),
('1997-03-05','Elena','Castillo','UX Designer','2020-09-05',13000),
('1987-12-01','Miguel','Ortega','Support Engineer','2016-12-01',22000),
('1993-05-23','David','Vidal','Data Engineer','2022-06-01',42000),
('1992-10-10','Laura','Cano','Security Engineer','2020-10-10',39000),
('1998-05-05','Nuria','Soler','Office Assistant','2015-05-05',18000);

SELECT * FROM employees;

SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id = 2;

SELECT * FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET first_name='Pepe' WHERE id = 7;

DELETE FROM employees WHERE id = 5;

DELETE FROM employees WHERE salary > 20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

SELECT * FROM employees WHERE first_name LIKE 'P%';

SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

-- EXTRA
SELECT AVG(salary) FROM employees GROUP BY title;

SELECT title, MAX(salary), MIN(salary) FROM employees GROUP BY title;
--

SELECT first_name, ROUND(salary,2) FROM employees;

-- EXTRA
SELECT first_name || ' ' || last_name AS nombre, ROUND(salary*0.21, 2) AS impuestos, ROUND(salary - salary*0.21, 2) AS salario_neto FROM employees;
--

CREATE TABLE IF NOT EXISTS departments(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

INSERT INTO departments (name) 
VALUES
('Engineering'),
('Marketing');

UPDATE employees SET departments_id=1 WHERE id = 8; 
UPDATE employees SET departments_id=1 WHERE id = 9; 

UPDATE employees SET departments_id=2 WHERE id = 11; 

SELECT * FROM employees INNER JOIN departments ON departments.id = employees.departments_id;

-- EXTRA #Para hacer este extra se vaciara la tabla employees para tener los datos de manera que aparezan bien las prácticas
TRUNCATE employees;

INSERT INTO departments (name) 
VALUES
('Sales'),
('HR'),
('R&D'),
('Legal');

INSERT INTO employees (birth_date, first_name, last_name, title, title_date, salary) 
VALUES
('1995-03-14','Raúl','Santos','Junior Engineer','2020-02-10',28000),
('1992-07-22','Raúl','Gómez','Data Analyst','2020-05-18',31000),
('1990-01-09','Raúl','López','Project Engineer','2019-09-01',36000),
('1988-11-03','Ana','Pérez','Senior Engineer','2020-03-01',45000),
('1996-04-28','María','Ruiz','HR Specialist','2021-07-10',27000),
('1993-09-17','Carlos','Díaz','QA Engineer','2020-11-20',26000),
('2000-02-02','Lucía','Martín','Intern','2020-07-01',5000),
('1989-06-12','Javier','Torres','DevOps Engineer','2018-04-15',18000),
('1991-12-21','Sofía','Navarro','Product Manager','2020-01-20',19000),
('1994-08-30','Pablo','Romero','Finance Analyst','2017-08-30',24000),
('1997-03-05','Elena','Castillo','UX Designer','2020-09-05',13000),
('1987-12-01','Miguel','Ortega','Support Engineer','2016-12-01',22000);

SELECT * FROM employees;

UPDATE employees SET departments_id=1 WHERE id = 16; 
UPDATE employees SET departments_id=1 WHERE id = 17; 
UPDATE employees SET departments_id=1 WHERE id = 18; 
UPDATE employees SET departments_id=1 WHERE id = 19; 

UPDATE employees SET departments_id=2 WHERE id = 20; 
UPDATE employees SET departments_id=2 WHERE id = 21; 
UPDATE employees SET departments_id=2 WHERE id = 22; 

UPDATE employees SET departments_id=3 WHERE id = 23; 
UPDATE employees SET departments_id=3 WHERE id = 24; 

UPDATE employees SET departments_id=4 WHERE id = 25; 

SELECT employees.first_name, departments.name FROM employees INNER JOIN departments ON departments.id = employees.departments_id;

SELECT employees.first_name, departments.name FROM employees LEFT JOIN departments ON departments.id = employees.departments_id;

UPDATE employees SET salary = 42000 WHERE id = 16;
UPDATE employees SET salary = 55000 WHERE id = 17;
UPDATE employees SET salary = 63500 WHERE id = 18;
UPDATE employees SET salary = 75000 WHERE id = 19;

UPDATE employees SET salary = 33000 WHERE id = 20;
UPDATE employees SET salary = 39500 WHERE id = 21;
UPDATE employees SET salary = 48000 WHERE id = 22;

UPDATE employees SET salary = 28000 WHERE id = 23;
UPDATE employees SET salary = 52000 WHERE id = 24;

UPDATE employees SET salary = 31000 WHERE id = 25;

UPDATE employees SET salary = 24000 WHERE id = 26;
UPDATE employees SET salary = 27000 WHERE id = 27;

UPDATE employees SET title = 'Backend Engineer' WHERE id = 16;
UPDATE employees SET title = 'Frontend Engineer' WHERE id = 17;
UPDATE employees SET title = 'Data Engineer' WHERE id = 18;
UPDATE employees SET title = 'DevOps' WHERE id = 19;

UPDATE employees SET title = 'SEO Specialist' WHERE id = 20;
UPDATE employees SET title = 'Content Manager' WHERE id = 21;
UPDATE employees SET title = 'Brand Manager' WHERE id = 22;

UPDATE employees SET title = 'Sales Rep' WHERE id = 23;
UPDATE employees SET title = 'Account Executive' WHERE id = 24;

UPDATE employees SET title = 'Generalist' WHERE id = 25;

UPDATE employees SET title = 'Intern' WHERE id = 26;
UPDATE employees SET title = 'Support' WHERE id = 27;

-- los title_date y los birth_date no estan en el rango de las instrucciones, pero si que están en valores razonables

SELECT * FROM employees INNER JOIN departments ON departments.id = employees.departments_id;

SELECT departments.name FROM departments LEFT JOIN employees ON departments.id = employees.departments_id WHERE employees.departments_id IS NULL; 

SELECT departments.name, COUNT(employees.id) FROM departments LEFT JOIN employees ON departments.id = employees.departments_id GROUP BY departments.name;

SELECT departments.name, ROUND(AVG(employees.salary)) FROM departments LEFT JOIN employees ON departments.id = employees.departments_id GROUP BY departments.name;

SELECT departments.name, MAX(employees.salary) FROM departments LEFT JOIN employees ON departments.id = employees.departments_id GROUP BY departments.name;

SELECT departments.name, MAX(employees.salary) FROM departments INNER JOIN employees ON departments.id = employees.departments_id GROUP BY departments.name ORDER BY max DESC LIMIT 1;

SELECT COUNT(DISTINCT title) FROM employees;

SELECT departments.name, employees.first_name FROM departments INNER JOIN employees ON departments.id = employees.departments_id ORDER BY departments.name;

SELECT departments.name, employees.first_name FROM departments INNER JOIN employees ON departments.id = employees.departments_id ORDER BY employees.last_name;
-- Para las practicas del tercer día de SQL, se eliminan las tablas y se crean de nuevo como el primer día

DROP TABLE employees;
DROP TABLE departments;

CREATE TABLE IF NOT EXISTS employees(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    salary NUMERIC(10,2),
    title VARCHAR(100),
    title_date DATE
);

INSERT INTO employees (birth_date, first_name, last_name, title, title_date, salary) 
VALUES
('1995-03-14','Raúl','Santos','Junior Engineer','2020-02-10',28000),
('1992-07-22','Raúl','Gómez','Data Analyst','2020-05-18',31000),
('1990-01-09','Raúl','López','Project Engineer','2019-09-01',36000),
('1988-11-03','Ana','Pérez','Senior Engineer','2020-03-01',45000),
('1996-04-28','María','Ruiz','HR Specialist','2021-07-10',27000),
('1993-09-17','Carlos','Díaz','QA Engineer','2020-11-20',26000),
('2000-02-02','Lucía','Martín','Intern','2020-07-01',5000),
('1989-06-12','Javier','Torres','DevOps Engineer','2018-04-15',18000),
('1991-12-21','Sofía','Navarro','Product Manager','2020-01-20',19000),
('1994-08-30','Pablo','Romero','Finance Analyst','2017-08-30',24000),
('1997-03-05','Elena','Castillo','UX Designer','2020-09-05',13000),
('1987-12-01','Miguel','Ortega','Support Engineer','2016-12-01',22000),
('1993-05-23','David','Vidal','Data Engineer','2022-06-01',42000),
('1992-10-10','Laura','Cano','Security Engineer','2020-10-10',39000),
('1998-05-05','Nuria','Soler','Office Assistant','2015-05-05',18000);

CREATE TABLE IF NOT EXISTS departments(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

ALTER TABLE employees ADD COLUMN departments_id INTEGER REFERENCES departments(id);

INSERT INTO departments (name) 
VALUES
('Engineering'),
('Marketing');

INSERT INTO departments (name)
VALUES
('Finance');

SELECT * FROM departments;

UPDATE employees SET departments_id=1 WHERE id = 1;

SELECT * FROM employees;

SELECT * FROM employees LEFT JOIN departments ON employees.departments_id = departments.id;

SELECT * FROM employees INNER JOIN departments ON employees.departments_id = departments.id;