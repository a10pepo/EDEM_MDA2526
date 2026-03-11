# Twitter/X Python Bot (API v2)

A minimal, production-ready **Python bot for X (Twitter)** that posts tweets using **X API v2** with robust error handling, environment variables, and Docker support.

> ⚠️ **Important**: Posting tweets requires an X Developer account with **write permissions**.

---

## Features

* ✅ Uses **X API v2** via `tweepy.Client`
* ✅ OAuth 1.0a user context (required for posting)
* ✅ Environment variables via `.env`
* ✅ Robust error handling and logging
* ✅ Docker-ready
* ✅ Clean exit codes for CI / automation

---

## Project Structure

```text
.
├── twitter_bot.py     # Main bot script
├── requirements.txt  # Python dependencies
├── Dockerfile        # Docker image definition
├── .env              # Environment variables
└── README.md
```

---

## Requirements

* Python **3.9+** (3.11 recommended)
* An **X Developer account** with:

  * App permissions: **Read and Write**
  * Access level that allows **Tweet creation**

---

## Installation (Local)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo>
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
APP_MODE=development
```

## Running the Bot Locally

```bash
python twitter_bot.py
```

If successful, the bot will:

* Authenticate with X
* Post a test tweet
* Exit with status code `0`

---

## Docker Usage

### Build the Docker image

```bash
docker build -t x-python-bot .
```

### Run the container with environment variables

```bash
docker run --env-file .env x-python-bot
```

This keeps secrets **out of the image** and allows safe deployment.

---

## Common Errors

### ❌ `403 Forbidden (Error 453)`

**Cause:** Your X Developer account does not have write access.

**Fix:**

* Upgrade your access tier
* Set app permissions to **Read and Write**
* Regenerate access tokens after changing permissions

---

### ❌ Missing environment variables

Ensure all required keys exist in `.env` and are spelled correctly.

---

## Disclaimer

This project is for educational and automation purposes. You are responsible for complying with **X’s Developer Policy** and **Terms of Service**.
