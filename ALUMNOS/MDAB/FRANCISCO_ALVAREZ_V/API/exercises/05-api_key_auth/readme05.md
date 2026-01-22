# Exercise 5: API Key Authentication

## Objective

Learn how to implement **API key authentication** in a Flask REST API, understanding when and why to use API keys instead of username/password credentials.

## Quick Start

```bash
cd exercises/05-api_key_auth
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

---

## What You'll Learn

This exercise builds on Exercise 04 (Basic Authentication) and introduces:

1. **API Key Generation** using UUID
2. **Custom Decorators** for API key validation
3. **Header-based Authentication** with `x-api-key`
4. **When to Use API Keys** vs Basic Auth
5. **Key Recovery Pattern** (retrieve lost API keys)

---

## What Are API Keys?

**API keys** are unique identifiers used to authenticate API requests without sending username/password credentials repeatedly.

### Real-World Examples:

- **Google Maps API**: Requires API key for every request
- **OpenWeatherMap**: Sends API key in query string (`?appid=YOUR_KEY`)
- **GitHub API**: Uses personal access tokens (a type of API key)
- **Stripe**: Uses secret keys for payment processing

### API Key vs Basic Auth

| Feature | Basic Auth | API Key |
|---------|------------|---------|
| **Sends credentials** | Every request (username:password) | Once at registration |
| **Token format** | Base64 encoded `user:pass` | UUID or random string |
| **Expires** | Never (unless password changes) | Can be revoked/regenerated |
| **Storage** | Client stores password | Client stores API key |
| **Security** | Credentials exposed on every request | Credentials only sent once |
| **Use case** | Simple apps, admin panels | Public APIs, third-party access |

---

## API Structure

### Public Endpoints (No Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user, receive API key |

### Basic Auth Protected

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/api-key` | Basic Auth | Retrieve your API key (if lost) |

### API Key Protected

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/users` | API Key | List all users |

---

## How It Works

### Pattern 1: Register and Get API Key

```
Client                          Server
  |                               |
  |  POST /register               |
  |  {username, password}         |
  | ----------------------------> |
  |                               | Generate UUID API key
  |                               | Hash password
  |                               | Store both
  |  {api_key: "abc123..."}       |
  | <---------------------------- |
  |                               |
  | Client stores API key locally |
```

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"secret123"}' \
     http://127.0.0.1:5000/register
```

**Response:**
```json
{
  "message": "User registered successfully",
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

**Client saves this API key** (in config file, environment variable, or secure storage).

### Pattern 2: Use API Key for Protected Endpoints

```
Client                          Server
  |                               |
  |  GET /users                   |
  |  Header: x-api-key: abc123... |
  | ----------------------------> |
  |                               | Validate API key
  |                               | Check if key exists
  |  {users: [...]}               |
  | <---------------------------- |
```

**Example:**
```bash
curl -H "x-api-key: a1b2c3d4-e5f6-4789-a012-3456789abcde" \
     http://127.0.0.1:5000/users
```

**Response:**
```json
{
  "users": ["alice", "bob"],
  "count": 2
}
```

### Pattern 3: Recover Lost API Key (Optional)

If a user loses their API key, they can retrieve it using their username/password:

```bash
curl -u alice:secret123 http://127.0.0.1:5000/api-key
```

**Response:**
```json
{
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

---

## Implementation Guide

### TODOs in app.py

You need to fill in **5 strategic blanks**:

1. **Line 4**: Import `uuid` library
2. **Line 46**: Get API key from request headers (`x-api-key`)
3. **Line 54**: Compare extracted API key with stored keys
4. **Line 87**: Generate unique API key using `uuid.uuid4()`
5. **Line 106**: Set HTTP method for API key retrieval endpoint
6. **Line 129**: Apply `@api_key_required` decorator

### Key Concepts to Implement

#### 1. Generating API Keys with UUID

**What is UUID?**
- **Universally Unique Identifier**
- 128-bit number, typically displayed as 32 hexadecimal digits
- Example: `550e8400-e29b-41d4-a716-446655440000`

**Why UUID for API keys?**
- Extremely low collision probability (duplicate keys)
- Cryptographically random
- Standardized format
- No database lookups needed for generation

**Implementation:**
```python
import uuid

# Generate a unique API key
api_key = str(uuid.uuid4())
# Result: "a1b2c3d4-e5f6-4789-a012-3456789abcde"
```

#### 2. Creating Custom Decorators

**What is a decorator?**
A decorator is a function that wraps another function to add extra behavior.

**Basic decorator pattern:**
```python
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Code before the function
        print("Before function call")

        # Call the original function
        result = f(*args, **kwargs)

        # Code after the function
        print("After function call")

        return result
    return decorated_function

@my_decorator
def hello():
    print("Hello!")
```

**For API key validation:**
```python
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Extract API key from headers
        api_key = request.headers.get('x-api-key')

        # 2. Validate it exists
        if not api_key:
            return jsonify({'error': 'API key missing'}), 401

        # 3. Check if valid
        if api_key not in valid_keys:
            return jsonify({'error': 'Invalid API key'}), 401

        # 4. If valid, call the original function
        return f(*args, **kwargs)

    return decorated
```

#### 3. Reading Headers in Flask

```python
from flask import request

# Get a specific header
api_key = request.headers.get('x-api-key')

# Check if header exists
if 'x-api-key' in request.headers:
    print("API key present")

# Get all headers
all_headers = request.headers
```

**Common API key header names:**
- `x-api-key` (most common)
- `Authorization: Bearer YOUR_KEY`
- `api-key`
- `X-API-KEY`

---

## Testing the API

### 1. Register a New User

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"secret123"}' \
     http://127.0.0.1:5000/register
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

