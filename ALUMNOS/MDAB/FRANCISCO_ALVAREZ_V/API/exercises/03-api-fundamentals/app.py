from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (simplified)
notes = {}
next_id = 1


@app.route('/health', methods=['_____'])  # TODO: Set the correct HTTP method
# Hint: Use 'GET'
def health():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'notes-api',
        'version': '1.0'
    }), 200


@app.route('/notes', methods=['_____', '_____'])  # TODO: Provide the methods for list and create (GET, POST)
# Hint: Use 'GET' and 'POST'
def notes_collection():
    """List notes and create a new note (simplified)"""
    # Handle listing
    if request.method == 'GET':
        return jsonify(list(notes.values())), 200

    # Handle creation
    # TODO: Validate Content-Type is JSON; otherwise return 415
    # Hint: Compare lowercased header value against 'application/json'
    if request.headers.get('Content-Type', '').lower() != '_____':
        return jsonify({'error': 'Unsupported Media Type', 'message': 'Content-Type must be application/json'}), 415

    # TODO: Parse JSON body
    # Hint: data = request.get_json(silent=True)
    data = _____
    if data is None:
        return jsonify({'error': 'Invalid JSON', 'message': 'Request body must be valid JSON'}), 415

    # TODO: Validate required fields title and content
    # Hint: title = data.get('title'); content = data.get('content')
    errors = []
    title = _____
    content = _____
    if not isinstance(title, str) or not title.strip():
        errors.append({'field': 'title', 'message': 'title is required and must be a non-empty string'})
    if not isinstance(content, str) or not content.strip():
        errors.append({'field': 'content', 'message': 'content is required and must be a non-empty string'})
    if errors:
        # Return 400 Bad Request
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    global next_id
    note_id = next_id
    next_id += 1

    # Build the note object
    note = {
        'id': note_id,
        'title': title.strip(),
        'content': content.strip()
    }
    notes[note_id] = note
    return jsonify(note), 201


@app.route('/notes/<int:note_id>', methods=['_____'])  # TODO: Set the correct HTTP method for retrieval
# Hint: Use 'GET'
def note_item(note_id):
    """Return a single note by id"""
    note = notes.get(note_id)
    if not note:
        return jsonify({'error': 'Not Found', 'message': 'Note not found'}), 404
    return jsonify(note), 200


# Error Handlers (keep response shape consistent)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found', 'message': str(error)}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed', 'message': str(error)}), 405


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal server error: {str(error)}')
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("📝 Notes API — Fundamentals (Starter)")
    print("="*70)
    print("Try: GET http://127.0.0.1:5000/health")
    print("Docs: Use readme03.md for steps and curl commands")
    print("="*70 + "\n")
    app.run(debug=True)
