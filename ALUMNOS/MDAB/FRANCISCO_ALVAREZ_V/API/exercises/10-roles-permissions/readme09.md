# Exercise 10: Implementation of Roles and Permissions in a Flask API

## Quick Start

```bash
cd exercises/10-roles-permissions
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask Flask-JWT-Extended Flask-Principal Werkzeug
python app.py
```

## Objective
- **Role and Permission Assignment:** Implement a role-based access control system for the API.
- **Route Protection:** Ensure that only users with appropriate permissions can access specific routes.
- **Authentication and Security:** Use JWT (JSON Web Tokens) and Flask-Principal to manage users, roles, and permissions.

---

## Prerequisites

1. **Install Dependencies:**
   Make sure you have the following libraries installed:
   - Flask
   - Flask-JWT-Extended
   - Flask-Principal
   - Werkzeug

   You can install them with:
   ```bash
   pip install Flask Flask-JWT-Extended Flask-Principal Werkzeug
   ```

2. **Clone the Project:**
   Clone the repository or copy the provided `app.py` file.

3. **Run the Script:**
   Start the application with:
   ```bash
   python app.py
   ```

---

## Features

### **User Registration**
Allows registering new users by assigning them a default or custom role.

### **Login**
Authenticates users and provides them with a JWT token that will be required to access protected routes.

### **Available Roles**
1. **Admin:**
   - Access to all routes, including those that manage users.
   - Can perform actions such as updating or deleting other users.

2. **Student:**
   - Restricted access to specific routes designed for students.

### **Route Protection**
Access to routes is restricted based on the user's role. This is managed through Flask-Principal decorators that verify assigned permissions.

---

## API Structure

### **Main Endpoints**

1. **User Registration**
   - **Method:** `POST`
   - **Route:** `/register`
   - **Description:** Registers a new user with a specific role.

2. **Login**
   - **Method:** `POST`
   - **Route:** `/login`
   - **Description:** Authenticates a user and returns a JWT token.

3. **User Profile**
   - **Method:** `GET`
   - **Route:** `/profile`
   - **Description:** Returns information about the authenticated user.

4. **List Users**
   - **Method:** `GET`
   - **Route:** `/users`
   - **Description:** Returns a paginated list of registered users.

5. **Update User**
   - **Method:** `PUT`
   - **Route:** `/users/<username>`
   - **Description:** Updates user information (password or role).
   - **Requires:** Administrator role.

6. **Delete User**
   - **Method:** `DELETE`
   - **Route:** `/users/<username>`
   - **Description:** Deletes a user.
   - **Requires:** Administrator role.

7. **Admin Dashboard**
   - **Method:** `GET`
   - **Route:** `/admin/dashboard`
   - **Description:** Returns information exclusive to administrators.

8. **Student Data**
   - **Method:** `GET`
   - **Route:** `/student/data`
   - **Description:** Returns specific information about the authenticated student.

---

## Testing

### **Basic Tests**
- Register a user and verify they can log in.
- Try to access protected routes without a JWT token and verify that access is denied.
- Generate a valid token and try to access specific routes based on the user's role.

### **Role Tests**
1. Create users with different roles.
2. Try to access restricted routes with each role and verify that restrictions are applied correctly.

### **Common Errors**
- **Invalid Token:** Make sure to include the JWT token in the `Authorization` header with the format `Bearer <token>`.
- **Access Denied:** Verify that the user has the correct role to access the route.

---

## Additional Notes
- Use tools like Postman or curl to test the API routes.
- Make sure the `app.py` file is configured correctly before running the tests.
- You can adjust roles and permissions according to your application's needs.

---

Good luck implementing roles and permissions in your Flask API!
