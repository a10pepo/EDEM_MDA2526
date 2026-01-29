CREATE TABLE IF NOT EXISTS employers (
    Id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    salary NUMERIC(10, 2),
    title VARCHAR,
    title_date DATE NOT NULL
);

INSERT INTO employers (birth_date, first_name, last_name, salary, title, title_date)
VALUES
('2004-12-12', 'Minguito', 'Aurelio', 30000.00, 'Intern', '2025-01-01'),
('2000-01-01', 'Carlos', 'Gómez', 45000.00, 'Manager', '2024-06-15'),
('1998-03-15', 'Carlos', 'Fernández', 50000.00, 'Analyst', '2024-06-15'),
('2001-07-22', 'Carlos', 'Pérez', 40000.00, 'Developer', '2025-02-01'),
('1999-09-30', 'María', 'López', 48000.00, 'Designer', '2025-03-12'), 
('2002-05-05', 'Pedro', 'Martínez', 42000.00, 'Tester', '2025-04-01'),
('2003-08-18', 'Ana', 'Sánchez', 38000.00, 'Support', '2025-01-20'),
('2004-11-10', 'Miguel', 'Torres', 35000.00, 'Intern', '2025-01-01'),
('2001-12-25', 'Sofía', 'Ramírez', 47000.00, 'HR', '2025-02-15'),
('2000-02-07', 'Javier', 'Hernández', 46000.00, 'Developer', '2025-03-01'),
('2002-06-14', 'Elena', 'García', 39000.00, 'Support', '2025-04-01'),
('1998-10-03', 'Diego', 'Ruiz', 52000.00, 'Analyst', '2024-06-15'),
('2003-01-21', 'Valeria', 'Vega', 41000.00, 'Designer', '2025-02-01'),
('2001-04-11', 'Fernando', 'Morales', 49000.00, 'Manager', '2024-06-15'),
('2000-09-29', 'Isabel', 'Castro', 44000.00, 'Tester', '2025-03-01');




SELECT * FROM employers;
-- SELECT * FROM employers WHERE id = 2;


UPDATE employers SET first_name = 'eustaquio' WHERE id = 7;
DELETE FROM employers WHERE salary > 20000
DELETE FROM employers WHERE salary BETWEEN 14000 AND 20000
SELECT * FROM employers ORDER BY birth_date DESC;
SELECT DISTINCT first_name FROM employers;
SELECT * FROM employers ORDER BY birth_date DESC;
SELECT first_name || ' ' || last_name AS name FROM employers WHERE id = 195;
SELECT * FROM employers WHERE first_name LIKE 'P%';
SELECT * FROM employers WHERE first_name LIKE 'P%';
SELECT * FROM employers WHERE first_name LIKE '%a%';



Crear tabla de departamentos
CREATE TABLE IF NOT EXISTS departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);

-- Insertar departamentos
INSERT INTO departments (name)
VALUES
('engineering'),
('marketing');

SELECT * FROM departments;


-- Crear tabla de empleados
CREATE TABLE IF NOT EXISTS employers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    departments_id INTEGER,
    FOREIGN KEY (departments_id) REFERENCES departments(id)
);

SELECT * FROM employers;


-- 🔹 Asignar dos empleados al departamento Engineering (id = 1)
UPDATE employers 
SET departments_id = 1
WHERE first_name = 'sergio' AND last_name = 'perez';

UPDATE employers 
SET departments_id = 1
WHERE first_name = 'carlos' AND last_name = 'lopez';


-- 🔹 Asignar un empleado al departamento Marketing (id = 2)
UPDATE employers 
SET departments_id = 2
WHERE id = 166;



-- 🔹 Consultar los resultados con JOIN
SELECT 
    employers.first_name, 
    employers.last_name, 
    departments.name AS department
FROM employers
INNER JOIN departments
    ON employers.departments_id = departments.id;





