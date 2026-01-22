from flask import Flask, request, jsonify

app = Flask(__name__)

notes = {}
next_id = 1


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'notes-api', 'version': '1.0'}), 200


@app.route('/notes', methods=['GET', 'POST'])
def notes_collection():
    if request.method == 'GET':
        return jsonify(list(notes.values())), 200

    if request.headers.get('Content-Type', '').lower() != 'application/json':
        return jsonify({'error': 'Unsupported Media Type', 'message': 'Content-Type must be application/json'}), 415

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Invalid JSON', 'message': 'Request body must be valid JSON'}), 415

    errors = []
    title = data.get('title')
    content = data.get('content')
    if not isinstance(title, str) or not title.strip():
        errors.append({'field': 'title', 'message': 'title is required and must be a non-empty string'})
    if not isinstance(content, str) or not content.strip():
        errors.append({'field': 'content', 'message': 'content is required and must be a non-empty string'})
    if errors:
        return jsonify({'error': 'Invalid input', 'details': errors}), 400

    global next_id
    note_id = next_id
    next_id += 1

    note = {
        'id': note_id,
        'title': title.strip(),
        'content': content.strip()
    }
    notes[note_id] = note
    return jsonify(note), 201


@app.route('/notes/<int:note_id>', methods=['GET'])
def note_item(note_id):
    note = notes.get(note_id)
    if not note:
        return jsonify({'error': 'Not Found', 'message': 'Note not found'}), 404
    return jsonify(note), 200


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
    print("📝 Notes API — Fundamentals (Solution)")
    print("="*70)
    print("Try: GET http://127.0.0.1:5000/health")
    print("="*70 + "\n")
    app.run(debug=True)
