from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
auth = HTTPBasicAuth()

# JWT Configuration
# WARNING: In production, use environment variables for secrets!
# Example: app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = 'super_secret_jwt_key'  # Only for educational purposes
jwt = JWTManager(app)

# Simulated database to store users
users = {}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username)['password'], password):
        return username
    return None

@app.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No JSON data received.'}), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required.'}), 400

        if username in users:
            return jsonify({'message': 'User already exists.'}), 400

        users[username] = {
            'password': generate_password_hash(password)
        }
        return jsonify({'message': 'User registered successfully.'}), 201

    except Exception as e:
        # Log error internally but don't expose details to client
        app.logger.error(f'Registration error: {str(e)}')
        return jsonify({'message': 'Error processing request.'}), 400

@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    current_user = auth.current_user()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({'profile': f'Profile information for {current_user}'}), 200

@app.route('/users/admin', methods=['POST'])
@jwt_required()
def create_user_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    if username in users:
        return jsonify({'message': 'User already exists.'}), 400

    users[username] = {
        'password': generate_password_hash(password)
    }
    return jsonify({'message': 'User created successfully.'}), 201

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    return jsonify({'users': list(users.keys())}), 200

@app.route('/users/<username>', methods=['PUT'])
@jwt_required()
def update_user(username):
    if username not in users:
        return jsonify({'message': 'User not found.'}), 404

    data = request.get_json()
    password = data.get('password')

    if password:
        users[username]['password'] = generate_password_hash(password)
        return jsonify({'message': 'User updated successfully.'}), 200
    else:
        return jsonify({'message': 'No data to update.'}), 400

@app.route('/users/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    if username not in users:
        return jsonify({'message': 'User not found.'}), 404

    del users[username]
    return jsonify({'message': 'User deleted successfully.'}), 200

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
    app.run(debug=True)