-- CREATE TABLE posts (
--     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     user_id INTEGER NOT NULL REFERENCES users(id),
--     title VARCHAR(100) NOT NULL,
--     body TEXT,                                                    
--     publish_date TIMESTAMPTZ NOT NULL DEFAULT NOW()                 
-- );

-- INSERT INTO posts(user_id, title, body) VALUES (12, 'Post One', 'This is post one'),
-- (9, 'Post Two', 'This is post two'),
-- (12, 'Post Three', 'This is post three'),
-- (9, 'Post Four', 'This is post four'),
-- (1, 'Post Five', 'This is post five'),
-- (3, 'Post Six', 'This is post six'),
-- (1, 'Post Seven', 'This is post seven'),
-- (10, 'Post Eight', 'This is post eight');

-- SELECT *
-- FROM users
-- INNER JOIN posts
-- ON users.id = posts.user_id;

-- CREATE TABLE comments (
--     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     post_id  INTEGER NOT NULL REFERENCES posts(id),
--     user_id  INTEGER NOT NULL REFERENCES users(id),
--     body TEXT NOT NULL,
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );ç


-- INSERT INTO comments(post_id, user_id, body) VALUES
-- (33, 3, 'This is comment one'),
-- (37, 1, 'This is comment two'),
-- (35, 3, 'This is comment three'),
-- (38, 2, 'This is comment four'),
-- (40, 2, 'This is comment five');

-- SELECT
-- comments.body,
-- posts.title,
-- users.first_name,
-- users.last_name
-- FROM comments
-- INNER JOIN posts ON posts.id = comments.post_id
-- INNER JOIN users ON users.id = comments.user_id;

-- CREATE TABLE departments (
--     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
--     name VARCHAR(100) NOT NULL
-- );

-- ALTER TABLE employees ADD COLUMN department_id INTEGER REFERENCES departments(id);

-- INSERT INTO departments (name) VALUES
-- ('Engineering'),
-- ('Marketing');

-- UPDATE employees SET department_id = 1 WHERE id IN (29);
-- UPDATE employees SET department_id = 2 WHERE id IN (30);
-- UPDATE employees SET department_id = 2 WHERE id IN (31);

-- SELECT
-- employees.first_name,
-- departments.name AS department_name
-- FROM employees
-- RIGHT JOIN departments ON employees.department_id = departments.id;

--DIA DE REPASO

-- INSERT INTO departments (name) VALUES
-- ('Finance');

-- SELECT * FROM departments;

-- INSERT INTO employees (first_name, last_name, birth_date, salary, title, title_date, department_id)
-- VALUES ('Sarah', 'Connor', '2022-02-20', 72000.00, 'Financial Analyst', '2022-02-20', 3);

-- SELECT * FROM employees;

-- SELECT
-- employees,
-- departments.name AS department_name
-- FROM employees
-- INNER JOIN departments ON employees.department_id = departments.id;

-- SELECT
-- employees,
-- departments.name AS department_name
-- FROM employees
-- LEFT JOIN departments ON employees.department_id = departments.id;


