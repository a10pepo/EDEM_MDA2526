-- CREATE TABLE IF NOT EXISTS employees (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     birth_date DATE NOT NULL,
--     first_name VARCHAR(100) NOT NULL,
--     last_name VARCHAR(100) NOT NULL
-- );

-- ALTER TABLE employees ADD COLUMN salary NUMERIC(10,2);
-- ALTER TABLE employees ADD COLUMN title VARCHAR(100);
-- ALTER TABLE employees ADD COLUMN title_date DATE;

-- INSERT INTO employees (birth_date, first_name, last_name, title, title_date, salary)
-- VALUES ('1985-04-15', 'Juan', 'Pérez', 'Analista', '2020-03-01', 10000),
-- ('1986-08-20', 'Juan', 'Santos', 'Desarrollador', '2019-05-10', 15000),
-- ('1987-11-02', 'Juan', 'Peris', 'Soporte Técnico', '2020-09-15', 5000),

-- ('1990-01-12', 'Ana', 'López', 'Gerente', '2020-01-20', 20000),
-- ('1982-04-22', 'Carlos', 'García', 'Líder de Proyecto', '2020-07-11', 25000),
-- ('1993-02-16', 'María', 'Ruiz', 'Diseñador', '2020-02-28', 30000),
-- ('1989-05-30', 'Felipe', 'Torres', 'Administrador', '2020-12-05', 18000),
-- ('1995-10-10', 'Sofía', 'Mendoza', 'Contador', '2020-05-19', 22000),

-- ('1988-07-25', 'Lucía', 'Castro', 'Recursos Humanos', '2018-11-13', 12000),
-- ('1978-09-05', 'Pedro', 'Muñoz', 'Director', '2017-06-17', 50000),
-- ('1992-03-18', 'Elena', 'Díaz', 'Tester', '2019-09-03', 17500),
-- ('1980-12-01', 'Roberto', 'Silva', 'Arquitecto de Software', '2021-04-22', 32000),
-- ('1984-06-14', 'Valentina', 'Ríos', 'Ingeniero de Datos', '2019-08-23', 28000),
-- ('1979-02-23', 'Esteban', 'Vargas', 'Consultor', '2022-02-14', 46000),
-- ('1983-05-08', 'Martina', 'Herrera', 'Product Owner', '2021-10-30', 35000);

-- SELECT * FROM employees;



-- SELECT first_name, salary FROM employees;

-- SELECT * FROM employees WHERE id=79;

-- SELECT * FROM employees WHERE salary > 20000;

-- SELECT * FROM employees WHERE salary <= 10000;


-- UPDATE employees SET first_name = 'Eleonor' WHERE id = 88;


-- SELECT * FROM employees;

-- DELETE FROM employees WHERE id = 92;

-- SELECT * FROM employees

-- DELETE FROM employees WHERE salary > 20000;

-- SELECT * FROM employees

-- SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;

-- SELECT * FROM employees ORDER BY birth_date DESC;

-- SELECT DISTINCT first_name FROM employees;

-- SELECT first_name || ' ' || last_name AS nombre_completo FROM employees WHERE id = 176;

-- SELECT * FROM employees WHERE first_name LIKE 'P%';

-- SELECT * FROM employees WHERE first_name LIKE '%a%';

-- SELECT COUNT(id) FROM employees;

-- SELECT MAX(salary) FROM employees;

-- SELECT first_name, salary, ROUND((salary),2) 
-- FROM employees


-- CREATE TABLE IF NOT EXISTS departments (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     name VARCHAR(100) NOT NULL 
-- );

-- ALTER TABLE employees ADD COLUMN department_id INTEGER REFERENCES departments(id);


-- INSERT INTO departments (name) VALUES ('Engineering'), ('Marketing');

-- SELECT *FROM departments;

-- UPDATE employees SET department_id = 1 WHERE id = 198; -- Engineering
-- UPDATE employees SET department_id = 2 WHERE id = 200; -- Engineering
-- UPDATE employees SET department_id = 2 WHERE id = 201; -- Marketing


-- SELECT e.*, d.name AS department_name
-- FROM employees e
-- JOIN departments d ON e.department_id = d.id;

-- INSERT INTO departments(name)
-- VALUES ('Sustainability');

-- SELECT * FROM departments

-- INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date, department_id)
-- VALUES ('2002-02-23', 'Iñaki', 'Buj', '60000', 'Economia', '2023-08-26', 3);

-- SELECT * FROM employees

-- SELECT e.*, d.name AS department_name
-- FROM employees e
-- JOIN departments d ON e.department_id = d.id;



