"""
Twitter/X bot using API v2 (OAuth 1.0a user context) with robust error handling.

Requirements:
  pip install tweepy python-dotenv

NOTE:
  Posting tweets with API v2 STILL requires write permissions
  in your X Developer account.
"""

import os
import sys
import logging
from dotenv import load_dotenv
import tweepy

# -----------------
# Logging setup
# -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------
# Load environment
# -----------------
try:
    load_dotenv()
except Exception as e:
    logger.critical("Failed to load .env file: %s", e)
    sys.exit(1)

X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
APP_MODE = os.getenv("APP_MODE","development").lower()

print(f"Running in {APP_MODE} mode")

missing_vars = [
    name for name, value in {
        "X_API_KEY": X_API_KEY,
        "X_API_SECRET": X_API_SECRET,
        "X_ACCESS_TOKEN": X_ACCESS_TOKEN,
        "X_ACCESS_TOKEN_SECRET": X_ACCESS_TOKEN_SECRET,
    }.items() if not value
]

if missing_vars:
    logger.critical("Missing environment variables: %s", ", ".join(missing_vars))
    sys.exit(1)

# -----------------
# API v2 Client
# -----------------
try:
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True
    )

    client.get_me()
    logger.info("Authentication successful (API v2)")

except tweepy.Forbidden as e:
    logger.critical("Authentication forbidden: check app permissions")
    logger.critical(e)
    sys.exit(1)

except tweepy.TweepyException as e:
    logger.critical("Failed to authenticate: %s", e)
    sys.exit(1)

# -----------------
# Bot actions
# -----------------
def post_tweet(text: str) -> bool:
    """Post a tweet using X API v2.

    Returns True if successful, False otherwise.
    """
    if not text or not text.strip():
        logger.warning("Tweet text is empty")
        return False

    try:
        response = client.create_tweet(text=text)

        if response and response.data:
            tweet_id = response.data.get("id")
            logger.info("Tweet posted successfully (id=%s)", tweet_id)
            return True

        logger.error("Tweet creation returned no data")

    except tweepy.Forbidden as e:
        logger.error("403 Forbidden: app lacks write permissions")

    except tweepy.TooManyRequests:
        logger.error("Rate limit exceeded")

    except tweepy.TweepyException as e:
        logger.error("Failed to post tweet: %s", e)

    except Exception as e:
        logger.exception("Unexpected error: %s", e)

    return False


if __name__ == "__main__":
    success = post_tweet("Hello X! This tweet was sent using API v2 🚀")
    if not success:
        sys.exit(1)
