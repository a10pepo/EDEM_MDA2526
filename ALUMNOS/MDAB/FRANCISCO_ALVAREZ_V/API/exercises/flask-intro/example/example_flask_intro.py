"""
Flask Introduction Exercise - Complete Solution
This is the reference solution for the Flask introduction exercise.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    """
    Root endpoint that returns a welcome message.
    """
    return 'Welcome to my first Flask application!'

@app.route('/about')
def about():
    """
    About endpoint that returns information about the app.
    """
    return 'This is a Flask introduction exercise to learn basic routing and JSON handling.'

@app.route('/api/hello')
def hello_api():
    """
    API endpoint that returns a simple JSON message.
    """
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/user/<username>')
def get_user(username):
    """
    API endpoint that accepts a username parameter and returns user information.

    Args:
        username (str): The username from the URL path

    Returns:
        JSON response with username and welcome message
    """
    user_data = {
        'username': username,
        'message': f'Welcome, {username}!'
    }
    return jsonify(user_data)

@app.route('/api/greet', methods=['POST'])
def greet():
    """
    API endpoint that accepts a POST request with JSON body containing a name,
    and returns a personalized greeting.

    Expected JSON body:
        {
            "name": "Alice"
        }

    Returns:
        JSON response with greeting message
    """
    # Get JSON data from request body
    data = request.get_json()

    # Extract the 'name' field, default to 'Guest' if not provided
    name = data.get('name', 'Guest')

    # Return JSON response with greeting
    return jsonify({'greeting': f'Hello, {name}!'})

if __name__ == '__main__':
    # Run the Flask application in debug mode
    # Debug mode enables auto-reload and better error messages
    app.run(debug=True)
