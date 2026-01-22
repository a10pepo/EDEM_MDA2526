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
app.config['JWT_SECRET_KEY'] = 'super_secret_jwt_key'
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
    """
    Register a new student.

    Request Body:
        username (str): Student's username
        password (str): Student's password

    Returns:
        201: User created successfully with API key
        400: Invalid input data
        409: User already exists
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in students:
        return jsonify({'message': 'User already exists.'}), 409  # Fixed: 409 instead of 400

    students[username] = {
        'password': generate_password_hash(password),
        'api_key': secrets.token_hex(16)
    }
    return jsonify({'message': 'User registered successfully.', 'api_key': students[username]['api_key']}), 201

@app.route('/login', methods=['POST'])
def login():
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
    current_user = get_jwt_identity()
    return jsonify({'profile': f'Profile information for {current_user}'}), 200

@app.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """
    Get paginated list of students.

    Query Parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10, max: 100)

    Returns:
        200: Paginated list of students with navigation links
        400: Invalid pagination parameters
        404: Page out of range
        401: Authentication required
    """
    try:
        # Get the query parameters 'page' and 'per_page' with default values
        page = request.args.get('page', 1, type=int)  # Current page
        per_page = request.args.get('per_page', 10, type=int)  # Students per page

        # Validate the 'per_page' value
        if per_page <= 0 or per_page > 100:
            return jsonify({'message': 'per_page must be between 1 and 100.'}), 400

        # Calculate the total number of students and pages
        total_students = len(students)  # Total registered students
        total_pages = math.ceil(total_students / per_page)  # Total number of pages

        # Validate the requested page range
        if page < 1 or page > total_pages:
            return jsonify({'message': 'Page not found.'}), 404

        # Determine the start and end indices of the student list
        start = (page - 1) * per_page  # Start index
        end = start + per_page  # End index
        students_list = list(students.keys())[start:end]  # Subset of students

        # Build links to navigate between pages
        base_url = request.base_url  # Base URL of the request
        query_params = request.args.to_dict()  # Current query parameters

        def build_url(new_page):
            # Build a URL with the updated page number
            query_params['page'] = new_page
            return f"{base_url}?{urlencode(query_params)}"

        # Create navigation links (prev and next)
        links = {}
        if page > 1:
            links['prev'] = build_url(page - 1)  # Link to previous page
        if page < total_pages:
            links['next'] = build_url(page + 1)  # Link to next page

        # Return the response with paginated data
        return jsonify({
            'students': students_list,  # List of students on the current page
            'total_pages': total_pages,  # Total number of pages
            'current_page': page,  # Current page
            'per_page': per_page,  # Number of students per page
            'total_students': total_students,  # Total registered students
            'links': links  # Navigation links
        }), 200

    except Exception as e:
        # Fixed: Don't expose internal error details to client
        app.logger.error(f'Pagination error: {str(e)}')
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    # Generate test users at startup
    generate_users(students, 500)  # Generate 500 users to test pagination
    app.run(debug=True)
