CREATE TABLE university_db;

CREATE TABLE IF NOT EXISTE students(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    enrollment_date TIMESTAMP NOT NULL DEFAULT now(),
    grade NUMERIC(4 , 2)
)

ALTER TABLE students ADD COLUMN city VARCHAR(100);
ALTER TABLE students ALTER COLUMN grade TYPE INTEGER;

INSERT INTO students (first_name, last_name, enrollment_date, grade, city)
VALUES
('Alice', 'Johnson', '2021-09-01', 3.5, 'New York'),
('Bob', 'Smith', '2020-09-01', 3.8, 'Los Angeles'),
('Charlie', 'Brown', '2019-09-01', 3.2, 'Chicago'),
('Diana', 'Prince', '2021-01-15', 3.9, 'San Francisco'),
('Ethan', 'Hunt', '2020-01-15', 3.6, 'Miami'),
('Fiona', 'Gallagher', '2019-01-15', 3.4, 'Boston'),
('George', 'Miller', '2021-05-20', 3.7, 'Seattle'),
('Bob', 'Davis', '2020-05-20', 3.3, 'Austin'),
('Ian', 'Clark', '2019-05-20', 3.0, 'Denver'),
('Jenna', 'Wilson', '2021-08-10', 3.8, 'Portland');