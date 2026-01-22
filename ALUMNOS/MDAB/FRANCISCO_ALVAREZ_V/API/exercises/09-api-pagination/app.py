from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import math
import random
import string
import secrets
from urllib.parse import urlencode

app = Flask(__name__)

# JWT configuration
# WARNING: In production, use environment variables for secrets!
# Example: app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = 'super_secret_jwt_key'  # Only for educational purposes
jwt = JWTManager(app)

# Simulated database to store students
students = {}

# Generate test users
def generate_users(students, total):
    """Generates test users with random names"""
    for _ in range(total):
        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        students[username] = {
            'password': generate_password_hash(password),
            'api_key': secrets.token_hex(16)
        }

@app.route('/register', methods=['POST'])
def register_student():
    """Register a new student"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in students:
        return jsonify({'message': 'User already exists.'}), 409

    students[username] = {
        'password': generate_password_hash(password),
        'api_key': secrets.token_hex(16)
    }
    return jsonify({'message': 'User registered successfully.', 'api_key': students[username]['api_key']}), 201

@app.route('/login', methods=['POST'])
def login():
    """Authenticate a user and generate a JWT token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = students.get(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid username or password.'}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Return the authenticated user's profile"""
    current_user = get_jwt_identity()
    return jsonify({'profile': f'Profile information for {current_user}'}), 200

@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """
    Get paginated list of students.

    Complete this function to implement pagination.

    Hints:
    - Use request.args.get() to retrieve 'page' and 'per_page' query parameters
    - Set default values: page=1, per_page=10
    - Validate that per_page is between 1 and 100
    - Calculate total_pages using math.ceil()
    - Get the subset of students using list slicing
    - Build navigation links using urlencode()
    """
    try:
        # TODO: Get the query parameters 'page' and 'per_page' with default values
        page = _____  # Hint: request.args.get('page', 1, type=int)
        per_page = _____  # Hint: request.args.get('per_page', 10, type=int)

        # TODO: Validate the 'per_page' value
        if per_page <= 0 or per_page > 100:
            return jsonify({'message': 'per_page must be between 1 and 100.'}), 400

        # TODO: Calculate the total number of students and pages
        total_students = _____  # Hint: len(students)
        total_pages = _____  # Hint: math.ceil(total_students / per_page)

        # TODO: Validate the requested page range
        if page < 1 or page > total_pages:
            return jsonify({'message': 'Page not found.'}), 404

        # TODO: Determine the start and end indices of the student list
        start = _____  # Hint: (page - 1) * per_page
        end = _____  # Hint: start + per_page
        students_list = _____  # Hint: list(students.keys())[start:end]

        # TODO: Build links to navigate between pages
        base_url = request.base_url
        query_params = request.args.to_dict()

        def build_url(new_page):
            # Build a URL with the updated page number
            query_params['page'] = new_page
            return f"{base_url}?{urlencode(query_params)}"

        # TODO: Create navigation links (prev and next)
        links = {}
        if page > 1:
            links['prev'] = build_url(page - 1)
        if page < total_pages:
            links['next'] = build_url(page + 1)

        # Return the response with paginated data
        return jsonify({
            'students': students_list,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'total_students': total_students,
            'links': links
        }), 200

    except Exception as e:
        # Log error internally but don't expose details to client
        app.logger.error(f'Pagination error: {str(e)}')
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found.'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed.'}), 405

@app.errorhandler(500)
def internal_error(error):
    # Log the error but don't expose internal details to client
    app.logger.error(f'Internal server error: {str(error)}')
    return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    # Generate test users at startup
    generate_users(students, 500)  # Generate 500 users to test pagination
    app.run(debug=True)
