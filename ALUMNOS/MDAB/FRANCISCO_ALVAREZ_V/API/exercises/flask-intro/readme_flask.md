# Flask Introduction Guide

## Table of Contents
1. [What is Flask?](#what-is-flask)
2. [Environment Setup](#environment-setup)
3. [Your First Flask Application](#your-first-flask-application)
4. [Basic Concepts](#basic-concepts)
5. [Working with JSON](#working-with-json)
6. [Additional Resources](#additional-resources)

## What is Flask?
Flask is a minimalist web framework written in Python that allows you to create web applications quickly with a minimum number of lines of code. It is especially popular for its simplicity and flexibility.

### Main Features:
- Built-in development server
- Built-in debugger
- Unit testing support
- Jinja2 template engine
- WSGI 1.0 compatible
- Extensive documentation
- Large community and many available extensions

## Environment Setup

### Step 1: Python Installation
1. Download Python from [python.org](https://python.org)
2. Make sure to check the "Add Python to PATH" option during installation
3. Verify the installation by opening a terminal and typing:
   ```bash
   python --version
   ```

### Step 2: Create a Virtual Environment
```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Flask
```bash
pip install flask
```

## Your First Flask Application

### Step 1: Create the app.py file
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, students!'

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 2: Run the application
```bash
python app.py
```
Visit http://localhost:5000 in your browser

## Basic Concepts

### 1. Routes
```python
@app.route('/about')
def about():
    return 'Welcome to my first Flask application!'

@app.route('/user/<username>')
def show_user(username):
    return f'Hello, {username}!'
```

### 2. HTTP Methods
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Processing login...'
    return 'Please log in'
```

### 3. Dynamic URL Parameters
```python
@app.route('/user/<username>')
def show_user(username):
    return f'User profile for: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Displaying post {post_id}'
```

## Working with JSON

Since you'll be building APIs in this course, it's important to learn how Flask handles JSON data. JSON is the standard format for sending and receiving data in web APIs.

### 1. Returning JSON Responses

Use `jsonify()` to return JSON data from your endpoints:

```python
from flask import jsonify

@app.route('/api/hello')
def hello_api():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': 'John Doe', 'email': 'john@example.com'}
    return jsonify(user)

@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return jsonify(users)
```

### 2. Reading JSON from Requests

When a client sends JSON data to your API, use `request.get_json()` to read it:

```python
from flask import request, jsonify

@app.route('/api/greet', methods=['POST'])
def greet():
    # Get JSON data from request body
    data = request.get_json()

    # Access fields from the JSON
    name = data.get('name', 'Guest')

    # Return a JSON response
    return jsonify({'greeting': f'Hello, {name}!'})
```

**Testing with Postman:**
- Set method to POST
- In Body tab, select "raw" and "JSON"
- Enter: `{"name": "Alice"}`
- Send the request

### 3. Simple In-Memory Data Storage

For these exercises, we'll use Python dictionaries to store data (no database needed):

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store users in memory
users = {}
next_id = 1

@app.route('/api/users', methods=['GET', 'POST'])
def handle_users():
    global next_id

    if request.method == 'POST':
        # Create a new user
        data = request.get_json()
        user = {
            'id': next_id,
            'name': data.get('name'),
            'email': data.get('email')
        }
        users[next_id] = user
        next_id += 1
        return jsonify(user)

    else:  # GET
        # Return all users
        return jsonify(list(users.values()))

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id])
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. Query Parameters

Access URL query parameters with `request.args`:

```python
from flask import request, jsonify

@app.route('/api/search')
def search():
    # Access query parameter: /api/search?q=flask
    query = request.args.get('q', '')
    return jsonify({'search_query': query})
```

**Note:** You'll learn more about HTTP status codes, validation, and error handling in the next exercises.

## Additional Resources

### Official Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Official Flask Tutorial](https://flask.palletsprojects.com/tutorial/)

### Useful Tools
- Postman (for testing APIs)
- SQLite Browser (for databases)
- Git (for version control)

### Best Practices
1. Always use virtual environments
2. Keep code organized in modules
3. Implement error handling
4. Write tests for your code
5. Document your code properly

## Tips for Students
- Practice writing code regularly
- Don't be afraid to experiment
- Join Flask/Python communities
- Review open source projects
- Keep a learning journal

Happy learning!

## Exercise Task (what to deliver)

**Goal:** Create your first Flask application with simple routes and test it using Postman.

### 1) Build the Application
Create an `app.py` file with the following endpoints:

**Required endpoints:**
- `GET /` - Return a welcome message (text or JSON)
- `GET /about` - Return information about the app
- `GET /api/hello` - Return a JSON message: `{"message": "Hello, World!"}`
- `GET /api/user/<username>` - Return JSON with the username
- `POST /api/greet` - Accept JSON with a "name" field, return a greeting

**Example for the POST endpoint:**
```python
# Request body: {"name": "Alice"}
# Response: {"greeting": "Hello, Alice!"}
```

### 2) Run the Application
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit http://127.0.0.1:5000 in your browser to see your app running.

### 3) Test with Postman
- Create a Postman collection named "Flask Intro" (keep it local, do not commit)
- Add requests for all 5 endpoints
- For each request, include:
  - A clear name (e.g., "Get Welcome Message")
  - A brief description of what the endpoint does
  - The correct HTTP method (GET or POST)
  - Example response
- For the POST request, remember to:
  - Set Body to "raw" and "JSON"
  - Include a sample JSON body: `{"name": "Your Name"}`

### 4) Deliverables
Submit the following:
1. Your `app.py` file
2. Screenshot showing the app running in your terminal
3. Screenshot of your Postman collection showing all 5 requests
4. Exported Postman collection (JSON file) shared via instructed channel

### 5) Tips
- Use the examples from this guide as reference
- Test each endpoint in your browser (for GET requests) before testing in Postman
- Make sure your app is running before testing in Postman
- Don't worry about error handling or validation yet - you'll learn that in the next exercises