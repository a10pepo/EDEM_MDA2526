CREATE DATABASE postgres;

CREATE TABLE IF NOT EXISTS departments (
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name VARCHAR(20) NOT NULL,
register_date  TIMESTAMPTZ NOT NULL DEFAULT now()
);

SELECT * FROM departments;

INSERT INTO departments(name) VALUES ('Ingenieria'), ('Marketing');

ALTER TABLE employees 
ADD COLUMN department_id BIGINT REFERENCES departments(id);

UPDATE employees SET department_id = 1 WHERE id IN (1);
UPDATE employees SET department_id = 2 WHERE id IN (2);

SELECT * FROM employees;

SELECT e.first_name, e.last_name, d.name AS department_name
FROM employees e
LEFT JOIN departments d ON e.department_id = d.id;
SELECT e.first_name, e.last_name, d.name AS department_name
FROM employees e
RIGHT JOIN departments d ON e.department_id = d.id;
SELECT e.first_name, e.last_name, d.name AS department_name
FROM employees e
FULL JOIN departments d ON e.department_id = d.id;