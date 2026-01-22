# Exercise 11: Exposing Your API Publicly with ngrok and GitHub Webhooks

## Introduction

In this exercise, you'll learn how to expose your local Flask API to the internet using **ngrok** and configure **real GitHub webhooks**. This is essential for:
- Receiving webhook notifications from GitHub when code is pushed
- Sharing your API with team members without deploying
- Understanding how services communicate via webhooks
- Learning production webhook patterns used in CI/CD systems

## Learning Objectives

By the end of this exercise, you will be able to:

1. Install and configure ngrok on your system (verified 2025)
2. Expose a local Flask API to a public HTTPS URL
3. Configure real GitHub webhooks in repository settings
4. Implement webhook endpoints that handle authentic GitHub payloads
5. Use ngrok's dashboard for request inspection and debugging
6. Apply webhook security best practices (signature verification)
7. Collaborate with teammates by sharing ngrok URLs

## What is ngrok?

**ngrok** is a tool that creates a secure tunnel from a public URL to your local development server. It provides:
- A public HTTPS URL that forwards to localhost
- A web dashboard showing all HTTP requests in real-time
- Request inspection and replay capabilities
- Free tier with essential features (perfect for learning)

**Official site:** https://ngrok.com

**Use Cases:**
- **GitHub Webhooks**: Receive push notifications from GitHub to your local Flask app
- **Team collaboration**: Share your API during the ProManage project without deployment
- **CI/CD Development**: Build automated workflows triggered by GitHub events
- **Microservices Testing**: Test service-to-service communication locally

## Prerequisites

Before starting this exercise, you should have completed:
- **Exercise 03**: API Fundamentals (understanding basic Flask apps)
- **Exercise 06**: JWT Authentication (optional, but recommended)

## Installation

### Step 1: Download ngrok

