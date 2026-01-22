# Exercise 8: Creating CRUD Endpoints

## Objective
Implement CRUD (Create, Read, Update, Delete) endpoints in a REST API using Python and Flask.

## Description
In this exercise, you will expand the API developed in previous exercises to include full CRUD operations on "users" resources. You will need to create routes that allow creating, reading, updating, and deleting users. Complete the blank spaces in the provided code to implement these functionalities.

## Quick Start

```bash
cd exercises/08-crud-endpoints
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Werkzeug
python app.py
```

**Note:** This exercise uses "users" as the resource name, building on the authentication patterns from previous exercises.

## Requirements
1. **Installation of Additional Dependencies:**
   - Make sure you have the `Flask` library and the extensions used in previous exercises installed.

2. **API Structure:**
   - **Register User (`POST /users`):** Public endpoint to register a new user
   - **Login (`POST /login`):** Authenticate and receive JWT token
   - **Get Users (`GET /users`):** Protected - Returns list of all users
   - **Create User (Admin) (`POST /users/admin`):** Protected - Admin endpoint to create users
   - **Update User (`PUT /users/<username>`):** Protected - Updates a specific user's password
   - **Delete User (`DELETE /users/<username>`):** Protected - Deletes a specific user

3. **CRUD Implementation:**
   - Use the appropriate HTTP methods for each operation.
   - Ensure that routes are protected using JWT authentication implemented in previous exercises.
   - Validate inputs and handle errors appropriately.

4. **Testing:**
   - Use tools like Postman or `curl` to test each of the CRUD operations.
   - Ensure that operations work correctly and that errors are handled appropriately.

## Suggested Steps

1. **Update the `app.py` File:**
   - Import the necessary libraries.
   - Create routes for CRUD operations on "students".

2. **Develop CRUD Operations in `app.py`:**

   Complete the following code in `exercises/08-crud-endpoints/app.py`, filling in the blank spaces indicated by `_____`:

   ```python
   from flask import Flask, jsonify, request
   from flask_httpauth import HTTPBasicAuth
   from werkzeug.security import generate_password_hash, check_password_hash
   from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
   import requests

   app = Flask(__name__)
   auth = HTTPBasicAuth()

   # JWT Configuration
   app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure secret key
   jwt = JWTManager(app)

   # Simulated database to store students
   students = {
       # 'student_name': {'password': 'hashed_password', 'api_key': 'api_key'}
   }

   @auth.verify_password
   def verify_password(username, password):
       if username in students and check_password_hash(students.get(username)['password'], password):
           return username
       return None

   @app.route('/students', methods=['____'])
   def register_student():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')

       if not username or not password:
           return jsonify({'message': 'Username and password are required.'}), 400
       if username in students:
           return jsonify({'message': 'User already exists.'}), 400

       # Hash the password before storing it
       students[username] = {
           'password': generate_password_hash(password),
           'api_key': 'api_key_placeholder'  # Implement API Key generation if applicable
       }
       return jsonify({'message': 'User registered successfully.'}), 201

   @app.route('/login', methods=['____'])
   @auth.login_required
   def login():
       current_user = auth.current_user()
       access_token = create_access_token(identity=current_user)
       return jsonify({'access_token': access_token}), 200

   @app.route('/profile', methods=['____'])
   @jwt_required()
   def profile():
       current_user = get_jwt_identity()
       return jsonify({'profile': f'Profile information for {current_user}'}), 200

   # Create Student
   @app.route('/students', methods=['____'])
   @jwt_required()
   def create_student():
       data = request.get_json()
       username = data.get('username')
       password = data.get('password')

       if not username or not password:
           return jsonify({'message': 'Username and password are required.'}), 400
       if username in students:
           return jsonify({'message': 'Student already exists.'}), 400

       students[username] = {
           'password': generate_password_hash(password),
           'api_key': 'api_key_placeholder'  # Implement API Key generation if applicable
       }
       return jsonify({'message': 'Student created successfully.'}), 201

   # Get Students
   @app.route('/students', methods=['___'])
   @jwt_required()
   def get_students():
       return jsonify({'students': list(students.keys())}), 200

   # Update Student
   @app.route('/students/<username>', methods=['___'])
   @jwt_required()
   def update_student(username):
       if username not in students:
           return jsonify({'message': 'Student not found.'}), 404

       data = request.get_json()
       password = data.get('password')

       if password:
           students[username]['password'] = generate_password_hash(password)
           return jsonify({'message': 'Student updated successfully.'}), 200
       else:
           return jsonify({'message': 'Nothing to update.'}), 400

   # Delete Student
   @app.route('/students/<username>', methods=['___'])
   @jwt_required()
   def delete_student(username):
       if username not in students:
           return jsonify({'message': 'Student not found.'}), 404

       del students[username]
       return jsonify({'message': 'Student deleted successfully.'}), 200

   @app.errorhandler(404)
   def not_found(error):
       return jsonify({'error': 'Resource not found.'}), 404

   @app.errorhandler(405)
   def method_not_allowed(error):
       return jsonify({'error': 'Method not allowed.'}), 405

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. **Run the Application:**

   ```bash
   python app.py
   ```

4. **Test the API:**

   Use Postman or `curl` to test the CRUD endpoints:

   - **Register a Student:**
     ```bash
     curl -X POST http://127.0.0.1:5000/students -H "Content-Type: application/json" -d '{"username": "student1", "password": "password123"}'
     ```

   - **Login:**
     ```bash
     curl -X POST http://127.0.0.1:5000/login -u student1:password123
     ```

   - **Get Students (use the token from login):**
     ```bash
     curl -X GET http://127.0.0.1:5000/students -H "Authorization: Bearer YOUR_TOKEN"
     ```

   - **Update a Student:**
     ```bash
     curl -X PUT http://127.0.0.1:5000/students/student1 -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d '{"password": "newpassword456"}'
     ```

   - **Delete a Student:**
     ```bash
     curl -X DELETE http://127.0.0.1:5000/students/student1 -H "Authorization: Bearer YOUR_TOKEN"
     ```

## Expected Results

- The API should allow you to create, read, update, and delete users.
- All protected routes should require a valid JWT token.
- Error responses should be returned for invalid inputs or when resources are not found.

## Understanding HTTP Status Codes

This exercise uses several HTTP status codes. Understanding when to use each is important:

- **200 OK**: Request succeeded (GET, PUT requests)
- **201 Created**: New resource created successfully (POST requests)
- **400 Bad Request**: Invalid input data (missing fields, bad format)
- **401 Unauthorized**: Authentication required or invalid token
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource already exists (duplicate user)
- **500 Internal Server Error**: Server-side error

### HTTP Methods and Their Purpose

- **POST**: Create a new resource
- **GET**: Retrieve resource(s)
- **PUT**: Update an entire resource (replace all fields)
- **DELETE**: Remove a resource

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

## Notes

- This exercise uses in-memory storage, so all data will be lost when the application restarts.
- In a production environment, you would use a proper database and implement additional security measures.
- The code includes blanks (`_____`) for you to complete - focus on understanding the HTTP methods for each route.
