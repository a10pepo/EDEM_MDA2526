# Exercise 4: Basic Authentication

## Objective
Implement basic authentication (Basic Auth) in a REST API using Python and Flask.

## Description
In this exercise, you will develop a simple REST API that manages "user" resources. You will implement basic authentication to protect certain routes, ensuring that only authenticated users can access them.

## Quick Start

```bash
cd exercises/04-basic_authentication
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-HTTPAuth Werkzeug
python app.py
```

## Requirements
1. **Project Setup:**
   - Initialize a virtual environment.
   - Install the necessary dependencies (`Flask`, `Flask-HTTPAuth`, `Werkzeug`).

2. **API Structure:**
   - Create a route to register new users (`POST /users`).
   - Create a route to get the list of users (`GET /users`), protected with basic authentication.

3. **Basic Authentication Implementation:**
   - Use `Flask-HTTPAuth` to handle authentication.
   - Store passwords securely using `Werkzeug` to hash passwords.
   - Protect routes that require authentication by verifying the provided credentials.

4. **Testing:**
   - Use tools like Postman or `curl` to test the protected routes with and without valid credentials.

## Instructions:

In the _____ space, use the appropriate Werkzeug function to hash the password provided by the user.
Also, observe the spaces within the code to set up the appropriate HTTP methods for each function.
Once corrected, run the script and perform tests from Postman.

## Suggested Steps

1. **Initialize the Project:**
   ```bash
   mkdir api-basic-authentication
   cd api-basic-authentication
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install Flask Flask-HTTPAuth Werkzeug
   ```

2. **Create the API:**
   - Set up the Flask application.
   - Define routes for user registration and listing users.

3. **Implement Basic Authentication:**
   - Use `Flask-HTTPAuth` to create an authentication handler.
   - Hash passwords using `generate_password_hash` from Werkzeug.
   - Verify credentials using `check_password_hash`.

4. **Test the API:**
   - Register a user via `POST /users`.
   - Try accessing `GET /users` without credentials (should fail).
   - Access `GET /users` with valid credentials (should succeed).

## Example Requests with `curl`

1. **Register a User:**
   ```bash
   curl -X POST -H "Content-Type: application/json" \
   -d '{"username": "user1", "password": "password123"}' \
   http://127.0.0.1:5000/users
   ```

2. **Get List of Users (With Authentication):**
   ```bash
   curl -u user1:password123 http://127.0.0.1:5000/users
   ```

3. **Get List of Users (Without Authentication):**
   ```bash
   curl http://127.0.0.1:5000/users
   ```
   This should return a 401 Unauthorized error.

## Points to Consider

- Passwords should never be stored in plain text.
- Basic Auth sends credentials in Base64 encoding (not encryption), so use HTTPS in production.
- Test both successful and failed authentication scenarios.

Good luck!
