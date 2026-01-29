-- CREATE TABLE IF NOT EXISTS employees (
--   id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--   birth_date      DATE,
--   first_name       VARCHAR(100) NOT NULL,
--   last_name           VARCHAR(255) UNIQUE NOT NULL,
--   register_date     TIMESTAMPTZ NOT NULL DEFAULT now()
-- );

-- ALTER TABLE employees ADD COLUMN salary NUMERIC(10, 2)DEFAULT 0;

-- ALTER TABLE employees ADD COLUMN title VARCHAR(100);
-- ALTER TABLE employees DROP COLUMN register_date;
-- ALTER TABLE employees ADD COLUMN title_date DATE;

-- INSERT INTO employees (birth_date, first_name, last_name, salary, title, title_date)
-- VALUES ('21-10-2003', 'Raul', 'Aragall', 50800, 'Developer', '01-01-2020'),
-- ('15-05-1990', 'Maria', 'Lopez', 6000, 'Manager', '15-03-2018'),
-- ('30-07-1985', 'Juan', 'Garcia', 5000, 'Analyst', '20-06-2019'),
-- ('12-12-1995', 'Ana', 'Martinez', 8000, 'Designer', '10-10-2021'),  
-- ('05-11-1988', 'Maria', 'Hernandez', 7700, 'Consultant', '25-12-2017'), 
-- ('22-03-1992', 'Sofia', 'Gonzalez', 5900, 'Engineer', '30-09-2019'),   
-- ('18-08-1980', 'Maria', 'Rodriguez', 9000, 'Director', '05-05-2016'), 
-- ('09-04-1998', 'Elena', 'Sanchez', 45000, 'Intern', '15-07-2022'),
-- ('27-06-1983', 'Miguel', 'Ramirez', 5700, 'Coordinator', '12-11-2018'), 
-- ('14-01-1991', 'Laura', 'Torres', 47000, 'Supervisor', '20-02-2020'),
-- ('03-09-1987', 'Javier', 'Flores', 6000, 'Specialist', '18-04-2019'),
-- ('11-11-1993', 'Isabel', 'Rivera', 15000, 'Technician', '22-08-2021'),
-- ('29-02-1984', 'Diego', 'Vargas', 355000, 'Administrator', '30-03-2017'),
-- ('07-07-1996', 'Carmen', 'Castillo', 47000, 'Assistant', '14-12-2020'),
-- ('16-10-1989', 'Fernando', 'Jimenez', 33000, 'Planner', '09-06-2018');

SELECT * FROM employees;
