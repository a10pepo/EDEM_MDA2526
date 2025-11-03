CREATE DATABASE PruebasSQL_III;

-- Create Table Departments
CREATE TABLE IF NOT EXISTS departments(
        id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name        VARCHAR
        );

-- Create Department (name)
INSERT INTO departments (name)
VALUES
('depart1'),
('depart2'),
('depart3'),
('depart4'),
('depart5');

-- Get departments
SELECT * FROM departments;

-- createEmployee(first_name, last_name, email, department_id)
CREATE TABLE employees (
        id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        first_name      VARCHAR(100) NOT NULL,
        last_name       VARCHAR(100) NOT NULL,
        email           VARCHAR(100) NOT NULL,
        department_id   INTEGER NOT NULL REFERENCES departments(id)
);

INSERT INTO employees(first_name, last_name, email, department_id)
VALUES
('Miguel', 'Herrera', 'miki@example.com', 1),
('Miguel', 'Navarro', 'migue@example.com', 2);

SELECT * FROM employees;
SELECT e.first_name, e.last_name, e.email, d.name FROM employees AS e
LEFT JOIN departments AS d
ON e.department_id = d.id;
