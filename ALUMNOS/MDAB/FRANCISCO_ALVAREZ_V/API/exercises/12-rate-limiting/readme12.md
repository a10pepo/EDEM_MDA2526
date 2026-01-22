# Exercise 12: Rate Limiting and API Security

## Quick Start

```bash
cd exercises/12-rate-limiting
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Objective

Learn to protect your API from abuse using **rate limiting** with Flask-Limiter:

- **Prevent Abuse**: Protect your API from malicious users and bots
- **Resource Management**: Control server load and prevent resource exhaustion
- **Fair Usage**: Ensure all users get fair access to your API
- **Security**: Prevent brute force attacks on authentication endpoints
- **Cost Control**: Limit expensive operations (database queries, external API calls)

## What is Rate Limiting?

**Rate limiting** restricts the number of requests a client can make to your API within a specific time window.

**Real-world examples:**
- **Twitter API**: 300 requests per 15 minutes (free tier)
- **GitHub API**: 60 requests per hour (unauthenticated), 5000/hour (authenticated)
- **Stripe API**: 100 requests per second
- **OpenAI API**: Varies by plan and endpoint

**Why rate limiting matters:**
1. **Prevents DoS attacks**: Malicious users can't overwhelm your server
2. **Stops brute force**: Limits password guessing attempts
3. **Controls costs**: Prevents expensive operations from draining resources
4. **Ensures availability**: Protects the API for all legitimate users
5. **Compliance**: Some regulations require rate limiting (e.g., payment APIs)

## Prerequisites

Before starting this exercise, complete:
- **Exercise 06**: JWT Authentication (this exercise builds on JWT concepts)
- **Exercise 03**: API Fundamentals (understanding HTTP status codes)

## What You'll Learn

1. **Flask-Limiter library**: Industry-standard rate limiting for Flask
2. **Rate limit strategies**:
   - Per IP address (default)
   - Per user (authenticated requests)
   - Per endpoint (different limits for different routes)
3. **HTTP 429 status code**: "Too Many Requests"
4. **Rate limit headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`
5. **Decorator patterns**: `@limiter.limit()`, `@limiter.exempt`
6. **Custom error handlers**: User-friendly rate limit messages
7. **Security best practices**: Protecting sensitive endpoints

## Installation

The exercise requires these dependencies (already in `requirements.txt`):

```txt
Flask==3.0.0
Werkzeug==3.0.1
Flask-JWT-Extended==4.6.0
Flask-Limiter==3.5.0
```

Install them:
```bash
pip install -r requirements.txt
```

## How Flask-Limiter Works

### Basic Concept

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,  # Identify clients by IP address
    default_limits=["200 per day", "50 per hour"]  # Applied to all routes
)
```

**Key components:**
- `key_func`: How to identify clients (IP address, user ID, API key, etc.)
- `default_limits`: Fallback limits applied to all routes unless overridden
- `storage_uri`: Where to store rate limit data (memory, Redis, etc.)

### Rate Limit Syntax

Flask-Limiter uses an intuitive string format:

```python
"5 per minute"     # 5 requests per minute
"100 per hour"     # 100 requests per hour
"1000 per day"     # 1000 requests per day
"1 per second"     # 1 request per second
"10/minute"        # Alternative syntax (same as "10 per minute")
```

**You can combine limits:**
```python
@limiter.limit("5 per minute;100 per hour;1000 per day")
```

This enforces ALL limits simultaneously - whichever is hit first triggers the rate limit.

## Exercise Structure

The provided `app.py` has a partially complete API with TODOs:

- `app.py` - Starter file with blanks to fill in
- `example/example12.py` - Complete reference solution
- `requirements.txt` - Dependencies
- `readme12.md` - This instruction file

## Part 1: Understanding the Code Structure (10 minutes)

### Step 1.1: Review the Setup

Open `app.py` and examine the setup:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=_____,  # TODO: What identifies the client?
    default_limits=_____  # TODO: Set reasonable default limits
)
```

**Your task:**
1. Fill in `key_func` with `get_remote_address` (tracks by IP address)
2. Fill in `default_limits` with `["200 per day", "50 per hour"]`

**Why these defaults?**
- `200 per day`: Prevents a single IP from making thousands of requests
- `50 per hour`: More granular control within the day limit
- Both limits are enforced - hitting either one triggers rate limiting

