CREAT   TABL   I  NO    EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_name VARCHAR(100),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(255) UNIQUE NOT NULL
);

ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
ALTER TABLE employees ADD COLUMN title VARCHAR (100);
ALTER TABLE employees ADD COLUMN title_date DATE; 


INSERT INTO employees (birth_name, first_name, last_name, salary, title, title_date)
VALUES ('Paola Reguera Gonzalez', 'Paola', 'Reguera', 50000, 'Comunicacion y RRPP', '2023-06-24'),
('Laura Isabel Martínez', 'Laura', 'Martínez', 48000, 'Senior Engineer', '2020-03-15'),
('Laura Sofía Gómez', 'Laura', 'Gómez', 42000, 'Engineer', '2020-07-10'),
-- ('Laura Elena Pérez', 'Laura', 'Pérez', 5100, 'Junior Engineer', '2021-01-20'),
('Carlos Javier López', 'Carlos', 'López', 15000, 'Technician', '2019-05-22'),
('Ana Lucía Torres', 'Ana', 'Torres', 22000, 'Analyst', '2020-02-12'),
('David Andrés Ruiz', 'David', 'Ruiz', 33000, 'Project Manager', '2020-11-09'),
('Marta Beatriz Santos', 'Marta', 'Santos', 27000, 'Consultant', '2020-06-05'),
('Lucía Fernanda Navarro', 'Lucía', 'Navarro', 37000, 'Developer', '2021-09-30'),
-- ('Pablo Alejandro Jiménez', 'Pablo', 'Jiménez', 19000, 'Sales Associate', '2018-04-14'),
-- ('Sofía Carolina Ramos', 'Sofía', 'Ramos', 12000, 'Marketing Specialist', '2022-07-19'),
('Andrés Felipe Moreno', 'Andrés', 'Moreno', 46000, 'Team Lead', '2017-10-01'),
-- ('Elena Patricia Castro', 'Elena', 'Castro', 8000, 'Intern', '2023-03-25'),
('Diego Luis Hernández', 'Diego', 'Hernández', 50000, 'Director', '2020-12-01'),
('Nuria Belén Vega', 'Nuria', 'Vega', 25000, 'HR Coordinator', '2021-05-10');

SELECT * FROM employees;
-- SELECT first_name, salary FROM employees; 

-- SELECT * FROM employees WHERE id=2;
-- SELECT * FROM employees WHERE salary>20000;
-- SELECT * FROM employees WHERE salary<=10000;

-- UPDATE employees SET first_name= 'Pepe' WHERE id=7; 
-- SELECT * FROM employees WHERE id=7;
-- DELETE FROM employees WHERE id=5;
-- SELECT * FROM employees;
-- DELETE FROM employees WHERE salary>20000;
-- SELECT * FROM employees;

-- SELECT * FROM employees ORDER BY salary BETWEEN 14.000 AND 50.000; 
-- SELECT * FROM employees ORDER BY birth_name DESC;

-- SELECT DISTINCT first_name FROM employees;
-- SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id=9; 

-- SELECT * FROM employees WHERE first_name LIKE 'P%';
-- SELECT * FROM employees WHERE first_name LIKE '%a%';

-- SELECT first_name, ROUND (salary, 2) FROM employees;

-- EXTRA 
-- SELECT first_name, salary FROM employees; 
-- SELECT first_name, salary,
--     ROUND (salary * 0.21, 2) AS salario_con_impuestos,
--     ROUND (salary -(salary* 0.21), 2) AS salario_neto
-- FROM employees;


-- CREATE TABLE IF NOT EXISTS departments (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     name VARCHAR (100) NOT NULL
-- );

-- ALTER TABLE employees
-- ADD COLUMN department_id INT REFERENCES departments(id);

-- ALTER TABLE departments
-- ALTER COLUMN name TYPE VARCHAR (100);

-- SELECT * FROM departments;

-- INSERT INTO departments (name) VALUES
-- ('Engineering'),
-- ('Marketing');

-- UPDATE employees SET department_id=1 WHERE id IN (1,10)
-- UPDATE employees SET department_id=2 WHERE id=4; 

-- SELECT 
--     employees.first_name,
--     employees.last_name,
--     employees.title,
--     departments.name AS department_name
-- FROM employees
-- INNER JOIN departments
-- ON employees.department_id = departments.id;

-- INSERT INTO departments (name)
-- VALUES ('Human Resources'),
-- ('Sales'),
-- ('Finance');
-- SELECT * FROM departments;

-- UPDATE employees SET department_id=3 WHERE id=55; 

-- SELECT
--     employees.first_name,
--     employees.last_name,
--     employees.title,
--     departments.name AS department_name
-- FROM employees
-- LEFT JOIN departments
-- ON employees.department_id = departments.id;   

SELECT employees.employees_id, employees.first_name, employees.last_name, departments.department_name
        FROM employees 
        JOIN departments ON employees.department_id = departments.department_id;




