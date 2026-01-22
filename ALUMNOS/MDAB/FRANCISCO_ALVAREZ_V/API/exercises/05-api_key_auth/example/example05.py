from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from functools import wraps

app = Flask(__name__)
auth = HTTPBasicAuth()

# Simulated database to store users with API keys
users = {
    # 'username': {
    #     'password': 'hashed_password',
    #     'api_key': 'unique_api_key'
    # }
}


# ============================================================================
# BASIC AUTH VERIFICATION (for API key retrieval only)
# ============================================================================

@auth.verify_password
def verify_password(username, password):
    """Verify username and password for Basic Auth"""
    if username in users:
        if check_password_hash(users[username]['password'], password):
            return username
    return None


# ============================================================================
# API KEY DECORATOR (for protecting endpoints with API keys)
# ============================================================================

def api_key_required(f):
    """
    Decorator to protect routes with API key authentication.

    Checks for 'x-api-key' header and validates it against stored keys.
    This is an ALTERNATIVE to Basic Auth, not used together.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the API key from request headers
        api_key = request.headers.get('x-api-key')

        if not api_key:
            return jsonify({'error': 'API key missing', 'message': 'Include x-api-key header'}), 401

        # Verify if the API key exists in our users database
        for username, user_data in users.items():
            if user_data.get('api_key') == api_key:
                # API key is valid, call the protected function
                return f(*args, **kwargs)

        # API key not found in database
        return jsonify({'error': 'Invalid API key', 'message': 'API key not recognized'}), 401

    return decorated


# ============================================================================
# PUBLIC ENDPOINTS (no authentication required)
# ============================================================================

@app.route('/register', methods=['POST'])
def register():
    """Register a new user and return their API key - Public endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    # Generate a unique API key using uuid
    api_key = str(uuid.uuid4())

    # Store user with hashed password and API key
    users[username] = {
        'password': generate_password_hash(password),
        'api_key': api_key
    }

    return jsonify({
        'message': 'User registered successfully',
        'username': username,
        'api_key': api_key
    }), 201


# ============================================================================
# BASIC AUTH PROTECTED ENDPOINTS (for API key recovery)
# ============================================================================

@app.route('/api-key', methods=['GET'])
@auth.login_required
def get_api_key():
    """
    Get your API key using Basic Auth - Protected by Basic Auth

    This endpoint allows users to retrieve their API key if they lost it.
    It uses Basic Auth (username:password) to authenticate.
    """
    # Get the authenticated username from Basic Auth
    current_user = auth.current_user()

    return jsonify({
        'username': current_user,
        'api_key': users[current_user]['api_key']
    }), 200


# ============================================================================
# API KEY PROTECTED ENDPOINTS (the main pattern to learn)
# ============================================================================

@app.route('/users', methods=['GET'])
@api_key_required
def get_users():
    """
    Get list of all users - Protected by API key

    This endpoint demonstrates API key authentication.
    Clients must include 'x-api-key' header with valid API key.
    """
    user_list = list(users.keys())
    return jsonify({
        'users': user_list,
        'count': len(user_list)
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Exercise 5: API Key Authentication")
    print("="*70)
    print("\nPublic endpoints:")
    print("  POST /register  - Register new user, receive API key")
    print("\nBasic Auth protected endpoints:")
    print("  GET  /api-key   - Retrieve your API key (requires username:password)")
    print("\nAPI Key protected endpoints:")
    print("  GET  /users     - List all users (requires x-api-key header)")
    print("\nExamples:")
    print("  curl -X POST -H 'Content-Type: application/json' \\")
    print("       -d '{\"username\":\"alice\",\"password\":\"secret123\"}' \\")
    print("       http://127.0.0.1:5000/register")
    print("\n  curl -H 'x-api-key: YOUR_API_KEY' http://127.0.0.1:5000/users")
    print("\nServer running at: http://127.0.0.1:5000")
    print("="*70 + "\n")

    app.run(debug=True)
