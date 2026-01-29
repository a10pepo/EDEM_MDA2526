CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    birth_date DATE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

ALTER TABLE employees
    ADD COLUMN salary NUMERIC(10,2),
    ADD COLUMN title VARCHAR(100),
    ADD COLUMN title_date DATE;

INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date) VALUES
('1990-06-12', 'Alex',      'García',     42000, 'Software Engineer',        '2020-02-14'),
('1988-11-03', 'Alex',      'Santos',     38000, 'Data Analyst',             '2020-05-21'),
('1985-04-22', 'Alex',      'Navarro',    45000, 'DevOps Engineer',          '2020-09-07'),
('1982-09-15', 'Lucía',     'Martínez',   48000, 'Product Manager',          '2020-01-30'),
('1982-09-15', 'Lucía',     'Martínez',   50000, 'Product Manager',          '2020-01-30'),
('1995-01-08', 'Diego',     'Ruiz',       27000, 'QA Engineer',              '2019-11-12'),
('1992-12-27', 'María',     'López',      36000, 'UX Designer',              '2021-03-18'),
('2002-05-14', 'Sofía',     'Hernández',  18000, 'Support Specialist',       '2018-07-22'),
('1980-02-02', 'Javier',    'Iglesias',   49000, 'Solutions Architect',      '2022-04-01'),
('1978-07-09', 'Elena',     'Vidal',      22000, 'Technical Writer',         '2017-10-05'),
('1999-03-30', 'Pablo',     'Serrano',    15000, 'IT Technician',            '2016-06-15'),
('1990-10-10', 'Nuria',     'Cano',       34000, 'Business Analyst',         '2023-02-09'),
('1970-01-20', 'Raúl',      'Ortega',     12000, 'SysAdmin',                 '2015-12-19'),
('1994-08-03', 'Carla',     'Benítez',    26000, 'Marketing Specialist',     '2024-08-27'),
('2001-11-25', 'Hugo',      'Molina',      8000, 'Junior Developer',         '2022-10-11');

DELETE FROM employees WHERE id IN = 5;