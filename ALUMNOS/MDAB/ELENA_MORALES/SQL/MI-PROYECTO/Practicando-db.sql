CREATE DATABASE practicandodb;

CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

ALTER TABLE departments ADD COLUMN engineering NUMERIC(10,2);
ALTER TABLE departments ADD COLUMN marketing VARCHAR(100);
ALTER TABLE departments DROP COLUMN engineering;
ALTER TABLE departments DROP COLUMN marketing;

INSERT INTO departments (name)
VALUES ('engineering'),
('marketing');

ALTER TABLE employees
ADD COLUMN department_id BIGINT,
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id)
REFERENCES departments(id);

UPDATE employees SET department_id = 1 WHERE id IN (1, 2);
UPDATE employees SET department_id = 2 WHERE id = 3;

SELECT * FROM departments;

SELECT * FROM employees;

SELECT
    employees.first_name,
    employees.last_name,
    departments.name
FROM
    employees
INNER JOIN
    departments ON employees.department_id = departments.id;

SELECT
    employees.first_name,
    employees.last_name,
    departments.name
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id;