**Save the API key!** You'll need it for subsequent requests.

### 2. Access Protected Endpoint with API Key

```bash
curl -H "x-api-key: a1b2c3d4-e5f6-4789-a012-3456789abcde" \
     http://127.0.0.1:5000/users
```

**Expected Response:**
```json
{
  "users": ["alice"],
  "count": 1
}
```

### 3. Test with Invalid API Key

```bash
curl -H "x-api-key: invalid-key-12345" \
     http://127.0.0.1:5000/users
```

**Expected Response:**
```json
{
  "error": "Invalid API key",
  "message": "API key not recognized"
}
```

### 4. Test with Missing API Key

```bash
curl http://127.0.0.1:5000/users
```

**Expected Response:**
```json
{
  "error": "API key missing",
  "message": "Include x-api-key header"
}
```

### 5. Recover API Key with Basic Auth

```bash
curl -u alice:secret123 http://127.0.0.1:5000/api-key
```

**Expected Response:**
```json
{
  "username": "alice",
  "api_key": "a1b2c3d4-e5f6-4789-a012-3456789abcde"
}
```

---

## Understanding the Code Flow

### Registration Flow

```python
@app.route('/register', methods=['POST'])
def register():
    # 1. Get username and password from JSON body
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 2. Validate input
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    # 3. Check if user exists
    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    # 4. Generate unique API key
    api_key = str(uuid.uuid4())

    # 5. Store user with hashed password and API key
    users[username] = {
        'password': generate_password_hash(password),
        'api_key': api_key
    }

    # 6. Return API key to client
    return jsonify({'api_key': api_key}), 201
```

### API Key Validation Flow

```python
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # 1. Extract API key from headers
        api_key = request.headers.get('x-api-key')

        # 2. Check if present
        if not api_key:
            return error_response('API key missing'), 401

        # 3. Search for API key in database
        for username, user_data in users.items():
            if user_data.get('api_key') == api_key:
                # Valid! Call the protected function
                return f(*args, **kwargs)

        # 4. API key not found
        return error_response('Invalid API key'), 401

    return decorated
```

---

## Common Issues and Solutions

### Issue 1: "pip install uuid" fails

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement uuid
```

**Solution:**
`uuid` is part of Python's standard library. **You don't need to install it.**
Just import it directly:
```python
import uuid
```

### Issue 2: API Key Not Working

**Symptom:**
```json
{
  "error": "Invalid API key"
}
```

**Solution:**
- Verify you're using the exact API key from the registration response
- Check for extra spaces or quotes in the header
- Ensure header name is exactly `x-api-key` (case-insensitive in HTTP)

**Debug tip:**
```bash
# Store API key in variable to avoid typos
API_KEY="a1b2c3d4-e5f6-4789-a012-3456789abcde"
curl -H "x-api-key: $API_KEY" http://127.0.0.1:5000/users
```

### Issue 3: API Key Missing Error

**Symptom:**
```json
{
  "error": "API key missing"
}
```

**Solution:**
Make sure you're including the `-H` flag with curl:
```bash
# Wrong (no header)
curl http://127.0.0.1:5000/users

# Right
curl -H "x-api-key: YOUR_KEY" http://127.0.0.1:5000/users
```

### Issue 4: Decorator Not Working

**Symptom:**
Protected endpoint accessible without API key.

**Solution:**
Make sure decorator is applied:
```python
# Wrong
@app.route('/users', methods=['GET'])
def get_users():  # Missing @api_key_required
    ...

# Right
@app.route('/users', methods=['GET'])
@api_key_required  # Decorator applied
def get_users():
    ...