### Step 1.2: Understand Key Function

The `key_func` parameter determines **who** is making the request.

**Common strategies:**

```python
# Strategy 1: By IP address (simple, works for unauthenticated requests)
from flask_limiter.util import get_remote_address
key_func=get_remote_address

# Strategy 2: By authenticated user (requires JWT/session)
def get_user_id():
    try:
        return get_jwt_identity()  # JWT username
    except:
        return get_remote_address()  # Fall back to IP if not authenticated

key_func=get_user_id
```

For this exercise, we'll use **IP address** since it's simpler and works for both authenticated and unauthenticated endpoints.

## Part 2: Implementing Rate Limits (30 minutes)

### Task 2.1: Protect Registration Endpoint

Registration endpoints are often targeted by bots creating spam accounts.

**Find this code in `app.py`:**

```python
@app.route('/register', methods=['POST'])
@limiter.limit(_____)  # TODO: Add rate limit
def register():
    # ... registration logic
```

**Your task:**
Fill in the blank with: `"5 per hour"`

**Why 5 per hour?**
- Legitimate users rarely need to create multiple accounts
- Prevents automated bot registration
- Still allows a user to retry if they make a mistake

**Testing:**
```bash
# Try registering 6 times in quick succession - the 6th should fail
for i in {1..6}; do
  curl -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"user$i\",\"password\":\"pass123\"}"
  echo ""
done
```

**Expected:** First 5 succeed, 6th returns HTTP 429 (Rate limit exceeded)

### Task 2.2: Protect Login Endpoint

Login endpoints are prime targets for **brute force attacks** (trying many passwords).

**Find this code:**

```python
@app.route('/login', methods=['POST'])
@limiter.limit(_____)  # TODO: Prevent brute force
def login():
    # ... login logic
```

**Your task:**
Fill in: `"10 per minute"`

**Why 10 per minute?**
- Allows legitimate users to retry incorrect passwords
- Prevents automated password guessing
- Industry standard for authentication endpoints

**Real-world comparison:**
- **GitHub**: 5 failed login attempts triggers CAPTCHA
- **AWS**: Throttles after 5 failed attempts
- **Google**: Uses adaptive rate limiting (slows down after failures)

### Task 2.3: General API Endpoint

Most API endpoints need moderate rate limiting.

**Find this code:**

```python
@app.route('/api/data', methods=['GET'])
@jwt_required()
@limiter.limit(_____)  # TODO: Standard API limit
def get_data():
    # ... data retrieval logic
```

**Your task:**
Fill in: `"20 per minute"`

**Why 20 per minute?**
- Allows normal application usage
- Prevents a single user from overwhelming the server
- Balances usability with protection

### Task 2.4: Expensive Operations

Some endpoints are **resource-intensive** (complex database queries, external API calls, AI processing).

**Find this code:**

```python
@app.route('/api/search', methods=['GET'])
@jwt_required()
@limiter.limit(_____)  # TODO: Strict limit for expensive operations
def search():
    # ... expensive search operation
```

**Your task:**
Fill in: `"5 per minute"`

**Why stricter limits?**
- Search often involves database scans or external API calls
- Prevents resource exhaustion
- Encourages efficient client-side caching

**Real examples:**
- **Algolia Search**: 10,000 requests/month (free tier)
- **Elasticsearch**: Often limited to 5-10 concurrent searches
- **OpenAI GPT-4**: 3 requests/minute (free tier)

### Task 2.5: Exempt Endpoints

Some endpoints should **never** be rate limited.

**Find this code:**

```python
@app.route('/api/unlimited', methods=['GET'])
@jwt_required()
_____  # TODO: Exempt from rate limiting
def unlimited():
    # ... critical operation
```

**Your task:**
Add: `@limiter.exempt`

**When to exempt endpoints:**
- Health checks (monitoring systems need reliable access)
- Critical emergency operations (e.g., "delete my account")
- Internal microservice communication
- Webhooks from trusted sources

**Warning:** Use exemptions sparingly - even "unlimited" endpoints can be abused!

## Part 3: Testing Rate Limits (30 minutes)

### Task 3.1: Run the Application

```bash
cd exercises/12-rate-limiting
python app.py
```

