# Exercise 6: Authentication with JSON Web Tokens (JWT)

## Objective

Learn how to implement **stateless authentication** using JSON Web Tokens (JWT) in a REST API with Flask. Understand why JWT is the preferred authentication method for modern APIs and how it differs from Basic Authentication.

## Quick Start

```bash
cd exercises/06-jwt-auth
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app_improved.py
```

---

## What is JWT Authentication?

### The Problem with Basic Auth

In Exercise 04, you learned Basic Authentication where:
- Client sends **username and password with EVERY request**
- Credentials are Base64 encoded (not encrypted!)
- Server must verify credentials on every request
- Credentials travel over the network constantly (security risk)

### The JWT Solution

**JWT (JSON Web Token)** provides **stateless authentication**:
1. Client sends username/password **ONCE** to `/login`
2. Server validates and returns a **signed token** (JWT)
3. Client stores the token and sends it with all future requests
4. Server validates the token signature (no database lookup needed!)
5. **No more sending passwords over the network after login**

### JWT Structure

A JWT token has three parts separated by dots:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTY3ODg4ODg4OH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
│                                      │                                      │
│                                      │                                      └─ Signature (verifies token hasn't been tampered with)
│                                      └─ Payload (user identity, expiration, etc.)
└─ Header (algorithm and token type)
```

**Key Concepts:**
- **Self-contained**: Contains all user info needed (no database lookup)
- **Stateless**: Server doesn't store sessions
- **Signed**: Server can verify it wasn't modified
- **Expiration**: Tokens expire after a set time (default 15 minutes)

---

## API Structure

### Public Endpoints (No Authentication)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user account |
| POST | `/login` | Login with credentials, get JWT token |

### Protected Endpoints (JWT Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/profile` | Get current user's profile information |
| GET | `/users` | Get list of all users |
| GET | `/protected` | Example protected resource |

---

## How JWT Authentication Works

### Step-by-Step Flow

```
1. User Registration
   Client                    Server
     |                         |
     |  POST /register         |
     |  {username, password}   |
     |------------------------>|
     |                         | • Validate input
     |                         | • Hash password
     |                         | • Store user
     |  201 Created            |
     |<------------------------|

2. User Login (Get Token)
   Client                    Server
     |                         |
     |  POST /login            |
     |  {username, password}   |
     |------------------------>|
     |                         | • Validate credentials
     |                         | • Generate JWT token
     |                         | • Sign token with secret
     |  200 OK                 |
     |  {access_token: "..."}  |
     |<------------------------|
     | Store token locally     |

3. Access Protected Resource
   Client                    Server
     |                         |
     | GET /profile            |
     | Authorization: Bearer   |
     | <token>                 |
     |------------------------>|
     |                         | • Verify token signature
     |                         | • Extract user identity
     |                         | • Return resource
     |  200 OK                 |
     |  {user data}            |
     |<------------------------|
```

---

## Implementation Details

### 1. JWT Configuration

```python
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change in production!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token lifetime

jwt = JWTManager(app)
```

### 2. User Registration (Public)

```python
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Store user with hashed password
    users[username] = {
        'password': generate_password_hash(password)
    }
    return jsonify({'message': 'User registered'}), 201
```

### 3. Login Endpoint (Public)

**This is where JWT differs from Basic Auth!**

```python
@app.route('/login', methods=['POST'])
def login():
    # Get credentials from REQUEST BODY, not Authorization header
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Manually validate credentials
    if username in users and check_password_hash(users[username]['password'], password):
        # Generate JWT token with user identity
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
```

**Key Differences from Exercise 04:**
- ❌ NO `@auth.login_required` decorator
- ❌ NO HTTP Basic Auth header
- ✅ Credentials sent in JSON body
- ✅ Returns JWT token instead of session

### 4. Protected Endpoints (JWT Required)

```python
@app.route('/profile', methods=['GET'])
@jwt_required()  # ← Validates JWT token
def profile():
    # Extract user identity from token
    current_user = get_jwt_identity()
    return jsonify({'username': current_user}), 200
```

**How `@jwt_required()` works:**
1. Extracts token from `Authorization: Bearer <token>` header
2. Verifies token signature using JWT_SECRET_KEY
3. Checks token hasn't expired
4. Makes user identity available via `get_jwt_identity()`

---

## Testing the API

### 1. Register a User

```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
```

**Expected Response:**
```json
{
  "message": "User registered successfully",
  "username": "alice"
}
```

### 2. Login and Get JWT Token

```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
```

**Expected Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

**Save the token** - you'll need it for the next requests!

### 3. Access Protected Endpoint with Token

Replace `<YOUR_TOKEN>` with the actual token from step 2:

```bash
curl -X GET http://127.0.0.1:5000/profile \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Expected Response:**
```json
{
  "username": "alice",
  "profile": "Profile information for alice",
  "account_created": "2025-01-01"
}
```

### 4. Try WITHOUT Token (Should Fail)

```bash
curl -X GET http://127.0.0.1:5000/profile
```

**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```

### 5. Get All Users (Protected)

```bash
curl -X GET http://127.0.0.1:5000/users \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## Understanding JWT Tokens

### Inspecting Your Token

1. Copy the `access_token` from your `/login` response
2. Go to [https://jwt.io/](https://jwt.io/)
3. Paste your token in the "Encoded" field
4. See the decoded payload:

```json
{
  "sub": "alice",           // Subject (user identity)
  "exp": 1678888888,        // Expiration timestamp
  "iat": 1678885288,        // Issued at timestamp
  "type": "access"          // Token type
}
```

**Important:** The token is **signed**, not **encrypted**:
- ✅ Server can verify it hasn't been tampered with
- ❌ Anyone can read the contents (don't put secrets in JWT!)
- ✅ If someone modifies the payload, signature verification fails

---

## JWT vs Basic Auth Comparison

| Feature | Basic Auth (Exercise 04) | JWT (Exercise 06) |
|---------|--------------------------|-------------------|
| **Credentials sent** | Every request | Only at login |
| **Stateful/Stateless** | Stateless (but less secure) | Stateless |
| **Server-side storage** | No sessions | No sessions |
| **Database lookup** | Every request | Only at login |
| **Scalability** | Good | Excellent |
| **Security** | Base64 (not secure) | Signed tokens |
| **Token expiration** | No | Yes (automatic) |
| **Mobile/SPA friendly** | Not ideal | Perfect |
| **Use case** | Simple APIs, testing | Production APIs |

### When to Use Each

**Basic Auth:**
- Internal tools
- Quick prototypes
- Development/testing
- Simple server-to-server APIs

**JWT:**
- Production web applications
- Mobile apps
- Single Page Applications (React, Vue, Angular)
- Microservices architecture
- APIs accessed by multiple clients

---

## Security Best Practices

### ✅ DO

1. **Use HTTPS in production** - Tokens can be intercepted on HTTP
2. **Set short expiration times** - Default 15 minutes is good
3. **Store tokens securely**:
   - Web: `httpOnly` cookies (prevents XSS)
   - Mobile: Secure storage (Keychain, KeyStore)
   - NOT in localStorage (vulnerable to XSS)
4. **Use strong secret keys** - Random, long, environment variable
5. **Implement refresh tokens** - For longer sessions without re-login
6. **Validate all inputs** - Check username/password format

### ❌ DON'T

1. **Don't put sensitive data in JWT** - Anyone can decode it
2. **Don't use weak secrets** - Makes tokens easy to forge
3. **Don't skip HTTPS** - Tokens can be stolen
4. **Don't make tokens valid forever** - Security risk
5. **Don't store passwords in plain text** - Always hash

---

## Common Errors and Solutions

### 1. Missing Authorization Header

```json
{"msg": "Missing Authorization Header"}
```

**Solution:** Add header to request:
```bash
-H "Authorization: Bearer <token>"
```

### 2. Invalid Token

```json
{"msg": "Signature verification failed"}
```

**Causes:**
- Token was modified
- Wrong JWT_SECRET_KEY
- Token was generated by different server

### 3. Expired Token

```json
{"msg": "Token has expired"}
```

**Solution:** Login again to get a new token

### 4. Malformed Token

```json
{"msg": "Not enough segments"}
```

**Cause:** Token format is wrong
**Solution:** Ensure format is `Bearer <token>`, not just `<token>`

---

## Acceptance Criteria

Your implementation should:

- ✅ Allow user registration via POST `/register`
- ✅ Accept login credentials in JSON body (not Authorization header)
- ✅ Return a valid JWT token on successful login
- ✅ Protect routes with `@jwt_required()` decorator
- ✅ Extract user identity with `get_jwt_identity()`
- ✅ Return 401 for invalid credentials
- ✅ Return 401 for missing/invalid JWT tokens
- ✅ Hash passwords before storage
- ✅ Use consistent error response format

---

## Stretch Goals

Once you complete the basic implementation:

1. **Add Token Expiration Configuration**
   ```python
   app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
   ```

2. **Implement Refresh Tokens** (Advanced)
   ```python
   from flask_jwt_extended import create_refresh_token, jwt_required, get_jwt_identity

   @app.route('/refresh', methods=['POST'])
   @jwt_required(refresh=True)
   def refresh():
       current_user = get_jwt_identity()
       new_token = create_access_token(identity=current_user)
       return jsonify({'access_token': new_token}), 200
   ```

3. **Add User Logout** (Token Blacklisting)
   - Maintain a blacklist of revoked tokens
   - Check blacklist in `@jwt_required()` callback

4. **Add User Profile Update**
   ```python
   @app.route('/profile', methods=['PUT'])
   @jwt_required()
   def update_profile():
       # Update user data
   ```

5. **Add Password Change Endpoint**
   - Require current password for verification
   - Hash new password before storing

---

## Next Steps

**Exercise 07:** Learn to consume external APIs (weather, GitHub, etc.)

**Exercise 10:** Add **Authorization** (roles and permissions) to your JWT tokens
- Current exercise: **Authentication** (who you are)
- Exercise 10: **Authorization** (what you can do)
- JWT will include role claims (admin, user, etc.)

---

## Additional Resources

- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [JWT.io](https://jwt.io/) - Decode and inspect tokens
- [RFC 7519 - JWT Specification](https://tools.ietf.org/html/rfc7519)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

## Summary

**Key Takeaways:**

1. **JWT = Stateless Authentication**
   - Send credentials once, get token
   - Use token for all subsequent requests
   - No server-side sessions needed

2. **JWT Structure**
   - Header + Payload + Signature
   - Signed (verifiable) but not encrypted (readable)
   - Contains user identity and expiration

3. **Best Practice Flow**
   - POST /login with JSON body → get JWT
   - Store JWT securely
   - Send JWT in Authorization header: `Bearer <token>`
   - All protected routes use `@jwt_required()`

4. **Security**
   - Use HTTPS in production
   - Short token expiration
   - Strong secret keys
   - Never put sensitive data in JWT payload

5. **Authentication ≠ Authorization**
   - This exercise: Who are you? (Authentication)
   - Exercise 10: What can you do? (Authorization with roles)

Good luck! 🚀
