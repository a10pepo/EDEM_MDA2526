CREATE TABLE IF NOT EXISTS employees(
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date     DATE NOT NULL,
    first_name     VARCHAR(100) NOT NULL,
    last_name      VARCHAR(100) NOT NULL
);

ALTER TABLE employees ADD COLUMN IF NOT EXISTS salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title VARCHAR(100);
ALTER TABLE employees ADD COLUMN IF NOT EXISTS title_date DATE;

INSERT INTO employees(birth_date, first_name, last_name, salary, title, title_date)
values ('1985-03-15', 'Marta', 'Soler', 25000, 'Engineer', '2020-06-15'),
('1990-07-22', 'Marta', 'Gómez', 30000, 'Manager', '2021-03-01'),
('1988-11-05', 'Marta', 'López', 28000, 'Analyst', '2022-01-20'),
('1975-05-12', 'Carlos', 'Ramírez', 45000, 'Director', '2019-09-10'),
('1992-09-30', 'Ana', 'Martínez', 15000, 'Engineer', '2020-02-18'),
('1983-02-25', 'Luis', 'Fernández', 20000, 'Analyst', '2020-07-12'),
('1995-06-10', 'Sofía', 'Torres', 5000, 'Intern', '2023-05-01'),
('1980-12-01', 'Javier', 'Pérez', 35000, 'Manager', '2018-11-11'),
('1987-08-14', 'Laura', 'García', 40000, 'Engineer', '2020-10-05'),
('1991-04-18', 'David', 'Ruiz', 32000, 'Analyst', '2021-12-22'),
('1989-03-27', 'Mónica', 'Vega', 27000, 'Consultant', '2022-04-17'),
('1993-11-02', 'Pablo', 'Sánchez', 22000, 'Engineer', '2020-08-30'),
('1984-01-20', 'Elena', 'Cruz', 38000, 'Manager', '2021-06-14'),
('1978-09-08', 'Miguel', 'Hernández', 50000, 'Director', '2017-03-29'),
('1990-05-05', 'Clara', 'Ramos', 12000, 'Analyst', '2020-12-12');

SELECT * FROM employees;

SELECT first_name, salary FROM employees;

SELECT * FROM employees WHERE id=2;

SELECT * FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary<=10000;

UPDATE employees SET first_name='Daniel' WHERE id=7;

DELETE FROM employees WHERE id=5;

DELETE FROM employees WHERE salary>20000;

SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

SELECT * FROM employees ORDER BY birth_date DESC;

SELECT DISTINCT first_name FROM employees;

SELECT first_name || '_' || last_name AS nombre_completo FROM employees;

SELECT * FROM employees WHERE first_name LIKE 'P%';

SELECT * FROM employees WHERE first_name LIKE '%a%';

SELECT COUNT(id) FROM employees;

SELECT MAX(salary) FROM employees;

SELECT title, AVG(salary) AS average_salary FROM employees GROUP BY title;

SELECT title, MAX(salary) AS maximum_salary, MIN(salary) AS minimum_salary FROM employees GROUP BY title;

SELECT first_name, ROUND(salary, 2) FROM employees;

SELECT first_name, ROUND(salary, 2) AS bruto,
    ROUND(salary*0.21, 2) AS impuesto,
    salary-ROUND(salary*0.21, 2) AS neto
FROM employees;

CREATE TABLE IF NOT EXISTS departments(
    id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name   TEXT
);

ALTER TABLE employees ADD COLUMN IF NOT EXISTS department_id  INTEGER REFERENCES departments(id);

INSERT INTO departments(name)
values ('Engineering'),
       ('Marketing');

UPDATE employees
SET department_id = CASE
    WHEN id=1 THEN 1
    WHEN id=2 THEN 1
    WHEN id=3 THEN 2
END;

SELECT * 
FROM employees
LEFT JOIN departments
ON employees.department_id=departments.id;

INSERT INTO departments(name)
values ('Engineering'),
       ('Marketing'),
       ('Sales'),
       ('HR'),
       ('R&D'),
       ('Legal');

UPDATE employees
SET department_id = CASE
    WHEN id=1  THEN 1
    WHEN id=2  THEN 1
    WHEN id=3  THEN 1
    WHEN id=4  THEN 1
    WHEN id=5  THEN 2
    WHEN id=6  THEN 2
    WHEN id=7  THEN 2
    WHEN id=8  THEN 3
    WHEN id=9  THEN 3
    WHEN id=10 THEN 6
END;

SELECT * FROM departments;

UPDATE employees
SET salary = CASE
    WHEN id=1  THEN 42000
    WHEN id=2  THEN 55000
    WHEN id=3  THEN 63500
    WHEN id=4  THEN 75000
    WHEN id=5  THEN 33000
    WHEN id=6  THEN 39500
    WHEN id=7  THEN 48000
    WHEN id=8  THEN 28000
    WHEN id=9  THEN 52000
    WHEN id=10 THEN 31000
    WHEN id=11 THEN 24000
    WHEN id=12 THEN 25000
    WHEN id=13 THEN 26000
    WHEN id=14 THEN 27000
    WHEN id=15 THEN 28000
END;

ALTER TABLE employees ADD COLUMN IF NOT EXISTS title TEXT;

UPDATE employees
SET title = CASE
    WHEN id=1  THEN 'Backend Engineer'
    WHEN id=2  THEN 'Frontend Engineer'
    WHEN id=3  THEN 'Data Engineer'
    WHEN id=4  THEN 'DevOps Engineer'
    WHEN id=5  THEN 'SEO Specialist'
    WHEN id=6  THEN 'Content Manager'
    WHEN id=7  THEN 'Brand Manager'
    WHEN id=8  THEN 'Sales rep'
    WHEN id=9  THEN 'Account ExecutiveHR'
    WHEN id=10 THEN 'HR Generalist'
    WHEN id=11 THEN 'Intern'
    WHEN id=12 THEN 'Intern'
    WHEN id=13 THEN 'Intern'
    WHEN id=14 THEN 'Support'
    WHEN id=15 THEN 'Support'
END;

SELECT * 
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id;

SELECT * 
FROM employees
LEFT JOIN departments
ON employees.department_id=departments.id
WHERE employees.department_id IS NULL;

SELECT departments.name, COUNT(employees.department_id) 
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name;

SELECT departments.name, COUNT(employees.department_id) 
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
WHERE departments.name = 'Engineering'
GROUP BY departments.name;

SELECT employees.*
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
WHERE departments.name='Engineering';

SELECT departments.name, AVG(employees.salary)
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name;

SELECT departments.name, MAX(employees.salary)
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name;

SELECT departments.name, COUNT(employees.title)
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name;

SELECT employees.last_name, departments.name
FROM employees
LEFT JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name, employees.last_name;

SELECT departments.name, COUNT(employees.department_id) as num_dept
FROM employees
INNER JOIN departments
ON employees.department_id=departments.id
GROUP BY departments.name
ORDER BY num_dept DESC
LIMIT 3;

SELECT * FROM employees