You should see:
```
Exercise 12: Rate Limiting and API Security
============================================================
Endpoints:
  POST   /register          - Register new user (5 per hour)
  POST   /login             - Login (10 per minute)
  GET    /api/data          - Get data (20 per minute)
  GET    /api/search?q=...  - Search (5 per minute)
  GET    /api/unlimited     - No rate limit
  ...
```

### Task 3.2: Test Registration Rate Limit

**Step 1: Register a user (should succeed):**
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

**Expected response:**
```json
{
  "message": "User alice registered successfully"
}
```

**Step 2: Try to register 5 more users rapidly:**
```bash
# Windows PowerShell:
for ($i=1; $i -le 5; $i++) {
  curl -X POST http://127.0.0.1:5000/register `
    -H "Content-Type: application/json" `
    -d "{`"username`":`"user$i`",`"password`":`"pass123`"}"
}

# Mac/Linux:
for i in {1..5}; do
  curl -X POST http://127.0.0.1:5000/register \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"user$i\",\"password\":\"pass123\"}"
  echo ""
done
```

**Expected:** After 5 registrations in the same hour, you'll get:
```json
{
  "error": "Rate limit exceeded",
  "message": "5 per 1 hour",
  "retry_after": "Check the Retry-After header"
}
```

**HTTP Status:** `429 Too Many Requests`

### Task 3.3: Inspect Rate Limit Headers

Every response includes rate limit information in the headers.

**Make a request:**
```bash
curl -i http://127.0.0.1:5000/health
```

**Look for these headers:**
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 199
X-RateLimit-Reset: 1704672000
```

**Header meanings:**
- `X-RateLimit-Limit`: Total requests allowed in the window
- `X-RateLimit-Remaining`: Requests left before hitting the limit
- `X-RateLimit-Reset`: Unix timestamp when the limit resets
- `Retry-After`: Seconds to wait before retrying (only on 429 responses)

**Clients should use these headers to:**
1. Display remaining quota to users
2. Automatically retry after the cooldown period
3. Implement exponential backoff

### Task 3.4: Test Login Rate Limit

**Step 1: Login successfully:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

Save the `access_token` from the response.

**Step 2: Simulate brute force attack (11 rapid login attempts):**
```bash
# Windows PowerShell:
for ($i=1; $i -le 11; $i++) {
  Write-Host "Attempt $i"
  curl -X POST http://127.0.0.1:5000/login `
    -H "Content-Type: application/json" `
    -d '{"username":"alice","password":"wrongpassword"}'
}

# Mac/Linux:
for i in {1..11}; do
  echo "Attempt $i"
  curl -X POST http://127.0.0.1:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"wrongpassword"}'
  echo ""
done
```

**Expected:** Attempts 1-10 return 401 (Unauthorized), attempt 11 returns 429 (Rate limit exceeded).

**Security benefit:** An attacker can only try 10 passwords per minute, making brute force impractical.

### Task 3.5: Test Authenticated Endpoints

**Step 1: Login and get a valid token:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

Copy the `access_token`.

**Step 2: Test the `/api/data` endpoint (limit: 20 per minute):**
```bash
# Replace YOUR_TOKEN_HERE with your actual token
TOKEN="YOUR_TOKEN_HERE"

# Windows PowerShell:
for ($i=1; $i -le 21; $i++) {
  Write-Host "Request $i"
  curl http://127.0.0.1:5000/api/data `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
TOKEN="YOUR_TOKEN_HERE"
for i in {1..21}; do
  echo "Request $i"
  curl http://127.0.0.1:5000/api/data \
    -H "Authorization: Bearer $TOKEN"
  echo ""
done
```

**Expected:** Requests 1-20 succeed, request 21 returns 429.

### Task 3.6: Test Expensive Search Endpoint

**Test the strict limit on search (5 per minute):**
```bash
TOKEN="YOUR_TOKEN_HERE"

# Windows PowerShell:
for ($i=1; $i -le 6; $i++) {
  Write-Host "Search $i"
  curl "http://127.0.0.1:5000/api/search?q=test" `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
for i in {1..6}; do
  echo "Search $i"
  curl "http://127.0.0.1:5000/api/search?q=test" \
    -H "Authorization: Bearer $TOKEN"
  echo ""
done
```

**Expected:** Searches 1-5 succeed, search 6 returns 429.

**Note:** The stricter limit (5 vs 20) simulates protecting an expensive operation.

### Task 3.7: Test Exempt Endpoint

**Test the unlimited endpoint:**
```bash
TOKEN="YOUR_TOKEN_HERE"

# Make 100 requests rapidly - all should succeed
# Windows PowerShell:
for ($i=1; $i -le 100; $i++) {
  curl http://127.0.0.1:5000/api/unlimited `
    -H "Authorization: Bearer $TOKEN"
}

