from flask import Flask, request, jsonify, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os

app = Flask(__name__)

# Secret key for session management
# IMPORTANT: Change this in production! Use environment variables
app.secret_key = 'your-super-secret-key-change-in-production-12345'

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

# OAuth Configuration
oauth = OAuth(app)

# Register GitHub as an OAuth provider
github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID', 'Ov23ct2hCM0q3nQk0aMq'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET', '6dd1fe3248335ad88262ba6e9baa50e93ab2a513'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# In-memory user database
users = {}

@app.route('/')
def home():
    """
    Home endpoint - provides API information and navigation links.

    Returns:
        200: Welcome message with available endpoints
    """
    return jsonify({
        'message': 'OAuth 2.0 Authentication API',
        'endpoints': {
            'GET /': 'This help message',
            'GET /login/github': 'Initiate GitHub OAuth login',
            'GET /callback': 'OAuth callback (handled automatically)',
            'GET /profile': 'Get user profile (requires JWT)',
            'GET /users': 'List all users (requires JWT)',
            'POST /logout': 'Logout (clears session)'
        },
        'flow': [
            '1. Visit /login/github in browser',
            '2. Authorize with GitHub',
            '3. Receive JWT token',
            '4. Use token for protected endpoints'
        ]
    }), 200


@app.route('/login/github')
def login_github():
    """
    Initiate OAuth login flow with GitHub.

    This redirects the user to GitHub's authorization page.
    After authorization, GitHub redirects back to /callback.

    Returns:
        302: Redirect to GitHub authorization page
    """
    # Generate the redirect URL for the OAuth callback
    redirect_uri = url_for('callback', _external=True)

    # Redirect to GitHub's authorization page
    return github.authorize_redirect(redirect_uri)


@app.route('/callback')
def callback():
    """
    OAuth callback endpoint - handles the redirect from GitHub.

    This endpoint:
    1. Receives the authorization code from GitHub
    2. Exchanges it for an access token
    3. Fetches user profile from GitHub API
    4. Creates/updates user in database
    5. Generates JWT token for our API

    Returns:
        200: JWT token and user info on success
        400: Error if OAuth flow fails
    """
    try:
        # Exchange authorization code for access token
        token = github.authorize_access_token()

        # Fetch user profile from GitHub API
        response = github.get('user')
        user_info = response.json()

        # Extract user data from GitHub response
        github_id = user_info.get('id')
        username = user_info.get('login')
        email = user_info.get('email')
        name = user_info.get('name')
        avatar_url = user_info.get('avatar_url')

        # Store or update user in database
        if username not in users:
            users[username] = {
                'github_id': github_id,
                'username': username,
                'email': email,
                'name': name,
                'avatar_url': avatar_url
            }

        # Create a JWT token for the user
        access_token = create_access_token(identity=username)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'token_type': 'Bearer',
            'user': {
                'username': username,
                'email': email,
                'name': name,
                'avatar_url': avatar_url
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'OAuth authentication failed',
            'message': str(e)
        }), 400


@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Get current user's profile information.

    Requires JWT token in Authorization header:
    Authorization: Bearer <token>

    Returns:
        200: User profile data
        401: Missing or invalid token
        404: User not found
    """
    # Get current user identity from JWT token
    current_user = get_jwt_identity()

    if current_user not in users:
        return jsonify({
            'error': 'User not found',
            'message': 'User profile does not exist'
        }), 404

    return jsonify({
        'username': current_user,
        'profile': users[current_user]
    }), 200


@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get list of all registered users.

    Requires JWT token in Authorization header.

    Returns:
        200: List of usernames
        401: Missing or invalid token
    """
    usernames = list(users.keys())
    return jsonify({
        'users': usernames,
        'count': len(usernames)
    }), 200


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logout endpoint (clears session).

    Note: With JWT, true logout requires token blacklisting.
    This is a simplified version that just clears the session.

    Returns:
        200: Logout confirmation
    """
    session.clear()
    return jsonify({
        'message': 'Logged out successfully',
        'note': 'JWT tokens remain valid until expiration. Implement token blacklisting for true logout.'
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors"""
    return jsonify({'error': 'Route not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 Method Not Allowed errors"""
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 Internal Server Error"""
    app.logger.error(f'Internal server error: {str(e)}')
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print('='*60)
    print('OAuth 2.0 Authentication API')
    print('='*60)
    print('\nBefore running this app, you need to:')
    print('1. Create a GitHub OAuth App at:')
    print('   https://github.com/settings/developers')
    print('2. Set Authorization callback URL to:')
    print('   http://127.0.0.1:5000/callback')
    print('3. Copy Client ID and Client Secret to this file')
    print('\nStarting server at http://127.0.0.1:5000')
    print('Visit http://127.0.0.1:5000/ for instructions')
    print('='*60)
    app.run(debug=True)
