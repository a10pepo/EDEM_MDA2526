from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, identity_changed
import math
import random
import string
import secrets
from urllib.parse import urlencode

app = Flask(__name__)

# JWT configuration for token-based authentication
app.config['JWT_SECRET_KEY'] = 'super_secret_jwt_key'
jwt = JWTManager(app)

# Flask-Principal configuration for role and permission management
app.config['SECRET_KEY'] = 'flask_secret_key'
principals = Principal(app)

# Role and permission definitions
admin_permission = Permission(RoleNeed('admin'))  # Permission for administrators
student_permission = Permission(RoleNeed('student'))  # Permission for students

# Simulated database for storing users
users = {}

# Generate test users
def generate_users(users, total):
    """Generates test users with random roles"""
    roles = ['admin', 'student']
    for _ in range(total):
        username = ''.join(random.choices(string.ascii_letters, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        role = random.choice(roles)
        users[username] = {
            'password': generate_password_hash(password),
            'api_key': secrets.token_hex(16),
            'role': role
        }

@app.route('/register', methods=['POST'])
def register_user():
    """Registers a new user with a default or custom role"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400
    if username in users:
        return jsonify({'message': 'User already exists.'}), 400

    users[username] = {
        'password': generate_password_hash(password),
        'api_key': secrets.token_hex(16),
        'role': role
    }
    return jsonify({'message': 'User registered successfully.', 'role': role}), 201

@app.route('/login', methods=['POST'])
def login():
    """Authenticates a user and generates a JWT token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        identity_changed.send(app, identity=Identity(username))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid username or password.'}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Returns the authenticated user's profile"""
    current_user = get_jwt_identity()
    return jsonify({'profile': f'Profile information for {current_user}'}), 200

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """Loads permissions and roles for the authenticated user"""
    identity.user = identity.id
    identity.provides.add(UserNeed(identity.id))

    if identity.id in users:
        role = users[identity.id].get('role')
        if role:
            identity.provides.add(RoleNeed(role))

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Returns a list of users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    total_users = len(users)
    total_pages = math.ceil(total_users / per_page)

    if page > total_pages or page < 1:
        return jsonify({'message': 'Page not found.'}), 404

    start = (page - 1) * per_page
    end = start + per_page
    users_list = list(users.keys())[start:end]

    return jsonify({
        'users': users_list,
        'total_pages': total_pages,
        'current_page': page
    }), 200

@app.route('/users/<username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    """Updates an existing user's information"""
    current_user = get_jwt_identity()

    if username not in users:
        return jsonify({'message': 'User not found.'}), 404

    if not admin_permission.can():
        return jsonify({'message': 'Permission denied.'}), 403

    data = request.get_json()
    password = data.get('password')
    role = data.get('role')

    if password:
        users[username]['password'] = generate_password_hash(password)
    if role:
        users[username]['role'] = role

    return jsonify({'message': 'User updated successfully.'}), 200

@app.route('/users/<username>', methods=['DELETE'])
@jwt_required()
@admin_permission.require(http_exception=403)
def delete_user(username):
    """Deletes a user if the requester has administrator permissions"""
    if username not in users:
        return jsonify({'message': 'User not found.'}), 404

    del users[username]
    return jsonify({'message': 'User deleted successfully.'}), 200

@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@admin_permission.require(http_exception=403)
def admin_dashboard():
    """Returns the dashboard exclusive to administrators"""
    return jsonify({'message': f'Welcome to the admin dashboard, {get_jwt_identity()}.'}), 200

@app.route('/student/data', methods=['GET'])
@jwt_required()
@student_permission.require(http_exception=403)
def student_data():
    """Returns specific data for the authenticated student"""
    return jsonify({'message': f'Student data for {get_jwt_identity()}.'}), 200

if __name__ == '__main__':
    generate_users(users, 100)
    app.run(debug=True)
