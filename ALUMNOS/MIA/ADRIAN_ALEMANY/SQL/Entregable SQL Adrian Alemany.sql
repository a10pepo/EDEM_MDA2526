CREATE TABLE IF NOT EXISTS employees (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    birth_date DATE,
    first_name VARCHAR(100),
    last_name VARCHAR(100));

ALTER TABLE employees ADD salary NUMERIC(10,2);
ALTER TABLE employees ADD title VARCHAR(100);
ALTER TABLE employees ADD title_date DATE;
ALTER TABLE employees ADD email VARCHAR(255);
ALTER TABLE employees ADD age INT;

INSERT INTO employees (first_name, last_name, email, age)
VALUES ('Ada', 'Lovelace', 'ada@example.com', 36);
INSERT INTO employees (first_name, last_name, email, age)
VALUES ('Adrian', 'Alemany', 'adrianalemany40@gmail.com', 22);
INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES
('1990-05-15', 'Ana', 'García', 45000.50, 'Project Manager', '2021-03-10'),
('1988-11-20', 'Carlos', 'Rodríguez', 32000.00, 'Software Engineer', '2020-01-15'),
('1992-01-30', 'Sofía', 'Martínez', 28500.75, 'UX/UI Designer', '2022-06-01'),
('1995-07-22', 'David', 'López', 26000.00, 'Junior Developer', '2023-02-20'),
('1985-03-12', 'Elena', 'Sánchez', 48000.90, 'Data Scientist', '2019-11-05'),
('1993-09-05', 'Ana', 'Pérez', 35000.00, 'Marketing Specialist', '2020-07-30'),
('1998-02-18', 'Javier', 'Gómez', 21000.25, 'Intern', '2023-09-01'),
('1991-06-25', 'Laura', 'Fernández', 39000.00, 'Senior Software Engineer', '2020-02-11'),
('1989-12-08', 'Miguel', 'Díaz', 41500.50, 'DevOps Engineer', '2021-08-19'),
('1996-04-14', 'Isabel', 'Moreno', 29500.00, 'QA Tester', '2022-10-03'),
('1990-08-30', 'Ana', 'Jiménez', 49500.00, 'Product Owner', '2018-12-01'),
('1994-10-01', 'Pablo', 'Ruiz', 31000.60, 'Systems Administrator', '2020-11-25'),
('1987-05-19', 'Raquel', 'Alonso', 44000.00, 'Lead Developer', '2020-09-01'),
('1997-03-28', 'Sergio', 'Navarro', 24000.00, 'Junior Analyst', '2023-01-16'),
('1992-11-11', 'Beatriz', 'Torres', 33500.80, 'Frontend Developer', '2021-05-22'),
('1993-01-07', 'Adrián', 'Vázquez', 30500.00, 'Backend Developer', '2022-03-14');


-- SELECT * FROM employees;

-- SELECT * FROM employees WHERE salary BETWEEN 14000 AND 45000;
-- SELECT birth_date FROM employees WHERE birth_date;

-- SELECT DISTINCT first_name
-- FROM employees;

-- SELECT first_name || ' ' || last_name AS nombre_completo
-- FROM employees
-- WHERE id = 9;

-- SELECT * FROM employees
-- WHERE first_name LIKE 'P%';

-- SELECT * FROM employees
-- WHERE first_name = (SELECT first_name FROM employees WHERE id = 9);

-- SELECT COUNT(id) FROM employees;

-- SELECT MAX(salary) FROM employees;

-- SELECT AVG(salary) FROM employees;

-- SELECT first_name, ROUND(salary, 2) AS rounded_salary FROM employees;




-- 1. Crea la nueva tabla 'departments'
-- (Usamos BIGINT para que coincida con el tipo de 'id' de tu tabla employees)
CREATE TABLE departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- 2. Modifica tu tabla 'employees' para añadir la clave foránea (FK)
ALTER TABLE employees
ADD COLUMN department_id BIGINT,
ADD FOREIGN KEY (department_id) REFERENCES departments(id);

-- 3. Inserta los dos departamentos
INSERT INTO departments (name)
VALUES ('Engineering'), ('Marketing');

-- 4. Actualiza tres empleados que YA EXISTEN en tu tabla
-- Usaremos los IDs de los 3 primeros empleados de tu lista:
-- id=1 (Ada Lovelace), id=2 (Adrian Alemany), id=3 (Ana García)

-- Asigna dos empleados a "Engineering"
UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Engineering')
WHERE id IN (1, 2);

-- Asigna un empleado a "Marketing"
UPDATE employees
SET department_id = (SELECT id FROM departments WHERE name = 'Marketing')
WHERE id = 3;

-- 5. Realiza la consulta final con JOIN
-- Esto mostrará TUS 18 empleados, y los 3 primeros
-- ahora tendrán el nombre de su departamento al lado.
SELECT
    employees.first_name,
    employees.last_name,
    employees.title,
    departments.name AS department_name
FROM
    employees
LEFT JOIN
    departments ON employees.department_id = departments.id;

VIEW TABLE employees;

create table users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT
);

CREATE TABLE posts (
    post_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    user_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE comments (
    comment_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);



INSERT INTO comments (post_id, user_id, content)
VALUES (1, 1, 'This is a comment on post one');


INSERT INTO departments (name)
VALUES ('Human Resources');

SELECT * FROM departments;

INSERT INTO employees (first_name, last_name, email, age, department_id)
VALUES (
    'Lucia',
    'Gomez',
    'lucia@example.com',
    31,
    (SELECT id FROM departments WHERE name = 'Ventas')
);

ALTER TABLE employees
DROP COLUMN department_id;

ALTER TABLE employees
ADD COLUMN department_id BIGINT REFERENCES departments(id);

SELECT * FROM employees;


DROP TABLE employees;
