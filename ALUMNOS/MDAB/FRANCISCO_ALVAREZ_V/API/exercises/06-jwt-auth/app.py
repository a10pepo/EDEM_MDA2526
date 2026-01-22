from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# JWT Configuration
# WARNING: In production, use environment variables for secrets!
# Example: app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # TODO: Change this to a secure secret key (only for educational purposes)

# Optional: Set token expiration time (default is 15 minutes)
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = _____  # TODO: Initialize JWTManager with the app
# Hint: JWTManager(app)

# Simulated database to store users
users = {
    # 'username': {'password': 'hashed_password'}
}

# ============================================================================
# PUBLIC ENDPOINTS (No authentication required)
# ============================================================================

@app.route('/register', methods=['POST'])
def register():
    """Register a new user - Public endpoint"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    # Hash the password before storing it
    users[username] = {
        'password': generate_password_hash(password)
    }

    return jsonify({
        'message': 'User registered successfully',
        'username': username
    }), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token - Public endpoint

    This is the KEY difference from Basic Auth:
    - User sends username/password ONCE in the request body
    - Server validates credentials and returns a JWT token
    - Client stores the token and uses it for all future requests
    - No need to send username/password with every request!
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Check if user exists and password is correct
    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401

    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT token with user identity
    access_token = _____(identity=username)  # TODO: Create access token
    # Hint: Use create_access_token(identity=username)

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'token_type': 'Bearer'
    }), 200


# ============================================================================
# PROTECTED ENDPOINTS (JWT authentication required)
# ============================================================================

@app.route('/profile', methods=['GET'])
@_____  # TODO: Add JWT required decorator
# Hint: @jwt_required()
def profile():
    """
    Get current user's profile - Protected endpoint

    This endpoint requires a valid JWT token in the Authorization header:
    Authorization: Bearer <token>
    """
    # Extract the user identity from the JWT token
    current_user = _____  # TODO: Get JWT identity
    # Hint: Use get_jwt_identity()

    # In a real application, you would fetch user data from a database
    user_info = {
        'username': current_user,
        'profile': f'Profile information for {current_user}',
        'account_created': '2025-01-01'  # Example data
    }

    return jsonify(user_info), 200


@app.route('/users', methods=['GET'])
@_____  # TODO: Add JWT required decorator
# Hint: @jwt_required()
def get_users():
    """
    Get list of all users - Protected endpoint

    Requires valid JWT token to access this resource.
    """
    current_user = _____  # TODO: Get JWT identity
    # Hint: Use get_jwt_identity()

    return jsonify({
        'users': list(users.keys()),
        'requested_by': current_user
    }), 200


@app.route('/protected', methods=['GET'])
@_____  # TODO: Add JWT required decorator
# Hint: @jwt_required()
def protected():
    """
    Example protected endpoint - Requires JWT

    This demonstrates that ANY endpoint can be protected with @jwt_required()
    """
    current_user = _____  # TODO: Get JWT identity

    return jsonify({
        'message': f'Hello {current_user}, you have access to this protected resource!',
        'tip': 'This endpoint can only be accessed with a valid JWT token'
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
    print("JWT Authentication API Server")
    print("="*70)
    print("\nPublic endpoints (no auth required):")
    print("  POST /register  - Register a new user")
    print("  POST /login     - Login and get JWT token")
    print("\nProtected endpoints (JWT required):")
    print("  GET  /profile   - Get user profile")
    print("  GET  /users     - Get all users")
    print("  GET  /protected - Example protected resource")
    print("\nServer running at: http://127.0.0.1:5000")
    print("="*70 + "\n")

    app.run(debug=True)
