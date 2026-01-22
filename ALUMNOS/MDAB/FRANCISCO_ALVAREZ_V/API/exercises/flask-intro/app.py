"""
Flask Introduction Exercise
Create a simple Flask application with basic routes and JSON responses.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# TODO: Create a route for the root path '/' that returns a welcome message
# Hint: Use @app.route('/') and return a string or JSON
@app.route('/')
def index():
    return 'Welcome to my first Flask application!'

# TODO: Create a route for '/about' that returns information about the app
# Hint: Return a string describing your app
@app.route('/about')
def about():
    return 'This is a Flask introduction exercise to learn basic routing and JSON handling.'

# TODO: Create a route for '/api/hello' that returns a JSON message
# Hint: Use jsonify() to return JSON data
@app.route('/api/hello')
def hello_api():
    # TODO: Return a JSON object with a 'message' key
    # Hint: return jsonify({'message': 'your message here'})
    return jsonify({'message': 'Hello, World!'})

# TODO: Create a route for '/api/user/<username>' that accepts a username parameter
# Hint: Use <username> in the route path and pass it as a function parameter
@app.route('/api/user/<username>')
def get_user(username):
    # TODO: Return a JSON object with the username
    # Hint: Create a dictionary with user information and use jsonify()
    user_data = {
        'username': username,
        'message': f'Welcome, {username}!'
    }
    return jsonify(user_data)

# TODO: Create a route for '/api/greet' that accepts POST requests
# Hint: Add methods=['POST'] to the route decorator
@app.route('/api/greet', methods=['POST'])
def greet():
    # TODO: Get JSON data from the request body
    # Hint: Use request.get_json() to parse the JSON body
    data = request.get_json()
    # TODO: Extract the 'name' field from the JSON data
    # Hint: Use data.get('name', 'default_value')
    name = data.get('name', 'Guest')

    # TODO: Return a JSON response with a greeting
    # Hint: Create a dictionary with a 'greeting' key and use jsonify()
    return jsonify({'greeting': f'Hello, {name}!'})

    from flask import jsonify

@app.route('/api/hello')
def hello_api():
    return jsonify({'message': '¡Hola, Mundo!'})

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user = {'id': user_id, 'name': 'Juan Pérez', 'email': 'juan@ejemplo.com'}
    return jsonify(user)

@app.route('/api/users')
def get_users():
    users = [
        {'id': 1, 'name': 'Alicia'},
        {'id': 2, 'name': 'Roberto'}
    ]
    return jsonify(users)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)