# Mac/Linux:
for i in {1..100}; do
  curl http://127.0.0.1:5000/api/unlimited \
    -H "Authorization: Bearer $TOKEN" -s | head -n 1
done
```

**Expected:** All 100 requests succeed - no rate limiting!

## Part 4: Understanding Rate Limit Strategies (20 minutes)

### Strategy 1: Per-IP Rate Limiting (Current Implementation)

**How it works:**
- Tracks requests by the client's IP address
- Uses `get_remote_address()` as the key function

**Pros:**
- Simple to implement
- Works for unauthenticated requests
- Protects against single-source attacks

**Cons:**
- Users behind the same NAT/proxy share the same limit
- Doesn't distinguish between authenticated users from the same IP
- Can block legitimate users in shared networks (offices, universities)

**Use cases:**
- Public endpoints (registration, login)
- Anonymous APIs
- Simple applications

### Strategy 2: Per-User Rate Limiting

**How it works:**
- Tracks requests by authenticated user ID (from JWT)
- Falls back to IP for unauthenticated requests

**Implementation example:**
```python
from flask_jwt_extended import get_jwt_identity

def get_user_key():
    """Use JWT identity if available, otherwise IP address"""
    try:
        identity = get_jwt_identity()
        return identity if identity else get_remote_address()
    except:
        return get_remote_address()

limiter = Limiter(
    app=app,
    key_func=get_user_key,  # Per-user tracking
    default_limits=["1000 per day", "100 per hour"]
)
```

**Pros:**
- Fair limits per user (not per IP)
- Users in shared networks don't affect each other
- Can offer different limits for different user tiers (free vs premium)

**Cons:**
- Requires authentication
- Doesn't protect unauthenticated endpoints
- Users can create multiple accounts to bypass limits

**Use cases:**
- SaaS APIs with user accounts
- Premium/tiered services
- Per-user quota systems

### Strategy 3: Tiered Rate Limiting (Advanced)

**How it works:**
- Different limits based on user role, subscription tier, or API key

**Implementation example:**
```python
from flask import g

def get_rate_limit():
    """Return different limits based on user role"""
    try:
        # Get user role from JWT claims
        claims = get_jwt()
        role = claims.get('role', 'free')

        if role == 'admin':
            return "1000 per hour"
        elif role == 'premium':
            return "500 per hour"
        else:  # free tier
            return "50 per hour"
    except:
        return "10 per hour"  # Unauthenticated users

# Dynamic limit based on user
@app.route('/api/data')
@limiter.limit(get_rate_limit)
def get_data():
    # ...
```

**Use cases:**
- Multi-tier SaaS platforms
- Freemium models
- Enterprise APIs

## Part 5: Best Practices (15 minutes)

### Best Practice 1: Use Different Limits for Different Endpoints

```python
# Generous limit for reading data
@app.route('/api/data', methods=['GET'])
@limiter.limit("100 per minute")

# Strict limit for creating data
@app.route('/api/data', methods=['POST'])
@limiter.limit("10 per minute")

# Very strict for expensive operations
@app.route('/api/export', methods=['GET'])
@limiter.limit("1 per hour")
```

**Why?** Read operations are usually cheaper than writes, and some operations (exports, reports) are very expensive.

### Best Practice 2: Always Include Rate Limit Headers

Clients need to know their quota! Flask-Limiter automatically includes:
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

**Best practice for clients:**
```python
# Pseudo-code for API client
response = make_request()

if response.status == 429:
    retry_after = response.headers['Retry-After']
    sleep(retry_after)
    retry_request()

remaining = response.headers['X-RateLimit-Remaining']
if remaining < 10:
    warn_user("Approaching rate limit")
```

### Best Practice 3: User-Friendly Error Messages

Don't just return "429 Too Many Requests" - explain what happened!

**Good error handler (already in `app.py`):**
```python
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description),  # e.g., "5 per 1 hour"
        'retry_after': 'Check the Retry-After header'
    }), 429
