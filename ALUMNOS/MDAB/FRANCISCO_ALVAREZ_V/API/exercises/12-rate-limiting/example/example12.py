"""
Exercise 12: Rate Limiting and API Security - COMPLETE SOLUTION
Learn to protect your API from abuse using Flask-Limiter
"""

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# Initialize Flask-Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Use IP address to identify clients
    default_limits=["200 per day", "50 per hour"],  # Default limits for all routes
    storage_uri="memory://"  # Use in-memory storage (can use Redis in production)
)

# In-memory data storage
users = {}
api_calls = {}  # Track API usage per user


# ==================== Helper Functions ====================

def get_user_from_jwt():
    """Get the current user's username from JWT token"""
    try:
        return get_jwt_identity()
    except:
        return None


# ==================== Routes ====================

@app.route('/health', methods=['GET'])
@limiter.exempt  # Health checks should not be rate limited
def health():
    """Health check endpoint - no rate limiting"""
    return jsonify({'status': 'ok', 'message': 'API is running'}), 200


@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")  # Limit registration to prevent spam
def register():
    """
    Register a new user
    Rate limited to prevent automated account creation
    """
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']
    role = data.get('role', 'user')  # Default role is 'user'

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    # Store user with hashed password
    users[username] = {
        'password': generate_password_hash(password),
        'role': role
    }

    return jsonify({'message': f'User {username} registered successfully'}), 201


@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Prevent brute force attacks
def login():
    """
    Login endpoint with rate limiting to prevent brute force attacks
    Limited to 10 attempts per minute per IP address
    """
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401

    if not check_password_hash(users[username]['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT token with user identity and role
    additional_claims = {'role': users[username]['role']}
    access_token = create_access_token(identity=username, additional_claims=additional_claims)

    return jsonify({
        'access_token': access_token,
        'username': username,
        'role': users[username]['role']
    }), 200


@app.route('/api/data', methods=['GET'])
@jwt_required()
@limiter.limit("20 per minute")  # General API usage limit
def get_data():
    """
    General data endpoint
    Rate limited to 20 requests per minute per user
    """
    current_user = get_jwt_identity()

    # Track API usage
    if current_user not in api_calls:
        api_calls[current_user] = 0
    api_calls[current_user] += 1

    return jsonify({
        'message': 'Here is your data',
        'user': current_user,
        'total_api_calls': api_calls[current_user],
        'data': [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'},
            {'id': 3, 'name': 'Item 3'}
        ]
    }), 200


@app.route('/api/search', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")  # Strict limit for expensive operations
def search():
    """
    Expensive search endpoint
    Strictly rate limited to 5 requests per minute
    This simulates a resource-intensive operation (database query, external API call, etc.)
    """
    query = request.args.get('q', '')
    current_user = get_jwt_identity()

    if not query:
        return jsonify({'error': 'Missing search query parameter'}), 400

    # Simulate expensive search operation
    results = [
        {'id': i, 'title': f'Result {i} for "{query}"'}
        for i in range(1, 6)
    ]

    return jsonify({
        'query': query,
        'results': results,
        'user': current_user,
        'note': 'This endpoint is rate limited to 5 requests per minute'
    }), 200


@app.route('/api/unlimited', methods=['GET'])
@jwt_required()
@limiter.exempt  # No rate limiting on this endpoint
def unlimited():
    """
    Unlimited endpoint - no rate limiting
    Use this pattern for critical endpoints that should never be rate limited
    """
    current_user = get_jwt_identity()

    return jsonify({
        'message': 'This endpoint has no rate limit',
        'user': current_user,
        'note': 'Use exempt endpoints carefully - only for critical operations'
    }), 200


@app.route('/api/stats', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
def get_stats():
    """Get API usage statistics for current user"""
    current_user = get_jwt_identity()

    return jsonify({
        'user': current_user,
        'total_api_calls': api_calls.get(current_user, 0),
        'registered_users': len(users)
    }), 200


# ==================== Error Handlers ====================

@app.errorhandler(429)
def ratelimit_handler(e):
    """
    Custom handler for rate limit exceeded errors
    Returns a JSON response instead of plain text
    """
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description),
        'retry_after': 'Check the Retry-After header'
    }), 429


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Exercise 12: Rate Limiting and API Security - SOLUTION")
    print("="*60)
    print("\nEndpoints:")
    print("  POST   /register          - Register new user (5 per hour)")
    print("  POST   /login             - Login (10 per minute)")
    print("  GET    /api/data          - Get data (20 per minute)")
    print("  GET    /api/search?q=...  - Search (5 per minute)")
    print("  GET    /api/unlimited     - No rate limit")
    print("  GET    /api/stats         - Get stats (10 per minute)")
    print("  GET    /health            - Health check (no limit)")
    print("\nDefault limits: 200 per day, 50 per hour")
    print("Rate limit info included in response headers")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
