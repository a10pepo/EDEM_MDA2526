from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for demonstration
users = {}
webhook_events = []


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify the API is running.
    This is useful for testing that ngrok is working correctly.
    """
    return jsonify({
        'status': 'ok',
        'service': 'github-webhook-demo',
        'version': '1.0',
        'message': 'API is running and accessible!'
    }), 200


@app.route('/info', methods=['GET'])
def info():
    """
    Returns information about the incoming request.
    Useful for debugging ngrok forwarding.
    """
    return jsonify({
        'your_ip': request.remote_addr,
        'your_user_agent': request.headers.get('User-Agent'),
        'host': request.host,
        'path': request.path,
        'method': request.method,
        'headers': dict(request.headers)
    }), 200


@app.route('/users', methods=['GET', 'POST'])
def users_endpoint():
    """
    Simple user management for testing team collaboration.

    GET: List all users
    POST: Create a new user
    """
    if request.method == 'GET':
        return jsonify(list(users.values())), 200

    # POST: Create user
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    username = data.get('username')
    email = data.get('email')

    if not username:
        return jsonify({'error': 'username is required'}), 400

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    user = {
        'username': username,
        'email': email,
        'id': len(users) + 1
    }
    users[username] = user

    return jsonify(user), 201


# ============================================================================
# GITHUB WEBHOOK ENDPOINT - COMPLETE SOLUTION
# ============================================================================

@app.route('/webhooks/github', methods=['POST'])
def github_webhook():
    """
    Receives REAL push events from GitHub.

    When you configure a webhook in GitHub repository settings, it sends POST
    requests to this endpoint with information about repository events.

    Official documentation: https://docs.github.com/en/webhooks/webhook-events-and-payloads
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    # Handle GitHub "ping" event (sent when webhook is first created)
    # This confirms your webhook endpoint is reachable
    if 'zen' in data and 'hook_id' in data:
        print(f"\n{'='*60}")
        print(f"📥 GitHub Webhook Ping Received!")
        print(f"   Hook ID: {data.get('hook_id')}")
        print(f"   Zen: {data.get('zen')}")
        print(f"   ✅ Webhook is configured correctly!")
        print(f"{'='*60}\n")
        return jsonify({'status': 'pong'}), 200

    # Extract repository info from real GitHub payload
    repository = data.get('repository', {})
    repo_name = repository.get('full_name', 'unknown') if repository else 'unknown'

    # Extract pusher info (who pushed the code)
    pusher = data.get('pusher', {})
    pusher_name = pusher.get('name', 'unknown') if pusher else 'unknown'

    # Extract commits list
    commits = data.get('commits', [])

    # Extract ref (which branch was pushed)
    ref = data.get('ref', 'unknown')

    # Log the webhook with detailed output
    print(f"\n{'='*60}")
    print(f"🎉 REAL GitHub Webhook Received!")
    print(f"📦 Repository: {repo_name}")
    print(f"👤 Pushed by: {pusher_name}")
    print(f"🌿 Branch: {ref}")
    print(f"📝 Commits: {len(commits)}")

    # Show details of each commit
    for i, commit in enumerate(commits, 1):
        commit_msg = commit.get('message', 'No message')
        commit_id = commit.get('id', 'unknown')[:7]  # Short SHA (first 7 chars)
        author = commit.get('author', {}).get('name', 'unknown')
        print(f"   {i}. [{commit_id}] {commit_msg} (by {author})")

    print(f"{'='*60}\n")

    # Store the event for later viewing via /webhooks/events
    webhook_event = {
        'type': 'github_push',
        'repository': repo_name,
        'pusher': pusher_name,
        'ref': ref,
        'commits_count': len(commits),
        'commit_messages': [c.get('message', '') for c in commits]
    }
    webhook_events.append(webhook_event)

    # GitHub expects 200 status to acknowledge receipt
    # If you return non-2xx, GitHub will mark the webhook as failed
    return jsonify({'status': 'received', 'commits_processed': len(commits)}), 200


# ============================================================================
# MONITORING AND DEBUGGING
# ============================================================================

@app.route('/webhooks/events', methods=['GET'])
def list_webhook_events():
    """
    Returns all received webhook events.
    Useful for debugging and verifying webhooks were received.
    """
    return jsonify({
        'total_events': len(webhook_events),
        'events': webhook_events
    }), 200


@app.route('/webhooks/events/clear', methods=['POST'])
def clear_webhook_events():
    """
    Clears all stored webhook events.
    Useful for testing - start fresh.
    """
    global webhook_events
    count = len(webhook_events)
    webhook_events = []
    return jsonify({
        'message': f'Cleared {count} webhook events',
        'remaining': 0
    }), 200


# ============================================================================
# REQUEST LOGGING (for debugging)
# ============================================================================

@app.before_request
def log_request():
    """
    Logs all incoming requests.
    This helps you see traffic coming through ngrok.
    """
    # Skip logging for some paths to reduce noise
    if request.path in ['/favicon.ico']:
        return

    print(f"\n{'='*60}")
    print(f"📨 Incoming Request:")
    print(f"   Method: {request.method}")
    print(f"   Path: {request.path}")
    print(f"   From: {request.remote_addr}")
    print(f"   User-Agent: {request.headers.get('User-Agent', 'Unknown')[:50]}")

    # Show request body for POST/PUT requests
    if request.method in ['POST', 'PUT', 'PATCH']:
        body = request.get_json(silent=True)
        if body:
            print(f"   Body: {body}")

    print(f"{'='*60}\n")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': f'The endpoint {request.path} does not exist',
        'tip': 'Try /health to verify the API is running'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Method Not Allowed',
        'message': f'{request.method} is not allowed for {request.path}'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal server error: {str(error)}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Something went wrong on the server'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 GitHub Webhook Demo - ngrok Exercise (COMPLETE SOLUTION)")
    print("="*70)
    print("Running on: http://127.0.0.1:5000")
    print("\nQuick Start:")
    print("1. In another terminal, run: ngrok http 5000")
    print("2. Copy the https://....ngrok-free.app URL")
    print("3. Configure GitHub webhook with that URL + /webhooks/github")
    print("4. Make a commit to trigger the webhook!")
    print("\nEndpoints available:")
    print("  GET  /health                - Health check")
    print("  GET  /info                  - Request debugging info")
    print("  GET  /users                 - List users")
    print("  POST /users                 - Create user")
    print("  POST /webhooks/github       - GitHub push webhook (MAIN ENDPOINT)")
    print("  GET  /webhooks/events       - List all received webhooks")
    print("  POST /webhooks/events/clear - Clear webhook history")
    print("\nFor detailed instructions, see readme11.md")
    print("="*70 + "\n")

    app.run(debug=True, port=5000)