```

**Example response:**
```json
{
  "error": "Rate limit exceeded",
  "message": "5 per 1 hour",
  "retry_after": "Check the Retry-After header"
}
```

### Best Practice 4: Exempt Critical Endpoints

```python
@app.route('/health')
@limiter.exempt  # Monitoring systems need reliable access
def health():
    return {'status': 'ok'}

@app.route('/api/emergency-stop')
@limiter.exempt  # Critical safety operation
@jwt_required()
def emergency_stop():
    # Stop dangerous operation
    pass
```

**When to exempt:**
- Health checks (monitoring)
- Emergency/safety operations
- Internal microservice endpoints (use authentication instead)

### Best Practice 5: Use Redis in Production

For this exercise, we use in-memory storage:
```python
limiter = Limiter(
    app=app,
    storage_uri="memory://"  # Simple, but doesn't scale
)
```

**In production, use Redis:**
```python
limiter = Limiter(
    app=app,
    storage_uri="redis://localhost:6379"  # Shared across multiple servers
)
```

**Why Redis?**
- Shared rate limit counters across multiple API servers
- Persistent across app restarts
- Fast and reliable
- Industry standard

### Best Practice 6: Log Rate Limit Violations

Add logging to detect abuse:

```python
from flask import request
import logging

@app.errorhandler(429)
def ratelimit_handler(e):
    # Log the violation
    logging.warning(
        f"Rate limit exceeded: IP={request.remote_addr}, "
        f"Path={request.path}, Limit={e.description}"
    )

    return jsonify({
        'error': 'Rate limit exceeded',
        'message': str(e.description)
    }), 429
```

**Use logs to:**
- Identify abusive IPs
- Detect bot traffic
- Optimize rate limits based on real usage patterns

## Testing Checklist

**Basic Setup:**
- [ ] Flask-Limiter installed (`pip install -r requirements.txt`)
- [ ] App runs without errors (`python app.py`)
- [ ] Health check endpoint accessible (`/health`)

**Rate Limit Implementation:**
- [ ] Limiter initialized with `get_remote_address` and default limits
- [ ] Registration endpoint limited to "5 per hour"
- [ ] Login endpoint limited to "10 per minute"
- [ ] Data endpoint limited to "20 per minute"
- [ ] Search endpoint limited to "5 per minute"
- [ ] Unlimited endpoint marked with `@limiter.exempt`

**Testing:**
- [ ] Registration limit enforced (6th attempt in an hour fails)
- [ ] Login limit enforced (11th attempt in a minute fails)
- [ ] Data endpoint limit enforced (21st request fails)
- [ ] Search limit enforced (6th search fails)
- [ ] Unlimited endpoint has no limit (100+ requests succeed)
- [ ] Rate limit headers present in responses
- [ ] 429 status code returned when limit exceeded
- [ ] Custom error handler returns JSON response

**Understanding:**
- [ ] Can explain when to use rate limiting
- [ ] Understands different rate limit strategies (per-IP vs per-user)
- [ ] Knows when to exempt endpoints
- [ ] Can choose appropriate limits for different operations

## Common Issues and Solutions

### Issue 1: Rate Limit Not Working

**Symptom:** Can make unlimited requests without getting 429 errors.

**Possible causes:**
1. **Decorator order matters:**
   ```python
   # WRONG - limiter runs before JWT, so unauthenticated requests pass
   @jwt_required()
   @limiter.limit("5 per minute")
   def endpoint():
       pass

   # CORRECT - limiter runs first
   @limiter.limit("5 per minute")
   @jwt_required()
   def endpoint():
       pass
   ```

2. **Endpoint marked as exempt:**
   Check if `@limiter.exempt` is applied (intentionally or by mistake).

3. **Limits too generous:**
   "1000 per minute" won't trigger during manual testing - use small limits for testing.

### Issue 2: Rate Limit Resets Too Quickly

**Symptom:** After hitting the limit, it resets immediately instead of waiting the full window.

**Cause:** Restarting the Flask app clears in-memory rate limit counters.

**Solution:** This is expected behavior with `memory://` storage. In production, use Redis for persistent counters.

### Issue 3: Multiple Users from Same IP Share Limit

**Symptom:** Two users on the same network (office, university) share the same rate limit.

**Cause:** Using `get_remote_address()` (IP-based) instead of per-user tracking.

**Solution:** Implement per-user rate limiting (see Part 4, Strategy 2).

