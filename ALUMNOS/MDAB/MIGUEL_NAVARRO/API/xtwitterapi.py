from dotenv import load_dotenv
import os

from sqlalchemy import exists

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

if APP_MODE != None:
    print(f"Running in {APP_MODE} mode")