```

---

## Acceptance Criteria

Your implementation should:

- ✅ Generate unique API keys with UUID
- ✅ Store API keys with user data
- ✅ Return API key on registration
- ✅ Validate API keys from `x-api-key` header
- ✅ Reject requests with missing API keys (401)
- ✅ Reject requests with invalid API keys (401)
- ✅ Allow API key recovery using Basic Auth
- ✅ Use custom decorator for API key protection
- ✅ Allow multiple users with unique API keys

---

## Stretch Goals

Once you complete the basic implementation:

### 1. Add API Key Regeneration

Allow users to regenerate their API key:

```python
@app.route('/api-key/regenerate', methods=['POST'])
@auth.login_required
def regenerate_api_key():
    current_user = auth.current_user()

    # Generate new API key
    new_api_key = str(uuid.uuid4())
    users[current_user]['api_key'] = new_api_key

    return jsonify({
        'message': 'API key regenerated',
        'api_key': new_api_key
    }), 200
```

### 2. Add API Key Expiration

Track when API keys were created and expire old ones:

```python
from datetime import datetime, timedelta

# On registration
users[username] = {
    'password': hashed_password,
    'api_key': api_key,
    'key_created_at': datetime.now()
}

# In decorator
def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')

        for username, user_data in users.items():
            if user_data.get('api_key') == api_key:
                # Check if expired (e.g., 30 days)
                created = user_data.get('key_created_at')
                if datetime.now() - created > timedelta(days=30):
                    return jsonify({'error': 'API key expired'}), 401

                return f(*args, **kwargs)

        return jsonify({'error': 'Invalid API key'}), 401

    return decorated
```

### 3. Add Rate Limiting

Track API calls per key and limit requests:

```python
from collections import defaultdict
from datetime import datetime

# Track requests per API key
api_calls = defaultdict(list)  # {api_key: [timestamp1, timestamp2, ...]}

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('x-api-key')

        # Validate API key exists...

        # Rate limiting: Max 10 requests per minute
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Remove old calls
        api_calls[api_key] = [
            call_time for call_time in api_calls[api_key]
            if call_time > minute_ago
        ]

        # Check limit
        if len(api_calls[api_key]) >= 10:
            return jsonify({'error': 'Rate limit exceeded'}), 429

        # Record this call
        api_calls[api_key].append(now)

        return f(*args, **kwargs)

    return decorated
```

### 4. Add Multiple API Keys per User

Allow users to have multiple API keys for different applications:

```python
users = {
    'alice': {
        'password': 'hashed',
        'api_keys': {
            'key1': {'name': 'Mobile App', 'created': datetime.now()},
            'key2': {'name': 'Web Dashboard', 'created': datetime.now()}
        }
    }
}
```

### 5. Add API Key Scopes

Implement permissions for API keys:

```python
users = {
    'alice': {
        'password': 'hashed',
        'api_keys': {
            'key1': {'scopes': ['read', 'write']},
            'key2': {'scopes': ['read']}  # Read-only key
        }
    }
}

def api_key_required(scopes=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('x-api-key')

            # Validate API key and check scopes
            for username, user_data in users.items():
                for key, key_info in user_data['api_keys'].items():
                    if key == api_key:
                        if scopes and not set(scopes).issubset(key_info['scopes']):
                            return jsonify({'error': 'Insufficient permissions'}), 403
                        return f(*args, **kwargs)

            return jsonify({'error': 'Invalid API key'}), 401

        return decorated
    return decorator

# Usage
@app.route('/users', methods=['GET'])
@api_key_required(scopes=['read'])
def get_users():
    ...

@app.route('/users', methods=['POST'])
@api_key_required(scopes=['write'])
def create_user():
    ...
```

---

## When to Use API Keys vs Other Auth Methods

### Use API Keys When:

✅ Building public APIs for third-party developers
✅ Allowing programmatic access (scripts, bots)
✅ Need to revoke access without changing passwords
✅ Want to track usage per application
✅ Building server-to-server communication

### Use Basic Auth When:

✅ Simple admin panels
✅ Internal tools
✅ Temporary authentication
✅ Quick prototypes
✅ API key recovery endpoints

### Use JWT (Next Exercise) When:

✅ Stateless authentication needed
✅ Microservices architecture
✅ Mobile/web applications
✅ Need expiring tokens
✅ Want to embed user data in token

---

## Summary

**Key Takeaways:**

1. **API Keys vs Basic Auth**
   - API keys are persistent tokens
   - Basic Auth sends credentials every request
   - API keys better for public APIs

2. **UUID for Key Generation**
   - Standard library, no installation needed
   - Cryptographically secure
   - Virtually no collision risk

3. **Custom Decorators**
   - Wrap functions to add behavior
   - Use `@wraps(f)` to preserve function metadata
   - Apply with `@decorator_name` above function

4. **Header-based Authentication**
   - API keys typically in headers
   - Use `request.headers.get('header-name')`
   - Headers are case-insensitive

5. **Security Best Practices**
   - Hash passwords, never store plain text
   - API keys should be long and random
   - Always use HTTPS in production
   - Allow key regeneration

**Next Steps:**
- **Exercise 06**: JWT Authentication (stateless tokens)
- **Exercise 07**: Consuming External Public APIs
- **Exercise 08**: CRUD Operations

Good luck! 🔑
