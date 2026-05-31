-- CREATE TABLE employees (
--     id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     first_name VARCHAR(50) NOT NULL,
--     last_name VARCHAR(50) NOT NULL,
--     birth_date DATE NOT NULL
-- );

-- ALTER TABLE employees ADD COLUMN salary NUMERIC(10, 2);
-- ALTER TABLE employees ADD COLUMN title VARCHAR(100);
-- ALTER TABLE employees ADD COLUMN title_date DATE;

-- INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date) 
-- VALUES ('John', 'Doe', '2020-01-15', 6000.00, 'Software Engineer', '2020-01-15'),
-- ('John', 'Mikel', '2019-03-22', 45000.00, 'Senior Software Engineer', '2020-03-22'),
-- ('John', 'Johnson', '2021-07-30', 50000.00, 'Junior Developer', '2020-07-30'),
-- ('Bob', 'Brown', '2018-11-12', 90000.00, 'Lead Developer', '2018-11-12'),
-- ('Alice', 'Smith', '2017-05-03', 120000.00, 'Project Manager', '2017-05-03'),
-- ('Eve', 'Davis', '2016-09-14', 110000.00, 'QA Engineer', '2016-09-14'),
-- ('Charlie', 'Wilson', '2015-12-25', 95000.00, 'DevOps Engineer', '2015-12-25'),
-- ('David', 'Taylor', '2014-04-18', 85000.00, 'Business Analyst', '2014-04-18'),
-- ('Fiona', 'Anderson', '2013-08-09', 75000.00, 'UI/UX Designer', '2013-08-09'),
-- ('George', 'Thomas', '2012-02-29', 65000.00, 'Intern', '2012-02-29'),
-- ('Hannah', 'Moore', '2011-06-15', 70000.00, 'Data Scientist', '2011-06-15'),
-- ('Ian', 'Jackson', '2010-10-20', 80000.00, 'System Administrator', '2010-10-20'),
-- ('Judy', 'White', '2009-01-05', 105000.00, 'Network Engineer', '2009-01-05'),
-- ('Kevin', 'Harris', '2008-03-30', 115000.00, 'Security Specialist', '2008-03-30'),
-- ('Laura', 'Martin', '2007-07-22', 95000.00, 'Technical Writer', '2007-07-22');

-- INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date)
-- VALUES ('Patrick', 'Doe', '2020-01-15', 6000.00, 'Software Engineer', '2020-01-15');

-- SELECT * FROM employees;
-- SELECT first_name, salary FROM employees;

-- SELECT * FROM employees WHERE id = 2;
-- SELECT * FROM employees WHERE salary > 20000;
-- SELECT * FROM employees WHERE salary <= 10000;

-- DELETE FROM employees WHERE id = 5;
-- DELETE FROM employees WHERE salary > 20000;

-- SELECT * FROM employees WHERE salary BETWEEN 14000 AND 50000;
-- SELECT * FROM employees ORDER BY birth_date DESC;

-- SELECT DISTINCT first_name FROM employees;
-- SELECT first_name || ' ' || last_name AS name FROM employees WHERE id = 18;

-- SELECT * FROM employees WHERE first_name LIKE 'P%';
-- SELECT * FROM employees WHERE first_name LIKE '%a%';

-- SELECT COUNT(id) FROM employees;
-- SELECT MAX(salary) FROM employees;
-- SELECT title, AVG(salary) FROM employees GROUP BY title;
-- SELECT title, MAX(salary) , MIN(salary) FROM employees GROUP BY title;

-- SELECT first_name, salary,
--     ROUND(salary, 2)
-- FROM employees;

-- SELECT first_name, salary,
--     ROUND(salary * 0.21) AS impuestos,
--     ROUND(salary - (salary * 0.21)) AS salario_neto
-- FROM employees;


-- SELECT
-- employees.first_name,
-- departments.name AS department_name
-- FROM employees
-- LEFT JOIN departments ON employees.department_id = departments.id;

-- SELECT first_name FROM employees;

SELECT * FROM departments;
