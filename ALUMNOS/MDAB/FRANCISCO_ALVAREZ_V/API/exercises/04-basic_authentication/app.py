from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# In-memory database for this example
users = {
    "admin": generate_password_hash("admin123")  # We are creating a test user here
}

# Verify the provided credentials
@auth.verify_password
def verify_password(username, password):
    """
    Verifies user credentials for HTTP Basic Authentication.

    This function is called automatically by Flask-HTTPAuth when a protected
    route is accessed with Basic Auth credentials.

    Args:
        username: Username from the Authorization header
        password: Plain text password from the Authorization header

    Returns:
        username if credentials are valid, None otherwise
    """
    # Check if the user is in the database and if the password is correct
    if username in users and check_password_hash(users[username], password):
        return username
    return None

# Route to register new users
@app.route('/users', methods=['POST'])  # TODO: Fill in the HTTP method
# Hint: Use 'POST' to create a user
def register_user():
    """
    Register a new user.

    Request Body (JSON):
        username: User's username
        password: User's password (will be hashed before storing)

    Returns:
        201: User created successfully
        400: Missing required fields or invalid data
        409: User already exists
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Required data is missing"}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 409  # 409 Conflict

    # TODO: Hash the password before storing it
    # Hint: Use generate_password_hash from Werkzeug library (imported at top)
    users[username] = _____(password)
    return jsonify({"message": "User registered successfully"}), 201

# Protected route to get the list of users
@app.route('/users', methods=['   '])  # TODO: Fill in the HTTP method
# Hint: Use 'GET' to list users
@auth.login_required  # Requires HTTP Basic Authentication
def get_users():
    """
    Get list of all registered users (protected endpoint).

    Requires HTTP Basic Authentication with valid credentials.
    The credentials should be sent in the Authorization header as:
    Authorization: Basic <base64(username:password)>

    Returns:
        200: List of usernames
        401: Authentication required or invalid credentials
    """
    # Return the list of registered users
    return jsonify({"users": list(users.keys())}), 200

# Custom error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors"""
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed errors"""
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 Internal Server Error"""
    app.logger.error(f'Internal server error: {str(e)}')
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Run the application in debug mode to facilitate testing
    # WARNING: Do not use debug=True in production!!
    app.run(debug=True)
