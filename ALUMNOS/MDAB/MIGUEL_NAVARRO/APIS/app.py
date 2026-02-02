from dotenv import load_dotenv
import os
import tweepy


# Load environment variables from .env file
load_dotenv()

# Access your credentials
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
APP_MODE = os.getenv('APP_MODE', 'production') # default to 'production'

if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
    raise ValueError("Missing required environment variables. Check your .env file.")

if APP_MODE:
    print(f"Running in {APP_MODE} mode")

def publish_tweet(text):
    if not text or len(text) > 280:
        print("Error: El post debe tener entre 1 y 280 caracteres.")
        return
    
    if APP_MODE == 'development':
        print(f"--- [MOCK MODE] ---")
        print(f"Simulating X post: {text}")
        print("--------------------")
    else:
        try:
            client = tweepy.Client(
                consumer_key=X_API_KEY,
                consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )
            response = client.create_tweet(text=text)
            print(f"Post successfully published! ID: {response.data['id']}")
        except Exception as e:
            print(f"Error publishing tweet: {e}")

if __name__ == "__main__":
    message = input("What's going on? ")
    publish_tweet(message)