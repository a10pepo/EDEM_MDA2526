from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username
    return None

@app.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user.

    Request Body:
        username (str): User's username
        password (str): User's password

    Returns:
        201: User created successfully
        400: Invalid input data
        409: User already exists
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Required data is missing"}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 409  # Fixed: 409 instead of 400

    users[username] = generate_password_hash(password)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    """
    Get list of all registered users.

    Requires HTTP Basic Authentication.

    Returns:
        200: List of usernames
        401: Authentication required
    """
    return jsonify({"users": list(users.keys())}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405  # Fixed: Removed detail exposure

@app.errorhandler(500)
def internal_error(e):
    # Log the error but don't expose details to client
    app.logger.error(f"Internal error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
