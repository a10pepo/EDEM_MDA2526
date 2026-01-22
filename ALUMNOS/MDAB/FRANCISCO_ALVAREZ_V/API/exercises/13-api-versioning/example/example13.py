"""
Exercise 13: API Versioning - COMPLETE SOLUTION
Learn to manage API versions and breaking changes
"""

from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# In-memory data storage
users = {}
notes = {}
note_id_counter = 1

# API version information
API_VERSIONS = {
    'v1': {
        'status': 'deprecated',
        'sunset_date': '2025-06-01',
        'deprecation_notice': 'API v1 is deprecated. Please migrate to v2.'
    },
    'v2': {
        'status': 'current',
        'sunset_date': None,
        'deprecation_notice': None
    }
}


# ==================== Helper Functions ====================

def add_version_headers(response, version):
    """
    Add version-related headers to response
    This helps clients know which version they're using and deprecation status
    """
    response.headers['API-Version'] = version

    if API_VERSIONS[version]['status'] == 'deprecated':
        response.headers['Deprecation'] = "true"
        response.headers['Sunset'] = API_VERSIONS[version]['sunset_date']
        response.headers['Warning'] = f'299 - "{API_VERSIONS[version]["deprecation_notice"]}"'

    return response


# ==================== Authentication Routes (Version-agnostic) ====================

@app.route('/auth/register', methods=['POST'])
def register():
    """Register a new user - no versioning needed for auth"""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    users[username] = {
        'password': generate_password_hash(data['password']),
        'created_at': datetime.utcnow().isoformat()
    }

    return jsonify({'message': f'User {username} registered successfully'}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    """Login - no versioning needed for auth"""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']

    if username not in users or not check_password_hash(users[username]['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username)

    return jsonify({
        'access_token': access_token,
        'username': username
    }), 200


# ==================== API Version 1 (Deprecated) ====================

@app.route('/api/v1/notes', methods=['GET'])
@jwt_required()
def get_notes_v1():
    """
    Version 1: Get all notes
    Returns a simple list of notes
    """
    current_user = get_jwt_identity()
    user_notes = [note for note in notes.values() if note['owner'] == current_user]

    response = make_response(jsonify(user_notes))
    response = add_version_headers(response, 'v1')

    return response


@app.route('/api/v1/notes', methods=['POST'])
@jwt_required()
def create_note_v1():
    """
    Version 1: Create a new note
    Simple structure: {title, content}
    """
    global note_id_counter
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400

    note = {
        'id': note_id_counter,
        'title': data['title'],
        'content': data.get('content', ''),
        'owner': current_user
    }

    notes[note_id_counter] = note
    note_id_counter += 1

    response = make_response(jsonify(note), 201)
    response = add_version_headers(response, 'v1')

    return response


@app.route('/api/v1/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note_v1(note_id):
    """
    Version 1: Get a specific note by ID
    """
    current_user = get_jwt_identity()

    if note_id not in notes:
        return jsonify({'error': 'Note not found'}), 404

    note = notes[note_id]

    if note['owner'] != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    response = make_response(jsonify(note))
    response = add_version_headers(response, 'v1')

    return response


# ==================== API Version 2 (Current) ====================

@app.route('/api/v2/notes', methods=['GET'])
@jwt_required()
def get_notes_v2():
    """
    Version 2: Get all notes with enhanced response structure

    BREAKING CHANGES from v1:
    - Response is now an object with 'data', 'count', and 'version' fields
    - Each note includes 'created_at' timestamp
    - Pagination support (query params: page, per_page)
    """
    current_user = get_jwt_identity()

    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Filter notes by owner
    user_notes = [note for note in notes.values() if note['owner'] == current_user]

    # Calculate pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notes = user_notes[start:end]

    response_data = {
        'data': paginated_notes,
        'count': len(user_notes),
        'page': page,
        'per_page': per_page
    }

    response = make_response(jsonify(response_data))
    response = add_version_headers(response, 'v2')

    return response


@app.route('/api/v2/notes', methods=['POST'])
@jwt_required()
def create_note_v2():
    """
    Version 2: Create a new note with enhanced fields

    BREAKING CHANGES from v1:
    - Adds 'created_at' and 'updated_at' timestamps
    - Adds 'tags' field (optional array)
    - Response wrapped in 'data' object
    """
    global note_id_counter
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400

    note = {
        'id': note_id_counter,
        'title': data['title'],
        'content': data.get('content', ''),
        'tags': data.get('tags', []),  # New field in v2
        'owner': current_user,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }

    notes[note_id_counter] = note
    note_id_counter += 1

    response_data = {'data': note, 'message': 'Note created successfully'}

    response = make_response(jsonify(response_data), 201)
    response = add_version_headers(response, 'v2')

    return response


@app.route('/api/v2/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note_v2(note_id):
    """
    Version 2: Get a specific note with enhanced structure

    BREAKING CHANGES from v1:
    - Response wrapped in 'data' object
    - Includes metadata fields
    """
    current_user = get_jwt_identity()

    if note_id not in notes:
        return jsonify({'error': 'Note not found'}), 404

    note = notes[note_id]

    if note['owner'] != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    response_data = {'data': note}

    response = make_response(jsonify(response_data))
    response = add_version_headers(response, 'v2')

    return response


@app.route('/api/v2/notes/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note_v2(note_id):
    """
    Version 2: Update a note (new endpoint, not in v1)
    """
    current_user = get_jwt_identity()

    if note_id not in notes:
        return jsonify({'error': 'Note not found'}), 404

    note = notes[note_id]

    if note['owner'] != current_user:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    # Update fields
    if 'title' in data:
        note['title'] = data['title']
    if 'content' in data:
        note['content'] = data['content']
    if 'tags' in data:
        note['tags'] = data['tags']

    # Update timestamp
    note['updated_at'] = datetime.utcnow().isoformat()

    response_data = {'data': note, 'message': 'Note updated successfully'}

    response = make_response(jsonify(response_data))
    response = add_version_headers(response, 'v2')

    return response


# ==================== Version Info Endpoint ====================

@app.route('/api/versions', methods=['GET'])
def get_versions():
    """
    Get information about all API versions
    """
    return jsonify({
        'versions': API_VERSIONS,
        'current': 'v2',
        'deprecated': ['v1']
    }), 200


# ==================== Root and Health ====================

@app.route('/', methods=['GET'])
def root():
    """API root with version information"""
    return jsonify({
        'message': 'Notes API with versioning',
        'current_version': 'v2',
        'available_versions': list(API_VERSIONS.keys()),
        'endpoints': {
            'auth': '/auth/register, /auth/login',
            'v1': '/api/v1/notes',
            'v2': '/api/v2/notes',
            'version_info': '/api/versions'
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Exercise 13: API Versioning - SOLUTION")
    print("="*60)
    print("\nEndpoints:")
    print("  POST   /auth/register        - Register user")
    print("  POST   /auth/login           - Login user")
    print("")
    print("  V1 (Deprecated - Sunset: 2025-06-01):")
    print("  GET    /api/v1/notes         - List notes (simple array)")
    print("  POST   /api/v1/notes         - Create note (simple)")
    print("  GET    /api/v1/notes/<id>    - Get note")
    print("")
    print("  V2 (Current):")
    print("  GET    /api/v2/notes         - List notes (with pagination)")
    print("  POST   /api/v2/notes         - Create note (with timestamps)")
    print("  GET    /api/v2/notes/<id>    - Get note (wrapped response)")
    print("  PUT    /api/v2/notes/<id>    - Update note (new in v2)")
    print("")
    print("  GET    /api/versions         - Get version information")
    print("  GET    /health               - Health check")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
