import os
import tweepy

def publish_to_x(text: str):
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
        )
    except Exception as exc:
        raise RuntimeError("Failed to initialize X (Twitter) client") from exc

    try:
        response = client.create_tweet(text=text)
    except Exception as exc:
        raise RuntimeError("Failed to publish tweet to X") from exc

    try:
        return response.data["id"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError("Unexpected response format when publishing tweet to X") from exc