**Windows:**
1. Visit [ngrok.com/download](https://ngrok.com/download)
2. Download the Windows ZIP file
3. Extract `ngrok.exe` to a folder (e.g., `C:\ngrok\`)
4. Add to PATH (optional but recommended):
   - Open "Environment Variables" in System Settings
   - Edit "Path" variable
   - Add `C:\ngrok\` (or your chosen location)
   - Restart terminal

**Mac (with Homebrew):**
```bash
brew install ngrok/ngrok/ngrok
```

**Linux:**
```bash
# Download
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

**Verify Installation:**
```bash
ngrok version
# Should show: ngrok version 3.x.x
```

### Step 2: Sign Up for ngrok Account (Free)

1. Go to [ngrok.com/signup](https://ngrok.com/signup)
2. Create a free account (required - no credit card needed)
3. Verify your email address

**Free tier includes:**
- 1 online ngrok process
- 40 connections/minute
- HTTPS tunnels
- Request inspection

### Step 3: Authenticate ngrok (Updated 2025)

1. Log in to [dashboard.ngrok.com](https://dashboard.ngrok.com)
2. Navigate to "Getting Started" → "Your Authtoken"
3. Copy your authtoken
4. Run in terminal:
   ```bash
   ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
   ```

**Example:**
```bash
ngrok config add-authtoken 2bXjYZ1234abcd5678efgh_9IJKLMnopqrstuvwxyz
```

This saves your token to the ngrok configuration file:
- **Mac/Linux**: `~/.ngrok2/ngrok.yml`
- **Windows**: `%USERPROFILE%\.ngrok2\ngrok.yml`

## Quick Start

### Run a Basic Flask App

```bash
cd exercises/11-ngrok-public-api
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install flask
python app.py
```

Your app runs at `http://127.0.0.1:5000`

### Expose with ngrok

**Open a new terminal** (keep Flask running) and run:
```bash
ngrok http 5000
```

You'll see output like:
```
ngrok

Session Status                online
Account                       your-email@example.com (Plan: Free)
Version                       3.5.0
Region                        United States (us)
Latency                       25ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abcd-1234-5678-efgh.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Your public URL**: `https://abcd-1234-5678-efgh.ngrok-free.app`

Anyone can now access your API at this URL!

### Test It

```bash
# From anywhere (your phone, another computer, etc.)
curl https://abcd-1234-5678-efgh.ngrok-free.app/health
```

## Exercise Structure

This exercise provides:
- `app.py` - Starter Flask app with TODOs for webhook implementation
- `example/example11.py` - Complete reference solution
- `readme11.md` - This instruction file

## Part 1: Basic Exposure (15 minutes)

### Task 1.1: Run the Sample App

The provided `app.py` has a basic API with health check and user endpoints.

```bash
python app.py
```

Visit `http://localhost:5000/health` - should return `{"status": "ok"}`

### Task 1.2: Expose with ngrok

In a **new terminal**:
```bash
ngrok http 5000
```

Copy your public URL (the `https://....ngrok-free.app` address).

### Task 1.3: Test Public Access

From your browser or curl:
```bash
curl https://YOUR-NGROK-URL.ngrok-free.app/health
```

**Expected Result**: Same response as localhost

### Task 1.4: Explore ngrok Dashboard

Open `http://localhost:4040` in your browser.

You'll see:
- List of all HTTP requests
- Request/response details (headers, body, status)
- Ability to replay requests
- Connection statistics

Try making several requests and watch them appear in real-time.

## Part 2: Real GitHub Webhook Setup (45 minutes)

This is the core of the exercise. You'll configure a **real GitHub webhook** that triggers when you push code.

### Task 2.1: Create or Choose a GitHub Repository

**Option A - Create New Test Repo:**
1. Go to [github.com/new](https://github.com/new)
2. Name it `api-webhook-test` (or anything you like)
3. Make it **Public** (required for free webhooks)
4. Initialize with a README
5. Create repository

**Option B - Use Existing Repo:**
- Any public repo you own will work
- You'll need admin access to configure webhooks

### Task 2.2: Complete the GitHub Webhook Endpoint

In `app.py`, complete the webhook endpoint to handle **real GitHub payloads**:

```python
@app.route('/webhooks/github', methods=['_____'])  # TODO: Which HTTP method?
# Hint: POST
def github_webhook():
    """
    Receives REAL push events from GitHub.

    GitHub sends webhooks when events occur in your repository.
    The payload structure is defined by GitHub's API.
    """
    # TODO: Get the JSON payload
    # Hint: Use request.get_json()
    data = _____

    if not data:
        return jsonify({'error': 'Invalid payload'}), 400

    # Real GitHub payload structure:
    # {
    #   "ref": "refs/heads/main",
    #   "repository": {"name": "...", "full_name": "user/repo"},
    #   "pusher": {"name": "...", "email": "..."},
    #   "commits": [{"id": "...", "message": "...", "author": {...}}, ...]
    # }

    # TODO: Extract repository info
    # Hint: data.get('repository', {})
    repository = _____
    repo_name = repository.get('full_name', 'unknown') if repository else 'unknown'

    # TODO: Extract pusher info (who pushed the code)
    # Hint: data.get('pusher', {})
    pusher = _____
    pusher_name = pusher.get('name', 'unknown') if pusher else 'unknown'

    # TODO: Extract commits list
    # Hint: data.get('commits', [])
    commits = _____

    # TODO: Extract ref (which branch was pushed)
    # Hint: data.get('ref', 'unknown')
    ref = _____

    # Log the webhook
    print(f"\n{'='*60}")
    print(f"🎉 REAL GitHub Webhook Received!")
    print(f"📦 Repository: {repo_name}")
    print(f"👤 Pushed by: {pusher_name}")
    print(f"🌿 Branch: {ref}")
    print(f"📝 Commits: {len(commits)}")

    for i, commit in enumerate(commits, 1):
        commit_msg = commit.get('message', 'No message')
        commit_id = commit.get('id', 'unknown')[:7]  # Short SHA
        print(f"   {i}. [{commit_id}] {commit_msg}")

    print(f"{'='*60}\n")

    # Store the event (optional - for viewing later)
    webhook_events.append({
        'type': 'github',
        'repository': repo_name,
        'pusher': pusher_name,
        'ref': ref,
        'commits_count': len(commits)
    })

    # TODO: Return success response
    # Hint: GitHub expects 200 status
    return jsonify({'status': 'received'}), _____
```

### Task 2.3: Run Your Flask App and ngrok

**Terminal 1 - Flask:**
```bash
cd exercises/11-ngrok-public-api
python app.py
```

**Terminal 2 - ngrok:**
```bash
ngrok http 5000
```

**Copy your ngrok URL** from the output:
```
Forwarding    https://abc123-xyz.ngrok-free.app -> http://localhost:5000
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
              Copy this URL!
```

### Task 2.4: Configure GitHub Webhook

1. **Go to your repository on GitHub**
   - Navigate to `https://github.com/YOUR-USERNAME/YOUR-REPO`

2. **Open Settings → Webhooks**
   - Click the repository **Settings** tab (top right)
   - Scroll down and click **Webhooks** in the left sidebar
   - Click **Add webhook** button

3. **Configure the Webhook**
   - **Payload URL**: `https://YOUR-NGROK-URL.ngrok-free.app/webhooks/github`
     - Example: `https://abc123-xyz.ngrok-free.app/webhooks/github`
     - ⚠️ Make sure to include `/webhooks/github` at the end!

   - **Content type**: Select `application/json`

   - **Secret**: Leave empty for now (we'll discuss security later)

   - **Which events?**: Select "Just the push event"

   - **Active**: Check this box ✅

   - Click **Add webhook**

4. **Verify Setup**
   - GitHub will immediately send a test "ping" event
   - Check your Flask terminal - you should see a request logged
   - In GitHub, scroll down to "Recent Deliveries" - should show green checkmark ✅

**Common Issue**: If you see a red X, check:
- Is Flask running?
- Is ngrok running?
- Did you copy the correct ngrok URL?
- Did you include `/webhooks/github` in the path?

### Task 2.5: Trigger the Webhook with a Real Push

Now for the magic moment! Make a change to your repository:

**Method 1 - GitHub Web Interface (easiest):**
1. Go to your repo on GitHub
2. Click on `README.md`
3. Click the pencil icon (Edit)
4. Add a line: `Testing webhook at [current time]`
5. Scroll down, click **Commit changes**
6. Click **Commit changes** again

**Watch your Flask terminal** - you should see:
```
============================================================
🎉 REAL GitHub Webhook Received!
📦 Repository: your-username/api-webhook-test
👤 Pushed by: your-username
🌿 Branch: refs/heads/main
📝 Commits: 1
   1. [a1b2c3d] Update README.md
============================================================
```

**Method 2 - Git Command Line (if you have git):**
```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
echo "Test webhook $(date)" >> README.md
git add README.md
git commit -m "Test webhook trigger"
git push
```

### Task 2.6: Inspect the Webhook in ngrok Dashboard

1. Open `http://localhost:4040` in your browser
2. You'll see the POST request from GitHub
3. Click on it to see:
   - Full headers (including GitHub-specific headers)
   - Complete JSON payload
   - Your response (200 OK)

**This is extremely useful for debugging webhooks!**

### Task 2.7: View All Received Webhooks

Your app stores webhook events. Check them:

```bash
curl https://YOUR-NGROK-URL.ngrok-free.app/webhooks/events
```

You'll see all GitHub events you've received.

## Part 3: Team Collaboration (20 minutes)

Now that you understand webhooks, practice sharing your API with teammates (essential for ProManage project!).

### Task 3.1: Share Your API

1. Ensure your Flask app and ngrok are running
2. Share your ngrok URL with a classmate: `https://your-url.ngrok-free.app`
3. Have them test your `/health` and `/info` endpoints

### Task 3.2: Call a Teammate's API

1. Get a teammate's ngrok URL
2. Test their endpoints:
   ```bash
   # Health check
   curl https://their-ngrok-url.ngrok-free.app/health

   # See request info
   curl https://their-ngrok-url.ngrok-free.app/info

   # Create a user on their API
   curl -X POST https://their-ngrok-url.ngrok-free.app/users \
     -H "Content-Type: application/json" \
     -d '{"username": "yourname", "email": "you@example.com"}'
   ```

### Task 3.3: Cross-Team Webhook Testing

**Advanced collaboration**: Configure your GitHub webhook to notify your teammate when you push!

1. Teammate shares their ngrok URL
2. In **your** GitHub repo settings:
   - Add a **second webhook**
   - Use your teammate's URL: `https://their-url.ngrok-free.app/webhooks/github`
3. Make a commit to **your** repo
4. Your teammate's Flask app receives the notification!

**This demonstrates microservices communication** - one service notifying another service about events.

**Note**: This exercise prepares you for Exercise 13 (ProManage) where you'll use ngrok to share APIs with team members!

## Part 4: Webhook Security (20 minutes)

**IMPORTANT**: The basic webhook we created is **not secure**. Anyone with your ngrok URL could send fake webhooks!

### Task 4.1: Understanding Webhook Signatures

Real webhook providers like GitHub include a **signature** in the headers to prove authenticity.

**How GitHub webhook signatures work:**
1. You set a secret key when configuring the webhook in GitHub
2. GitHub creates a hash of the payload using your secret
3. GitHub sends the hash in the `X-Hub-Signature-256` header
4. Your app recalculates the hash and compares
5. If they match → legitimate webhook from GitHub. If not → reject it as fake.

### Task 4.2: Add GitHub Webhook Secret (Optional)

Let's secure your GitHub webhook:

**Step 1: Generate a Secret**
```bash
# On Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# On Mac/Linux
openssl rand -base64 32
```

Copy the output (example: `dGhpc2lzYXNlY3JldGtleQ==`)

**Step 2: Update GitHub Webhook**
1. Go to your repo → Settings → Webhooks
2. Click "Edit" on your webhook
3. In the **Secret** field, paste your secret
4. Click "Update webhook"

**Step 3: Verify Signature in Your App**

Add this to `app.py` (above the `github_webhook` function):

```python
import hmac
import hashlib

GITHUB_WEBHOOK_SECRET = "dGhpc2lzYXNlY3JldGtleQ=="  # Your secret here

def verify_github_signature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub"""
    if not signature_header:
        return False

    # GitHub sends: sha256=<hash>
    hash_algorithm, github_signature = signature_header.split('=')

    # Calculate expected signature
    expected_signature = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, github_signature)
```

**Step 4: Use Verification in Webhook**

Update your `github_webhook` function:

```python
@app.route('/webhooks/github', methods=['POST'])
def github_webhook():
    # Verify signature before processing
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_github_signature(request.data, signature):
        print("⚠️  Invalid signature - rejecting webhook")
        return jsonify({'error': 'Invalid signature'}), 401

    # Now safe to process...
    data = request.get_json()
    # ... rest of your code
```

**Test it**: Make a commit. If it works, your signature verification is correct! 🎉

### Task 4.3: Request Inspection and Replay

The ngrok dashboard is incredibly useful:

1. Open `http://localhost:4040`
2. Make a commit to trigger GitHub webhook
3. Click on the webhook request in the dashboard
4. Inspect:
   - **Headers**: See `X-Hub-Signature-256` and other GitHub headers
   - **Raw payload**: See the exact JSON GitHub sent
   - **Your response**: Confirm you returned 200
5. Click **Replay**: Resends the exact same request (useful for debugging)


## Security Best Practices

### ⚠️ Important Security Warnings

1. **Never expose production databases or sensitive data**
   - ngrok URLs are public - anyone can find them
   - Free tier URLs are not protected by authentication
   - Only expose development/test environments

2. **URLs are temporary**
   - Free tier URLs change every time you restart ngrok
   - Don't hard-code ngrok URLs in your code
   - Use environment variables for URLs

3. **Validate webhook signatures**
   - Always verify GitHub webhook signatures in production
   - See Part 4 for implementation details
   - Example:
     ```python
     # GitHub webhook signature verification
     import hmac
     import hashlib

     def verify_github_signature(payload_body, signature_header, secret):
         hash_algorithm, github_signature = signature_header.split('=')
         expected = hmac.new(
             secret.encode(),
             msg=payload_body,
             digestmod=hashlib.sha256
         ).hexdigest()
         return hmac.compare_digest(expected, github_signature)
     ```

4. **Rate limiting**
   - Add rate limiting to prevent abuse
   - Use Flask-Limiter (see future exercises)

5. **Environment variables**
   - Never commit ngrok URLs or authtokens to Git
   - Use `.env` files (add to `.gitignore`)

### Recommended Practices

```python
import os
from dotenv import load_dotenv

load_dotenv()

# In your webhook handlers
GITHUB_WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')

@app.route('/webhooks/github', methods=['POST'])
def github_webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_github_signature(request.data, signature, GITHUB_WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401
    # Process webhook...
```

## Common Issues and Solutions

### Issue 1: "ERR_NGROK_108 - You must sign up"
**Solution:** Create free account at ngrok.com and add authtoken

### Issue 2: ngrok URL returns "Invalid Host header"
**Solution:** Some frameworks check Host header. For Flask, this shouldn't happen. For other frameworks, configure allowed hosts.

### Issue 3: Can't access from mobile device
**Solution:**
- Ensure you're using the HTTPS URL (not HTTP localhost)
- Check if mobile device has internet connection
- Try accessing from mobile browser first

### Issue 4: Connection timed out
**Solution:**
- Ensure Flask app is actually running
- Confirm ngrok is pointing to correct port (5000)
- Check firewall settings

### Issue 5: "ERR_NGROK_3200 - Tunnel Limit Reached"
**Solution:** Free plan allows 1 tunnel. Close other ngrok processes with `Ctrl+C`

## Testing Checklist

**Part 1: Basic Setup**
- [ ] ngrok installed and authenticated
- [ ] Flask app runs on localhost:5000
- [ ] ngrok exposes app successfully
- [ ] Public URL accessible from browser
- [ ] Public URL accessible from curl
- [ ] ngrok dashboard shows requests (localhost:4040)

**Part 2: GitHub Webhook**
- [ ] Created or selected a GitHub repository
- [ ] Configured webhook in GitHub settings
- [ ] GitHub ping event received successfully (green checkmark)
- [ ] Made a commit to trigger webhook
- [ ] Webhook received and logged in Flask terminal
- [ ] Saw full commit details in the log
- [ ] Inspected webhook payload in ngrok dashboard

**Part 3: Team Collaboration**
- [ ] Shared ngrok URL with teammate
- [ ] Successfully tested teammate's API
- [ ] Created user on teammate's API

**Part 4: Security (Optional)**
- [ ] Generated webhook secret
- [ ] Configured secret in GitHub
- [ ] Implemented signature verification
- [ ] Verified that webhook still works with signature

## Real-World Applications of GitHub Webhooks

Now that you understand webhooks, here are real-world scenarios where they're used:

### 1. Continuous Integration/Deployment (CI/CD)
```
Developer pushes code → GitHub webhook → Your server
                                      ↓
                              Automatically:
                              - Run tests
                              - Build application
                              - Deploy if tests pass
```

**Example tools**: Jenkins, GitHub Actions, CircleCI all use webhooks

### 2. Project Management Automation
```
Push to repo → Webhook → Update Jira ticket status
                      → Post to Slack channel
                      → Update project dashboard
```

### 3. Code Review Workflows
```
Pull Request created → Webhook → Assign reviewers automatically
                               → Run linters
                               → Check for security issues
```

### 4. Documentation Generation
```
Push to main → Webhook → Rebuild documentation site
                      → Update API reference
                      → Deploy to production
```

### 5. Team Notifications
```
Push event → Webhook → Send Discord/Slack notification
                    → Email team members
                    → Update team dashboard
```

**In ProManage Project (Exercise 13):**
You could use webhooks to notify team members when:
- A new task is created
- Project status changes
- Assignments are updated

## Preparing for ProManage Team Project

In Exercise 13 (ProManage), you'll work in teams where:
- **Each member develops their own microservice**
- **Services need to communicate with each other**
- **ngrok allows you to share your API without deployment**

Example scenario:
- Student A: User authentication service (port 5000)
- Student B: Project management service (port 5001)
- Student C: Task management service (port 5002)

Each runs their service locally, exposes via ngrok, and shares URLs with the team.

```bash
# Student A's auth service
ngrok http 5000
# Share: https://student-a.ngrok-free.app

# Student B's project service
ngrok http 5001
# Share: https://student-b.ngrok-free.app

# Student C can now call both services:
curl https://student-a.ngrok-free.app/login -d '{"username":"test","password":"pass"}'
curl https://student-b.ngrok-free.app/projects -H "Authorization: Bearer <token>"
```

**This exercise prepares you for exactly this workflow!**

## Additional Resources

### Official Documentation
- **[ngrok Documentation](https://ngrok.com/docs)** - Complete ngrok reference
- **[ngrok Getting Started](https://ngrok.com/docs/getting-started)** - Quick start guide (2025)
- **[GitHub Webhooks](https://docs.github.com/en/webhooks/webhook-events-and-payloads)** - Official webhook documentation
- **[Creating GitHub Webhooks](https://docs.github.com/en/webhooks/using-webhooks/creating-webhooks)** - Setup guide

### Tutorials
- [ngrok + Flask Integration](https://ngrok.com/docs/integrations/python/flask) - Official Flask guide
- [GitHub Webhook Security](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) - Signature verification
- [Testing Webhooks Locally](https://ngrok.com/docs/guides/webhooks/local-testing) - Development best practices

### Alternative Tools (for reference)
- [localtunnel](https://localtunnel.me/) - Open source alternative
- [Cloudflare Tunnel](https://www.cloudflare.com/products/tunnel/) - Free, permanent URLs
- [Hookdeck](https://hookdeck.com/) - Webhook testing platform

## Deliverables

When you complete this exercise, you should have:

1. **ngrok Setup**:
   - ngrok installed and authenticated
   - Successfully exposed Flask API with public URL

2. **Real GitHub Webhook**:
   - GitHub repository with configured webhook
   - Flask app receiving real push events
   - Completed TODOs in `app.py` for GitHub webhook handling

3. **Evidence** (screenshots or documentation):
   - ngrok terminal showing public URL
   - GitHub webhook settings page showing active webhook with green checkmark
   - Flask terminal showing received webhook with commit details
   - ngrok dashboard (localhost:4040) showing the GitHub webhook request

4. **Team Collaboration**:
   - Successfully shared your API with a teammate
   - Tested a teammate's API endpoints

5. **Optional - Security**:
   - Implemented webhook signature verification
   - Tested that verification works correctly

## Evaluation Criteria

Your work will be evaluated on:

1. **ngrok Setup** (20%):
   - ngrok properly installed and authenticated
   - Flask app successfully exposed with public URL

2. **Real GitHub Webhook** (40%):
   - GitHub webhook properly configured
   - Flask endpoint correctly handles real GitHub payloads
   - Successfully receives and processes push events
   - Correct extraction of repository, pusher, commits, and ref data

3. **Code Quality** (20%):
   - All TODOs completed correctly
   - Code follows the established patterns
   - Proper error handling

4. **Team Collaboration** (15%):
   - Successfully shared API with teammate
   - Tested teammate's API endpoints

5. **Documentation/Evidence** (5%):
   - Clear screenshots or notes showing successful webhook delivery
   - Evidence of testing and verification

## Next Steps

After completing this exercise:

1. **Exercise 12**: Swagger Documentation - Document your APIs professionally
2. **Exercise 13**: ProManage Team Project - Use ngrok for team collaboration
3. **Beyond**: Learn about production deployment (Heroku, AWS, Docker) for real applications

**Note**: ngrok is for development/testing only. Production apps should be properly deployed.

## Questions to Consider

1. Why can't you use `localhost` URLs for webhooks from external services?
2. What are the security implications of exposing your development server?
3. When would you use ngrok vs. actual deployment (Heroku, AWS, etc.)?
4. How would you secure webhook endpoints in production?
5. What happens if your ngrok tunnel disconnects during the ProManage project?

Good luck exposing your APIs to the world! 🚀
