# 🚀 X API Challenge: Post Publisher

## 📝 Description
This project is a Python-based automated post publisher for X (formerly Twitter). It was developed as part of an API integration challenge. The application allows users to validate message length and publish content directly to X using the v2 API.

## ✨ Features
- **Input Validation:** Ensures posts adhere to the 280-character limit.
- **Environment Management:** Securely handles API credentials using `.env` files to prevent credential leakage.
- **Mock Mode:** Includes a development toggle to simulate posts without consuming API quota.
- **Error Handling:** Robust try-except blocks to catch and report API-specific errors.

## 🛠️ Technologies
- **Python 3.x**
- **Tweepy:** Modern library for X API v2 integration.
- **Python-dotenv:** For managing environment variables.

## ⚙️ Setup & Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows/Bash
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Configuration:
   Copy .env.example to .env
   Fill in your X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, and X_ACCESS_TOKEN_SECRET.
   Set APP_MODE=production to enable live posting.
5. Usage.
   ```bash
   python app.py
   Enter your post content when prompted.

## 📸 Proof of Concept & Execution Logs

To demonstrate the application's functionality across different environments, the following logs capture the transition from local testing to live API interaction.

1. Development Mode (Mocking)
Before making live requests, the application was tested in `development` mode to verify input validation and logic without consuming API quota.
> **Note:** This verifies that the script correctly identifies the environment and handles the payload.

![Development Mode Screenshot](ALUMNOS\MDAB\MIGUEL_NAVARRO\API\development.png)

2. Production Mode (Live API Request)
After successful local testing, the `APP_MODE` was switched to `production`. 
> **Observation:** As shown in the log below, the application successfully authenticated and attempted to create the tweet. However, the X API returned an **HTTP 402 Payment Required** error, indicating that the current "Free" tier for this specific developer account requires a paid subscription to perform write operations.

![Production Mode Screenshot](ALUMNOS\MDAB\MIGUEL_NAVARRO\API\production.png)