### Issue 4: Rate Limit Headers Not Showing

**Symptom:** No `X-RateLimit-*` headers in responses.

**Cause:** Flask-Limiter automatically adds headers, but they may not show in all clients.

**Solution:** Use `curl -i` or check browser DevTools Network tab to see headers.

### Issue 5: "429 Too Many Requests" for Health Checks

**Symptom:** Monitoring system gets 429 errors when checking `/health`.

**Solution:** Exempt the health check endpoint:
```python
@app.route('/health')
@limiter.exempt
def health():
    return {'status': 'ok'}
```

## Real-World Rate Limiting Examples

### Example 1: GitHub API

**Free tier (unauthenticated):**
- 60 requests per hour

**Authenticated:**
- 5,000 requests per hour

**Search API (special limit):**
- 10 requests per minute (stricter because search is expensive)

**How they communicate limits:**
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1704672000
X-RateLimit-Resource: core
```

### Example 2: Twitter API v2

**Free tier:**
- 500,000 Tweets read per month
- 1,667 Tweets per hour

**Basic tier ($100/month):**
- 10,000,000 Tweets per month

**How they enforce:**
- Returns 429 with `x-rate-limit-reset` header
- Clients must wait until reset time before retrying

### Example 3: Stripe API

**Limits:**
- 100 read requests per second
- 100 write requests per second (stricter in practice)

**Special handling:**
- Payment endpoints have stricter limits
- Test mode has separate limits from live mode

**How they handle overages:**
- 429 status code
- Exponential backoff recommended
- SDKs automatically retry with backoff

## Beyond This Exercise

### Next Steps

1. **Exercise 13+**: Apply rate limiting to your final project API
2. **Production deployment**: Configure Redis for rate limit storage
3. **Monitoring**: Set up alerts for rate limit violations
4. **Analytics**: Track API usage patterns to optimize limits

### Advanced Topics (Beyond This Course)

1. **Distributed Rate Limiting**:
   - Redis Cluster for high-availability
   - Consistent hashing for sharding

2. **Adaptive Rate Limiting**:
   - Increase limits for trusted users
   - Decrease limits for suspicious IPs
   - Machine learning-based anomaly detection

3. **Token Bucket Algorithm**:
   - More sophisticated than fixed windows
   - Allows burst traffic
   - Refills at a steady rate

4. **Geographic Rate Limiting**:
   - Different limits by region
   - Stricter limits for high-risk countries
   - GeoIP-based blocking

5. **Cost-Based Rate Limiting**:
   - Assign "cost" to each endpoint
   - Track total cost instead of request count
   - Example: 1 search = 5 points, 1 read = 1 point

## Additional Resources

### Official Documentation
- **[Flask-Limiter Docs](https://flask-limiter.readthedocs.io/)** - Complete library reference
- **[RFC 6585](https://tools.ietf.org/html/rfc6585)** - HTTP 429 status code specification
- **[Redis](https://redis.io/)** - In-memory data store for production

### Tutorials
- [Rate Limiting Best Practices](https://nordicapis.com/everything-you-need-to-know-about-api-rate-limiting/)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

### Alternative Libraries
- **[django-ratelimit](https://django-ratelimit.readthedocs.io/)** - For Django applications
- **[express-rate-limit](https://github.com/nfriedly/express-rate-limit)** - For Node.js/Express

## Deliverables

When you complete this exercise, you should have:

1. **Completed `app.py`**:
   - All TODOs filled in correctly
   - Limiter initialized with proper key function and defaults
   - All endpoints have appropriate rate limits
   - Exempt endpoint configured

2. **Testing Evidence**:
   - Screenshots or logs showing rate limit enforcement
   - 429 responses when limits exceeded
   - Rate limit headers in successful responses

3. **Understanding**:
   - Explain why different endpoints have different limits
   - Describe when to use per-IP vs per-user rate limiting
   - Identify appropriate limits for your own API projects

## Questions to Consider

1. Why is the login endpoint more strictly limited than the data endpoint?
2. What would happen if you used per-user rate limiting for the `/register` endpoint?
3. How would you implement different rate limits for free vs premium users?
4. When would you exempt an endpoint from rate limiting? What are the risks?
5. How do rate limit headers help API clients implement better retry logic?
6. What's the difference between rate limiting and throttling?

Good luck protecting your APIs! 🛡️
