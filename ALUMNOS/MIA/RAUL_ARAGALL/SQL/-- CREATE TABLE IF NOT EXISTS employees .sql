-- CREATE TABLE IF NOT EXISTS employees (
--   id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--   birth_date      DATE,
--   first_name       VARCHAR(100) NOT NULL,
--   last_name           VARCHAR(255) UNIQUE NOT NULL,
--   register_date     TIMESTAMPTZ NOT NULL DEFAULT now()
-- );

-- ALTER TABLE employees ADD COLUMN salary NUMERIC(10, 2)DEFAULT 0;

-- ALTER TABLE employees ADD COLUMN title VARCHAR(100);
-- ALTER TABLE employees DROP COLUMN register_date;
-- ALTER TABLE employees ADD COLUMN title_date DATE;

-- INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
-- VALUES ('1990-10-21','Alice','Smith',75000,'Engineer','2020-01-01'),
-- ('1985-05-15','Bob','Johnson',85000,'Manager','2018-03-15'),
-- ('1978-07-30','Charlie','Brown',95000,'Director','2016-06-20'),
-- ('1992-12-12','Diana','Miller',65000,'Designer','2021-10-10'),
-- ('1988-11-05','Ethan','Davis',72000,'Consultant','2017-12-25'),
-- ('1991-03-22','Fiona','Segura',68000,'Analyst','2019-09-30'),
-- ('1980-08-18','George','Tupu',98000,'Director','2016-05-05'),
-- ('1998-04-09','Hannah','Liez',45000,'Intern','2022-07-15'),
-- ('1983-06-27','Ian','Gonzalez',59000,'Coordinator','2018-11-12'),
-- ('1991-01-14','Julia','Wilson',47000,'Supervisor','2020-02-20');

-- SELECT * FROM employees;
-- SELECT first_name, salary FROM employees;

-- SELECT * FROM employees WHERE id = 2;
-- SELECT * FROM employees WHERE salary > 70000;
-- SELECT * FROM employees WHERE salary BETWEEN 60000 AND 80000;

-- UPDATE employees SET title_date = '2023-01-01' WHERE id = 5;

-- UPDATE employees SET first_name = 'Paco'  WHERE id = 7;

-- DELETE FROM employees WHERE id = 5;
-- DELETE FROM employees WHERE salary > 20000;
-- SELECT * FROM employees;

-- SELECT * FROM employees ORDER BY first_name ASC;
-- SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
-- SELECT * FROM employees ORDER BY birth_date DESC;


-- SELECT first_name || ' ' || last_name AS name FROM employees;
-- SELECT DISTINCT age FROM employees;

-- SELECT DISTINCT first_name FROM employees;
-- SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 9;

-- SELECT * FROM  employees WHERE last_name LIKE '%a%';
-- SELECT * FROM employees WHERE first_name LIKE 'a%';

-- SELECT * FROM employees WHERE first_name LIKE '%P%';
-- SELECT * FROM employees WHERE first_name LIKE '%a%';

-- SELECT COUNT(id) FROM employees;
-- SELECT MAX(age) FROM employees;
-- SELECT MIN(age) FROM employees;
-- SELECT SUM(salary) FROM employees;
-- SELECT AVG(salary) FROM employees;

-- SELECT COUNT(DISTINCT id ) FROM employees;
-- SELECT MAX(salary) FROM employeees;
-- SELECT AVG(salary)  FROM employees GROUP BY title;
-- SELECT MAX(salary) AND MIN(salary) FROM employees GROUP BY title;

-- SELECT first_name, salary, 
--     salary * 0.12 AS ahorro_mensual
-- FROM employees; 

-- SELECT first_name, salary,
--     ROUND((salary * 0.21) * 3, 2) AS impuesto_anual
--     FROM employees;

-- SELECT first_name, salary,
--     ROUND(salary - (salary * 0.21) * 3, 2) AS impuesto_anual_neto
--     FROM employees;




-- SELECT * FROM employees;

-- CREATE TABLE departamentos ( 
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     nombre VARCHAR(100) NOT NULL
-- );

-- ALTER TABLE employees ADD COLUMN departamento_id INT,
-- ADD CONSTRAINT fk_departamento
--     FOREIGN KEY (departamento_id)
--     REFERENCES departamentos(id);   

-- INSERT INTO departamentos (nombre) VALUES
-- ('Engineering'),
-- ('Marketing');

-- UPDATE employees SET departamento_id = 1 WHERE id IN (1, 2);
-- UPDATE employees SET departamento_id = 2 WHERE id IN (3);

-- SELECT 
--     e.id AS employee_id,
--     e.first_name AS employees_name,
--     d.nombre AS departamentos_name
-- FROM employees e
-- LEFT JOIN departamentos d
--     ON e.departamento_id = d.id;


-- SELECT * FROM departamentos;
-- SELECT * FROM employees;

-- INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, departamento_id)
-- VALUES
-- ('1987-02-28','Laura','Marti',82000,'Manager','2019-08-22', 2);  

-- SELECT * FROM employees;

-- SELECT departamentos.nombre, employees.first_name
-- FROM employees
-- LEFT JOIN departamentos
-- ON employees.departamento_id = departamentos.id;

-- SELECT * FROM departamentos;

services:
    app:
        image: python:3.11-slim
        working_dir: /app
    volumes:
        - ./:/app                                                  
    env_file: .env
    command: >
        sh -c "pip install -r requirements.txt && python main.py"
    depends_on:
        - postgres 